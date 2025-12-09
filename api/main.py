from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from .metrics import REQUEST_COUNT, REQUEST_LATENCY
import time

from .routes import router
from .routes_monitoring import router_monitoring
from .models import (
    load_model_a_lille,
    load_model_m_lille,
    load_scaler_Xa_lille,
    load_scaler_Xm_lille,
    load_scaler_ya_lille,
    load_scaler_ym_lille,
    load_model_a_bordeaux,
    load_model_m_bordeaux,
)



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context: load models and scalers on startup,
    clean up if necessary on shutdown.
    """
    # Load models & scalers
    app.state.model_a = load_model_a_lille()
    app.state.model_m = load_model_m_lille()
    app.state.scaler_Xa = load_scaler_Xa_lille()
    app.state.scaler_Xm = load_scaler_Xm_lille()
    app.state.scaler_ya = load_scaler_ya_lille()
    app.state.scaler_ym = load_scaler_ym_lille()
    app.state.model_a_b = load_model_a_bordeaux()
    app.state.model_m_b = load_model_m_bordeaux()

    # You can initialize metrics here if needed
    # e.g., from .metrics import initialize_metrics
    # initialize_metrics(app)

    print("✅ Models and scalers loaded successfully")

    yield  # app runs here

    # Shutdown: optional cleanup
    print("App is shutting down...")

# Initialize FastAPI with lifespan
app = FastAPI(
    title="Welcome to the Price Prediction Application",
    description=(
        "Cette API permet d'estimer le prix au mètre carré d'un bien immobilier "
        "(appartement ou maison) en fonction de ses caractéristiques."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Include your routers
app.include_router(router)
app.include_router(router_monitoring)

# ----------------- Middleware for Prometheus -----------------


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    """
    Middleware to track Prometheus metrics automatically for all endpoints.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    endpoint = request.url.path
    method = request.method

    # Increment request count
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

    # Observe latency
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(process_time)

    return response



