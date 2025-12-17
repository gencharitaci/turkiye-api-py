# Turkiye API (Python/FastAPI)

> **Language / Dil**: [English](README.md) | [Türkçe](README_TR.md)

**Version 1.1.1** | **Production Ready** ✅

TurkiyeAPI is a comprehensive REST API providing detailed information about Turkiye's administrative divisions including provinces, districts, neighborhoods and villages with demographic and geographical data.

This is a Python/FastAPI implementation based on the original [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) project by [Ubeyde Emir Özdemir](https://github.com/ubeydeozdmr), licensed under the MIT License.

## ✨ Features

### Core Features

- **FastAPI Framework**: Modern, fast (high-performance), web framework for building APIs
- **Multi-Language Documentation**: Automatic language detection with English and Turkish support
- **Scalar Documentation**: Beautiful, interactive API documentation with modern UI
- **OpenAPI Support**: Full OpenAPI 3.0 specification in multiple languages
- **Type Safety**: Full type hints with Pydantic models
- **API Versioning**: Comprehensive versioning strategy (`/api/v1/...`) for smooth migrations

### Security & Performance 🔒⚡

- **OWASP Security Headers**: All critical security headers implemented (CSP, X-Frame-Options, HSTS, etc.)
- **Secured Health Endpoint**: Environment-aware detail levels with optional authentication
- **Redis Caching**: High-performance distributed caching with automatic key generation and 30-minute TTL
- **Rate Limiting**: Built-in rate limiting with Redis support for distributed deployments
- **CORS Configuration**: Environment-aware Cross-Origin Resource Sharing
- **GZip Compression**: Automatic response compression for better performance

### Quality & DevOps 🧪🚀

- **Comprehensive Testing**: 80+ tests across all layers (data, services, API, middleware)
- **Automated Workflows**: GitHub Actions for data and documentation synchronization
- **Pre-commit Hooks**: Automated code quality checks (Black, isort, flake8, Bandit, mypy)
- **Code Quality**: 9.0/10 quality score with excellent maintainability
- **Production Ready**: Docker, Gunicorn, comprehensive deployment guides, and production config templates

### Monitoring & Observability 📊

- **Prometheus Metrics**: Built-in metrics at `/metrics` endpoint
- **Structured Logging**: JSON logging with configurable levels
- **Health Checks**: Enhanced health endpoint with dependency status monitoring

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/gencharitaci/turkiye-api-py.git
cd turkiye-api-py
```

2. Create a virtual environment:

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
# For development
cp .env.example .env

# For production (recommended)
cp .env.production.recommended .env
```

Edit `.env` to customize settings. See [Configuration](#configuration) section for details.

5. (Optional) Set up pre-commit hooks for code quality:

```bash
pip install pre-commit
pre-commit install
```

## Using as Python SDK

After installing via pip, you can use the package as a Python SDK to interact with any Turkiye API server:

### Installation from PyPI

```bash
# Install the latest version
pip install turkiye-api-py

# Or install a specific version
pip install turkiye-api-py==1.1.1
```

### Quick Start with SDK

```python
from app import TurkiyeClient

# Connect to a running API server (you need to have a server running)
client = TurkiyeClient(base_url="http://localhost:8181")

# Get all provinces
provinces = client.get_provinces()
print(f"Total provinces: {len(provinces)}")

# Get Istanbul (ID: 34)
istanbul = client.get_province(34)
print(f"{istanbul['name']}: {istanbul['population']:,} people")

# Get districts in Istanbul
districts = client.get_districts(province_id=34)
print(f"Istanbul has {len(districts)} districts")

# Filter provinces by population
large_cities = client.get_provinces(min_population=1000000)
for city in large_cities:
    print(f"{city['name']}: {city['population']:,}")
```

### Running Your Own API Server

To use the SDK, you need an API server running. You can either:

**Option 1: Run the server from the installed package**

```bash
# Start the server (after pip install)
turkiye-api serve

# Start with auto-reload for development
turkiye-api serve --reload

# Start on a custom port
turkiye-api serve --port 8000
```

**Option 2: Connect to an existing server**

```python
from app import TurkiyeClient

# Connect to a remote server
client = TurkiyeClient(base_url="https://your-api-domain.com")
provinces = client.get_provinces()
```

### SDK Features

- **Simple & Pythonic**: Clean, intuitive API
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Comprehensive error messages
- **Context Manager**: Automatic resource cleanup
- **Pagination**: Built-in pagination support
- **Filtering**: Advanced filtering options
- **Language Support**: English and Turkish responses

For complete SDK documentation and examples, see [SDK_USAGE.md](https://github.com/gencharitaci/turkiye-api-py/blob/master/docs/SDK_USAGE.md)

## Running the Application

### Development Mode

```bash
python run.py
```

The API will be available at: `http://localhost:8181`

### Production Mode

For production deployment, we recommend using Gunicorn with Uvicorn workers or Docker:

**Option 1: Docker (Recommended)**

```bash
docker-compose up -d
```

**Option 2: Gunicorn**

```bash
gunicorn -c gunicorn.conf.py app.main:app
```

**Option 3: Quick Start Scripts**

```bash
# Linux/Mac
chmod +x start-production.sh
./start-production.sh

# Windows
start-production.bat
```

For detailed production deployment instructions, see [DEPLOYMENT_EN.md](https://github.com/gencharitaci/turkiye-api-py/blob/master/docs/DEPLOYMENT_EN.md) or [DEPLOYMENT_TR.md](https://github.com/gencharitaci/turkiye-api-py/blob/master/docs/DEPLOYMENT_TR.md)

## Configuration

### Environment Variables

Key configuration options (see `.env.production.recommended` for complete list):

```env
# Application
ENVIRONMENT=production
DEBUG=false
PORT=8181
WORKERS=4

# Security (CRITICAL for production)
EXPOSE_SERVER_HEADER=false
HEALTH_CHECK_DETAILED=false
HEALTH_CHECK_AUTH_ENABLED=true
HEALTH_CHECK_PASSWORD=your-secure-password

# Redis (for caching and rate limiting)
REDIS_URL=redis://localhost:6379/0

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100

# CORS
ALLOWED_ORIGINS=https://yourdomain.com
```

### Security Configuration

**Production Security Checklist**:

- ✅ Set `HEALTH_CHECK_DETAILED=false` to minimize information disclosure
- ✅ Enable `HEALTH_CHECK_AUTH_ENABLED=true` for sensitive environments
- ✅ Set strong `HEALTH_CHECK_PASSWORD`
- ✅ Keep `EXPOSE_SERVER_HEADER=false` to prevent technology stack exposure
- ✅ Configure `ALLOWED_ORIGINS` with your actual domains
- ✅ Enable HTTPS via reverse proxy (nginx/Apache)

All OWASP security headers are automatically applied:

- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy (configured)
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy (geolocation, microphone, camera disabled)
- Strict-Transport-Security (production only)

## API Documentation

Once the server is running, you can access the documentation in multiple languages:

- **Auto-Detect Language**: <http://localhost:8181/docs> (Redirects based on browser language)
- **English Documentation**: <http://localhost:8181/docs/en> (Interactive Scalar UI)
- **Turkish Documentation**: <http://localhost:8181/docs/tr> (İnteraktif Scalar UI)
- **English OpenAPI Spec**: <http://localhost:8181/openapi-en.json>
- **Turkish OpenAPI Spec**: <http://localhost:8181/openapi-tr.json>

The documentation automatically detects your browser language and displays content in English or Turkish. You can also manually switch languages using the selector buttons in the top-right corner.

For more details, see the interactive documentation at `/docs` endpoint.

## Documentation Guides

The `guides/` folder contains comprehensive documentation synchronized from the [turkiye-api-docs](https://github.com/ubeydeozdmr/turkiye-api-docs) repository.

**Auto-Sync**: Documentation is automatically updated daily at 2:00 AM UTC via GitHub Actions.

**Manual Sync**:

```bash
# Linux/Mac
./scripts/sync-guides.sh

# Windows
scripts\sync-guides.bat
```

For detailed information about the sync mechanism, see [GUIDES_SYNC.md](https://github.com/gencharitaci/turkiye-api-py/blob/master/docs/GUIDES_SYNC.md)

## Data Synchronization

The `app/data/` folder contains administrative data (provinces, districts, etc.) synchronized from the [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) repository.

**Auto-Sync**: Data is automatically updated weekly on Sunday at 3:00 AM UTC via GitHub Actions.

**Manual Sync**:

```bash
# Linux/Mac
./scripts/sync-data.sh

# Windows
scripts\sync-data.bat
```

**Features**:

- ✅ Automatic JSON validation
- ✅ Backup before update
- ✅ Weekly scheduled sync
- ✅ Manual trigger available

For detailed information about data synchronization, see [DATA_SYNC.md](https://github.com/gencharitaci/turkiye-api-py/blob/master/docs/DATA_SYNC.md)

## Advanced Features

For information about advanced features including rate limiting, Redis integration, API versioning, and monitoring, see [ADVANCED_FEATURES.md](https://github.com/gencharitaci/turkiye-api-py/blob/master/docs/ADVANCED_FEATURES.md).

### Quick Overview

- **Rate Limiting**: Protect your API from abuse with configurable rate limits
- **Redis Integration**: Distributed rate limiting for multi-instance deployments
- **API Versioning**: `/api/v1/...` with support for future versions
- **Monitoring**: Prometheus metrics at `/metrics` endpoint
- **Version Info**: Get supported versions at `/api/versions`

## API Endpoints

### System Endpoints

- `GET /health` - Enhanced health check with dependency status
- `GET /api/versions` - Get supported API versions information

### Language Endpoints

- `GET /api/v1/language` - Get current language preference
- `POST /api/v1/language` - Set language preference
- `GET /api/v1/languages` - Get list of supported languages

### Provinces

- `GET /api/v1/provinces` - Get all provinces with optional filters
- `GET /api/v1/provinces/{id}` - Get specific province by ID

### Districts

- `GET /api/v1/districts` - Get all districts with optional filters
- `GET /api/v1/districts/{id}` - Get specific district by ID

### Neighborhoods

- `GET /api/v1/neighborhoods` - Get all neighborhoods with optional filters
- `GET /api/v1/neighborhoods/{id}` - Get specific neighborhood by ID

### Villages

- `GET /api/v1/villages` - Get all villages with optional filters
- `GET /api/v1/villages/{id}` - Get specific village by ID

### Towns

- `GET /api/v1/towns` - Get all towns with optional filters
- `GET /api/v1/towns/{id}` - Get specific town by ID

## Query Parameters

All list endpoints support these common query parameters:

- `name`: Filter by name (partial match)
- `minPopulation`: Minimum population filter
- `maxPopulation`: Maximum population filter
- `offset`: Pagination offset
- `limit`: Pagination limit
- `fields`: Comma-separated list of fields to return
- `sort`: Sort by field (prefix with `-` for descending)

Additional filters vary by endpoint. See the interactive documentation for details.

## Example Requests

### Get all provinces

```bash
curl http://localhost:8181/api/v1/provinces
```

### Get provinces with population over 1 million

```bash
curl http://localhost:8181/api/v1/provinces?minPopulation=1000000
```

### Get a specific province (Istanbul, id=34)

```bash
curl http://localhost:8181/api/v1/provinces/34
```

### Get districts in a specific province

```bash
curl http://localhost:8181/api/v1/districts?provinceId=34
```

### Get only specific fields

```bash
curl http://localhost:8181/api/v1/provinces?fields=id,name,population
```

## Testing

The project includes comprehensive test coverage (80+ tests) across all layers.

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing

# Run with HTML coverage report
pytest tests/ -v --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

### Test Structure

```
tests/
├── test_data_loader.py              # DataLoader tests (14 tests)
├── test_api/
│   └── test_provinces_endpoint.py   # API integration tests (19 tests)
├── test_services/
│   ├── test_base_service.py         # Base service tests (18 tests)
│   └── test_province_service.py     # Province service tests (18 tests)
└── test_middleware/
    └── test_security.py             # Security middleware tests (11 tests)
```

**Current Coverage**: 80+ tests covering:

- ✅ Data loading and caching
- ✅ Service layer (filtering, sorting, pagination)
- ✅ API endpoints (all HTTP methods and error cases)
- ✅ Security middleware (all OWASP headers)

For detailed testing guide, see [TESTING.md](https://github.com/gencharitaci/turkiye-api-py/blob/master/docs/TESTING.md)

## Project Structure

```
turkiye-api-py/
├── app/
│   ├── data/                 # JSON data files
│   ├── i18n/                 # Internationalization
│   ├── middleware/           # Request/response middleware
│   │   ├── security.py       # Security headers (NEW)
│   │   ├── metrics.py        # Prometheus metrics
│   │   └── language.py       # Language detection
│   ├── models/               # Pydantic models and schemas
│   ├── routers/              # API route handlers
│   ├── services/             # Business logic layer
│   │   ├── cache_service.py  # Redis caching service (NEW)
│   │   ├── base_service.py   # Base service utilities
│   │   └── *_service.py      # Domain services
│   ├── main.py               # FastAPI application
│   ├── settings.py           # Configuration management
│   └── scalar_docs.py        # API documentation setup
├── tests/                    # Test suite (80+ tests) (NEW)
│   ├── test_api/             # API integration tests
│   ├── test_services/        # Service unit tests
│   ├── test_middleware/      # Middleware tests
│   └── conftest.py           # Test fixtures
├── docs/                     # Documentation (NEW)
│   ├── ADVANCED_FEATURES.md  # Advanced features guide
│   ├── CHANGELOG.md          # Version history
│   ├── DATA_SYNC.md          # Data synchronization guide
│   ├── DEPLOYMENT_EN.md      # Deployment guide (English)
│   ├── DEPLOYMENT_TR.md      # Deployment guide (Turkish)
│   ├── GUIDES_SYNC.md        # Documentation sync guide
│   ├── IMPLEMENTATION_SUMMARY.md  # Implementation details
│   ├── PRODUCTION_READINESS.md    # Production checklist
│   └── TESTING.md            # Testing guide
├── scripts/                  # Utility scripts (NEW)
│   ├── sync-data.sh          # Data sync script (Linux/Mac)
│   ├── sync-data.bat         # Data sync script (Windows)
│   ├── sync-guides.sh        # Guides sync script (Linux/Mac)
│   └── sync-guides.bat       # Guides sync script (Windows)
├── .github/
│   └── workflows/
│       ├── sync-data.yml     # Data sync workflow (NEW)
│       └── sync-guides.yml   # Guides sync workflow (NEW)
├── requirements.txt          # Python dependencies
├── run.py                    # Development server runner
├── gunicorn.conf.py          # Production Gunicorn configuration
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
├── .env.example              # Development environment template
├── .env.production.recommended  # Production config template (NEW)
├── .pre-commit-config.yaml   # Pre-commit hooks (NEW)
├── README.md                 # This file (English)
└── README_TR.md              # Turkish README
```

## Technology Stack

### Core Framework

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation
- **Gunicorn**: Production WSGI/ASGI server

### Performance & Caching

- **Redis**: Distributed caching and rate limiting
- **In-Memory Cache**: Pre-indexed data structures for O(1) lookups

### Security

- **OWASP Headers**: Comprehensive security header middleware
- **CORS Middleware**: Configurable cross-origin resource sharing
- **Rate Limiting**: Request throttling with Redis backend

### Documentation & API

- **Scalar**: Beautiful, interactive API documentation UI
- **OpenAPI 3.0**: Full specification with multi-language support

### Testing & Quality

- **pytest**: Testing framework with 80+ tests
- **pytest-cov**: Code coverage reporting
- **pytest-asyncio**: Async test support
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **Bandit**: Security vulnerability scanning
- **mypy**: Static type checking

### DevOps & Monitoring

- **Docker**: Containerization
- **GitHub Actions**: Automated data and documentation synchronization
- **Prometheus**: Metrics collection
- **Pre-commit**: Git hooks for code quality

## Sources

- [Population of districts](https://biruni.tuik.gov.tr/medas)
- [Area of districts](https://web.archive.org/web/20190416051733/https://www.harita.gov.tr/images/urun/il_ilce_alanlari.pdf)

## Contributing

Contributions are welcome! This project maintains high quality standards with comprehensive testing and automated quality checks.

### Development Workflow

1. **Fork and Clone**

   ```bash
   git clone https://github.com/YOUR_USERNAME/turkiye-api-py.git
   cd turkiye-api-py
   ```

2. **Set Up Development Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install pre-commit pytest pytest-cov
   pre-commit install
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Write Code and Tests**
   - Follow existing code style (enforced by Black, isort, flake8)
   - Add tests for new features (maintain 80%+ coverage)
   - Update documentation as needed

5. **Run Quality Checks**

   ```bash
   # Run tests
   pytest tests/ -v --cov=app

   # Run pre-commit hooks
   pre-commit run --all-files
   ```

6. **Commit and Push**

   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure all tests and quality checks pass locally

### Coding Standards

- **Code Style**: Black formatting with 120-character line length
- **Import Sorting**: isort with Black profile
- **Type Hints**: Required for all public functions and methods
- **Docstrings**: Required for all public classes and functions
- **Testing**: Minimum 80% code coverage for new code
- **Security**: All code scanned by Bandit

### Pull Request Guidelines

- ✅ All tests must pass
- ✅ Code coverage must not decrease
- ✅ Pre-commit hooks must pass
- ✅ Clear commit messages (conventional commits preferred)
- ✅ Update CHANGELOG.md for notable changes
- ✅ For major changes, open an issue first to discuss

### Running Quality Checks Locally

Run these checks locally before committing to ensure code quality:

```bash
# Test matrix (Python 3.8-3.11)
pytest tests/ -v --cov=app

# Linting
black --check app/ tests/
isort --check app/ tests/
flake8 app/ tests/
mypy app/

# Security
bandit -r app/ -ll
```

### Documentation

When adding new features:

- Update README.md (English and Turkish)
- Add examples to API documentation in `app/scalar_docs.py`
- Update DEPLOYMENT guides if configuration changes
- Add entries to CHANGELOG.md

Thank you for contributing to Turkiye API! 🎉

## Credits

This project is based on the original [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) by [Ubeyde Emir Özdemir](https://github.com/ubeydeozdmr).

**Original Author**: Ubeyde Emir Özdemir

- Email: [ubeydeozdmr@gmail.com](mailto:ubeydeozdmr@gmail.com)
- Telegram: [@ubeydeozdmr](https://t.me/ubeydeozdmr)
- GitHub: [@ubeydeozdmr](https://github.com/ubeydeozdmr)

**Python Implementation**: Adem Kurtipek

- Email: [gncharitaci@gmail.com](mailto:gncharitaci@gmail.com)
- GitHub: [@gencharitaci](https://github.com/gencharitaci)
- Repository: [turkiye-api-py](https://github.com/gencharitaci/turkiye-api-py)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Based on the original [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) project, also licensed under MIT.
