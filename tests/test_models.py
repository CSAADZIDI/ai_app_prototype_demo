from unittest.mock import patch

import api.models as models


# -------------------------------------
# Helper: fake dummy model/scaler dict
# -------------------------------------
DUMMY_MODEL_DATA = {
    "model_a": "dummy_model_a",
    "model_m": "dummy_model_m",
    "scaler_Xa": "dummy_scaler_Xa",
    "scaler_ya": "dummy_scaler_ya",
    "scaler_Xm": "dummy_scaler_Xm",
    "scaler_ym": "dummy_scaler_ym",
}


# -------------------------------------
# Tests using joblib.load patching
# -------------------------------------
@patch("api.models.joblib.load", return_value=DUMMY_MODEL_DATA)
def test_load_model_a_lille(mock_load):
    result = models.load_model_a_lille()
    assert result == "dummy_model_a"
    mock_load.assert_called_once_with(models.models_file)


@patch("api.models.joblib.load", return_value=DUMMY_MODEL_DATA)
def test_load_scaler_Xa_lille(mock_load):
    result = models.load_scaler_Xa_lille()
    assert result == "dummy_scaler_Xa"
    mock_load.assert_called_once_with(models.models_file)


@patch("api.models.joblib.load", return_value=DUMMY_MODEL_DATA)
def test_load_model_m_lille(mock_load):
    result = models.load_model_m_lille()
    assert result == "dummy_model_m"
    mock_load.assert_called_once_with(models.models_file)


@patch("api.models.joblib.load", return_value=DUMMY_MODEL_DATA)
def test_load_model_a_bordeaux(mock_load):
    result = models.load_model_a_bordeaux()
    assert result == "dummy_model_a"
    mock_load.assert_called_once_with(models.models_bordeaux_file)


@patch("api.models.joblib.load", return_value=DUMMY_MODEL_DATA)
def test_load_model_m_bordeaux(mock_load):
    result = models.load_model_m_bordeaux()
    assert result == "dummy_model_m"
    mock_load.assert_called_once_with(models.models_bordeaux_file)


@patch("api.models.joblib.load", return_value=DUMMY_MODEL_DATA)
def test_load_scaler_ym_lille(mock_load):
    result = models.load_scaler_ym_lille()
    assert result == "dummy_scaler_ym"
    mock_load.assert_called_once_with(models.models_file)
