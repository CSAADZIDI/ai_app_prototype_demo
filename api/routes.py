from fastapi import APIRouter, Request, BackgroundTasks, Depends
from fastapi.responses import RedirectResponse
from .schemas import House, Prediction, CityHouse
from .services import make_prediction
from .security import authenticate
from .metrics import REQUEST_COUNT, REQUEST_LATENCY
import time

router = APIRouter()


@router.get("/", include_in_schema=False)
async def root():
    """
    Redirige automatiquement la racine de l'application vers la documentation interactive (/docs).
    """
    return RedirectResponse(url="/docs")


@router.post("/predict/lille", response_model=Prediction, summary="Prédiction pour Lille")
async def get_prediction_lille(
    house: House,
    request: Request,
    background_tasks: BackgroundTasks,
    _: str = Depends(authenticate)
) -> Prediction:
    """
    Prédit le prix au m² pour un bien immobilier situé à Lille.
    """
    method = request.method
    endpoint = "/predict/lille"
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    start = time.time()
    try:
        return await make_prediction(house, "lille", request,background_tasks)
    finally:
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start)


@router.post("/predict/bordeaux", response_model=Prediction, summary="Prédiction pour Bordeaux")
async def get_prediction_bordeaux(
    house: House,
    request: Request,
    background_tasks: BackgroundTasks
) -> Prediction:
    """
    Prédit le prix au m² pour un bien immobilier situé à Bordeaux.
    """
    method = request.method
    endpoint = "/predict/bordeaux"
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    start = time.time()
    try:
        return await make_prediction(house, "bordeaux", request,background_tasks)
    finally:
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start)


@router.post("/predict", response_model=Prediction, summary="Prédiction générique par ville")
async def get_prediction(
    cityhouse: CityHouse,
    request: Request,
    background_tasks: BackgroundTasks
) -> Prediction:
    """
    Prédit le prix au m² pour un bien immobilier, en fonction de la ville spécifiée.
    """
    method = request.method
    endpoint = "/predict"
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    start = time.time()
    try:
        return await make_prediction(cityhouse.features, cityhouse.ville, request,background_tasks)
    finally:
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start)
