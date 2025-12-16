# Testing Guide

This document provides instructions for running tests and understanding test coverage.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install test dependencies (if not already installed)
pip install pytest pytest-cov pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run with coverage and generate HTML report
pytest tests/ -v --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Structure

```
tests/
├── conftest.py                              # Shared fixtures
├── test_data_loader.py                      # DataLoader tests (14 tests)
├── test_api/
│   ├── __init__.py
│   └── test_provinces_endpoint.py           # Province endpoints (19 tests)
├── test_services/
│   ├── __init__.py
│   ├── test_base_service.py                 # BaseService utilities (18 tests)
│   └── test_province_service.py             # ProvinceService (18 tests)
└── test_middleware/
    ├── __init__.py
    └── test_security.py                     # Security middleware (11 tests)
```

## Test Coverage

### Current Coverage (80+ tests)

| Module | Tests | Coverage |
|--------|-------|----------|
| `app/services/data_loader.py` | 14 | ✅ Excellent |
| `app/services/base_service.py` | 18 | ✅ Excellent |
| `app/services/province_service.py` | 18 | ✅ Good |
| `app/routers/provinces.py` | 19 | ✅ Excellent |
| `app/middleware/security.py` | 11 | ✅ Good |

### Missing Coverage (To Be Added)

| Module | Status | Priority |
|--------|--------|----------|
| `app/services/district_service.py` | ⚠️ No tests | Medium |
| `app/services/neighborhood_service.py` | ⚠️ No tests | Medium |
| `app/services/village_service.py` | ⚠️ No tests | Medium |
| `app/services/town_service.py` | ⚠️ No tests | Medium |
| `app/routers/districts.py` | ⚠️ No tests | Medium |
| `app/routers/neighborhoods.py` | ⚠️ No tests | Medium |
| `app/routers/villages.py` | ⚠️ No tests | Medium |
| `app/routers/towns.py` | ⚠️ No tests | Medium |
| `app/middleware/language.py` | ⚠️ No tests | Low |
| `app/middleware/metrics.py` | ⚠️ No tests | Low |
| `app/i18n/` modules | ⚠️ No tests | Low |

## Running Specific Tests

```bash
# Run only DataLoader tests
pytest tests/test_data_loader.py -v

# Run only service tests
pytest tests/test_services/ -v

# Run only API integration tests
pytest tests/test_api/ -v

# Run only middleware tests
pytest tests/test_middleware/ -v

# Run a specific test class
pytest tests/test_services/test_base_service.py::TestBaseService -v

# Run a specific test function
pytest tests/test_data_loader.py::TestDataLoader::test_singleton_pattern -v

# Run tests matching a pattern
pytest tests/ -k "sort" -v  # All tests with "sort" in name

# Run tests in parallel (faster)
pip install pytest-xdist
pytest tests/ -v -n auto
```

## Test Fixtures

Available fixtures from `tests/conftest.py`:

- `client` - FastAPI TestClient for making HTTP requests
- `data_loader` - DataLoader singleton instance
- `sample_province` - Sample province dictionary
- `sample_district` - Sample district dictionary
- `sample_neighborhood` - Sample neighborhood dictionary

### Using Fixtures

```python
def test_example(client, data_loader):
    """Example test using fixtures."""
    # Use client for API requests
    response = client.get("/api/v1/provinces")
    assert response.status_code == 200

    # Use data_loader for data validation
    provinces = data_loader.provinces
    assert len(provinces) == 81
```

## Writing New Tests

### Test File Naming

- Unit tests: `test_<module_name>.py`
- Integration tests: `test_<feature>_endpoint.py`
- Test classes: `class Test<ClassName>:`
- Test functions: `def test_<what_it_tests>():`

### Example Test Template

```python
"""
Unit tests for <ModuleName>.

Brief description of what this test file covers.
"""
import pytest
from app.services.example_service import ExampleService


class TestExampleService:
    """Test suite for ExampleService."""

    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return ExampleService()

    def test_functionality_description(self, service):
        """Should describe expected behavior."""
        # Arrange
        input_data = {"key": "value"}

        # Act
        result = service.method(input_data)

        # Assert
        assert result["key"] == "value"
```

## Test Categories

### Unit Tests
Test individual components in isolation:
- Services (business logic)
- Data loader (caching, indexing)
- Middleware (request processing)
- Utility functions

### Integration Tests
Test API endpoints end-to-end:
- HTTP request/response cycle
- Status codes
- Response format
- Error handling

### Coverage Goals

- **Minimum**: 70% overall coverage
- **Target**: 80% overall coverage
- **Excellent**: 90%+ overall coverage

Critical modules (services, routers) should have 90%+ coverage.

## Continuous Integration

Tests run automatically on:
- Every push to `main` or `develop`
- Every pull request

See `.github/workflows/ci.yml` for CI configuration.

### CI Test Matrix

Tests run on:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

## Coverage Reports

### Terminal Report

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

Shows:
- Overall coverage percentage
- Per-file coverage
- Missing line numbers

### HTML Report

```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

Interactive HTML report with:
- Line-by-line coverage highlighting
- Branch coverage
- Clickable file tree

### XML Report (for CI)

```bash
pytest tests/ --cov=app --cov-report=xml
```

Generates `coverage.xml` for Codecov integration.

## Common Test Commands

```bash
# Quick test run (no coverage)
pytest tests/ -v

# Test with coverage and summary
pytest tests/ -v --cov=app --cov-report=term

# Test specific file with coverage
pytest tests/test_data_loader.py -v --cov=app.services.data_loader

# Test with verbose output and show print statements
pytest tests/ -v -s

# Test with warnings shown
pytest tests/ -v -W default

# Stop on first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf

# Run tests changed since last commit
pytest tests/ --picked

# Generate JUnit XML for CI
pytest tests/ --junitxml=test-results.xml
```

## Debugging Tests

### Using pytest debugger

```bash
# Drop into debugger on failure
pytest tests/ --pdb

# Drop into debugger on error
pytest tests/ --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### Using print debugging

```python
def test_example(client):
    response = client.get("/api/v1/provinces")
    print(f"Response: {response.json()}")  # Will show with -s flag
    assert response.status_code == 200
```

Run with: `pytest tests/ -v -s`

## Best Practices

1. **Write tests first** (TDD approach when possible)
2. **One assertion per test** (focused tests)
3. **Clear test names** (describes what and why)
4. **Use fixtures** (reduce duplication)
5. **Test edge cases** (empty data, invalid input, errors)
6. **Keep tests independent** (no test depends on another)
7. **Mock external dependencies** (Redis, databases, APIs)
8. **Test error handling** (not just happy path)

## Troubleshooting

### pytest not found

```bash
pip install pytest pytest-cov pytest-asyncio
```

### Import errors

Ensure you're in the project root:
```bash
cd /path/to/turkiye-api-py
pytest tests/
```

### Tests pass locally but fail in CI

- Check Python version differences
- Verify environment variables
- Check for order-dependent tests
- Review CI logs for specific errors

### Coverage report not generated

```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=term
```

## Next Steps

1. Run existing tests to verify setup:
   ```bash
   pytest tests/ -v
   ```

2. Check coverage:
   ```bash
   pytest tests/ --cov=app --cov-report=term-missing
   ```

3. Add tests for uncovered modules (see Missing Coverage table above)

4. Set up pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. Enable GitHub Actions for automated testing

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing best practices](https://docs.python-guide.org/writing/tests/)
