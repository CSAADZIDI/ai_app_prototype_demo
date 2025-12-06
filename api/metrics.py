from prometheus_client import Counter, Histogram, Gauge, generate_latest


# Traffic
REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["method", "endpoint"])
ERROR_COUNT = Counter("api_errors_total", "Total failed requests", ["method", "endpoint", "status_code"])

# Performance
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency", ["method", "endpoint"])

# Model state / business metrics
PREDICTIONS_TOTAL = Counter("predictions_total", "Total predictions made", ["model", "city"])
MODEL_LOADED = Gauge("model_loaded", "1 if model loaded successfully, 0 otherwise", ["model", "city"])


def metrics_response():
    return generate_latest()
