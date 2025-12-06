import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from api.routes import router, authenticate


# ---------------------------
# Build a test FastAPI app
# ---------------------------
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)

    # Override authenticate dependency globally for all tests
    app.dependency_overrides[authenticate] = lambda: "mock_user"
    yield app

    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    return TestClient(app)


# ---------------------------
# Mock make_prediction
# ---------------------------
@pytest.fixture
def mock_make_prediction():
    """Mock async make_prediction"""
    with patch("api.routes.make_prediction", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "prix_m2_estime": 3500.50,
            "ville_modele": "lille",
            "model": "RandomForestRegressor",
        }
        yield mock


# ============================================================
#                      TESTS
# ============================================================

def test_root_redirects_to_docs(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "/docs" in str(response.url)


# ---------------------------
#        /predict/lille
# ---------------------------
def test_predict_lille(client, mock_make_prediction):
    payload = {
        "surface_bati": 80,
        "nombre_pieces": 4,
        "type_local": "maison",
        "surface_terrain": 150,
        "nombre_lots": 1,
    }

    response = client.post("/predict/lille", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "prix_m2_estime": 3500.5,
        "ville_modele": "lille",
        "model": "RandomForestRegressor"
    }
    mock_make_prediction.assert_awaited_once()


# ---------------------------
#       /predict/bordeaux
# ---------------------------
def test_predict_bordeaux(client, mock_make_prediction):
    payload = {
        "surface_bati": 80,
        "nombre_pieces": 4,
        "type_local": "maison",
        "surface_terrain": 150,
        "nombre_lots": 1,
    }

    response = client.post("/predict/bordeaux", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ville_modele"] == "lille"  # from mock return
    mock_make_prediction.assert_awaited_once()


# ---------------------------
#        /predict (generic)
# ---------------------------
def test_predict_generic(client, mock_make_prediction):
    payload = {
        "ville": "lille",
        "features": {
            "surface_bati": 100,
            "nombre_pieces": 5,
            "type_local": "maison",
            "surface_terrain": 200,
            "nombre_lots": 1,
        },
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prix_m2_estime" in data
    mock_make_prediction.assert_awaited_once()
