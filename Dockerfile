# Turkiye API - Production Docker Image
# Version: 1.1.0
# Base: Python 3.13 (slim variant for smaller image size)

FROM python:3.13-slim

# Metadata
LABEL maintainer="Adem Kurtipek <gncharitaci@gmail.com>"
LABEL version="1.1.0"
LABEL description="Turkiye API - FastAPI-based REST API for Turkiye administrative data"

# Set working directory
WORKDIR /app

# Install system dependencies
# gcc: Required for compiling some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: Reduces image size by not caching pip packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application code
# Excludes: tests/, temp/, .git/ (via .dockerignore)
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8181

# Health check
# Checks /health endpoint every 30 seconds
# Note: In production with auth enabled, this may need adjustment
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8181/health')"

# Run application with Gunicorn
# Configuration loaded from gunicorn.conf.py
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]
