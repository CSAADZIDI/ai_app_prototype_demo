from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from .metrics import REQUEST_COUNT, REQUEST_LATENCY, metrics_response
from prometheus_client import CONTENT_TYPE_LATEST




router_monitoring = APIRouter()

@router_monitoring.get("/health")
def health():
    return {"status": "ok"}

@router_monitoring.get("/metrics")
def prometheus_metrics():
    """Expose Prometheus metrics"""
    return PlainTextResponse(metrics_response(), media_type=CONTENT_TYPE_LATEST)
