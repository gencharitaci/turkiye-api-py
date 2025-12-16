#!/bin/bash
#
# Production startup script for Turkiye API v1.1.0
# Usage: ./start-production.sh
#

set -e

echo "========================================"
echo "  Turkiye API - Production Startup"
echo "  Version: 1.1.0"
echo "========================================"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "   For production, copy .env.production.recommended to .env"
    echo "   and configure all settings."
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Startup cancelled."
        exit 1
    fi
else
    echo "✅ Found .env file"
    # Load environment variables
    export $(cat .env | grep -v '^#' | grep -v '^\s*$' | xargs)
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python version: $PYTHON_VERSION"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  WARNING: Virtual environment not activated"
    echo "   Recommended: source venv/bin/activate"
    echo ""
fi

# Check if gunicorn is installed
echo "🔍 Checking for Gunicorn..."
if ! command -v gunicorn &> /dev/null; then
    echo "❌ Gunicorn not found. Installing..."
    pip install gunicorn
else
    echo "✅ Gunicorn is installed"
fi

# Check if Redis is configured
if [ -n "$REDIS_URL" ]; then
    echo "✅ Redis URL configured: $REDIS_URL"
else
    echo "⚠️  WARNING: REDIS_URL not set (caching disabled)"
fi

# Security check
if [ "$HEALTH_CHECK_DETAILED" = "true" ] && [ "$ENVIRONMENT" = "production" ]; then
    echo "⚠️  WARNING: HEALTH_CHECK_DETAILED=true in production"
    echo "   This exposes internal information. Set to 'false' for security."
fi

if [ "$EXPOSE_SERVER_HEADER" = "true" ] && [ "$ENVIRONMENT" = "production" ]; then
    echo "⚠️  WARNING: EXPOSE_SERVER_HEADER=true in production"
    echo "   This exposes technology stack. Set to 'false' for security."
fi

echo ""
echo "========================================"
echo "🚀 Starting Turkiye API..."
echo "   Host: ${HOST:-0.0.0.0}"
echo "   Port: ${PORT:-8181}"
echo "   Workers: ${WORKERS:-auto}"
echo "   Environment: ${ENVIRONMENT:-development}"
echo "========================================"
echo ""

# Start the server
exec gunicorn -c gunicorn.conf.py app.main:app
