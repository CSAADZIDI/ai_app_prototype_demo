FROM python:3.10-slim-bullseye

WORKDIR /app

# Install OS‑level dependencies needed for scientific libs / xgboost / compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      gfortran \
      libgomp1 \
      libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade packaging tools
RUN python -m pip install --upgrade pip setuptools wheel

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Default command (adjust as needed)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
