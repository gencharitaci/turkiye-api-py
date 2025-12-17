# Publishing to PyPI Guide

This guide explains how to build and publish the `turkiye-api-py` package to the Python Package Index (PyPI).

## 📦 Package Overview

The package provides both:
1. **REST API Server** - Full FastAPI application
2. **Python SDK Client** - Programmatic access library

## 🔧 Prerequisites

### 1. Install Build Tools

```bash
# Install build dependencies
pip install --upgrade pip
pip install build twine

# Optional: Install development dependencies
pip install -e ".[dev]"
```

### 2. Create PyPI Account

- **TestPyPI** (for testing): https://test.pypi.org/account/register/
- **PyPI** (production): https://pypi.org/account/register/

### 3. Configure API Tokens

1. Generate API token from PyPI account settings
2. Create `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

**Security Note**: Keep your API tokens secure! Never commit them to version control.

## 🏗️ Building the Package

### Step 1: Clean Previous Builds

```bash
# Windows
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist turkiye_api_py.egg-info rmdir /s /q turkiye_api_py.egg-info

# Linux/Mac
rm -rf dist/ build/ *.egg-info/
```

### Step 2: Update Version

Edit `pyproject.toml` and update version number:

```toml
[project]
version = "1.1.0"  # Update this
```

Also update in:
- `app/__init__.py` (`__version__`)
- `app/settings.py` (`app_version`)

### Step 3: Build Distribution

```bash
# Build both source distribution (.tar.gz) and wheel (.whl)
python -m build
```

This creates:
- `dist/turkiye-api-py-1.1.0.tar.gz` (source distribution)
- `dist/turkiye_api_py-1.1.0-py3-none-any.whl` (wheel distribution)

### Step 4: Verify Package Contents

```bash
# List files in the distribution
tar -tzf dist/turkiye-api-py-1.1.0.tar.gz

# Check package metadata
twine check dist/*
```

Expected output:
```
Checking dist/turkiye-api-py-1.1.0.tar.gz: PASSED
Checking dist/turkiye_api_py-1.1.0-py3-none-any.whl: PASSED
```

## 🧪 Testing on TestPyPI

**Always test on TestPyPI before publishing to production PyPI!**

### Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

### Install from TestPyPI

```bash
# Create new virtual environment for testing
python -m venv test_venv
source test_venv/bin/activate  # Windows: test_venv\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ turkiye-api-py
```

**Note**: `--extra-index-url` is needed because TestPyPI doesn't have all dependencies.

### Test the Package

```bash
# Test CLI
turkiye-api version
turkiye-api info

# Test client SDK
python -c "from app import TurkiyeClient; print('SDK import successful!')"

# Run server (in background)
turkiye-api serve --port 8282 &

# Test API call
python -c "from app import TurkiyeClient; client = TurkiyeClient('http://localhost:8282'); print(client.health())"
```

## 🚀 Publishing to PyPI

### Final Checks

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Code quality checks pass: `pre-commit run --all-files`
- [ ] Version numbers updated in all files
- [ ] CHANGELOG.md updated
- [ ] README.md updated with installation instructions
- [ ] Tested on TestPyPI successfully

### Upload to PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

You'll see output like:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading turkiye-api-py-1.1.0.tar.gz
Uploading turkiye_api_py-1.1.0-py3-none-any.whl
```

### Verify Publication

```bash
# Install from PyPI
pip install turkiye-api-py

# Verify installation
turkiye-api version
```

Visit your package page: `https://pypi.org/project/turkiye-api-py/`

## 📖 Usage Examples After Publishing

### As a Server

```bash
# Install with server dependencies
pip install turkiye-api-py[server]

# Run server
turkiye-api serve

# Production with workers
turkiye-api serve --workers 4
```

### As a Library

```python
# Install base package
# pip install turkiye-api-py

from app import TurkiyeClient

# Create client
client = TurkiyeClient(base_url="http://localhost:8181")

# Or connect to remote API
# client = TurkiyeClient(base_url="https://api.example.com")

# Get provinces
provinces = client.get_provinces()
print(f"Found {len(provinces)} provinces")

# Get specific province
istanbul = client.get_province(34)
print(f"Province: {istanbul['name']}")

# Get districts in Istanbul
districts = client.get_districts(province_id=34)
print(f"Istanbul has {len(districts)} districts")

# Use context manager
with TurkiyeClient() as client:
    provinces = client.get_provinces(min_population=1000000)
    for province in provinces:
        print(f"{province['name']}: {province['population']:,}")
```

## 🔄 Updating the Package

### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes (2.0.0)
- **MINOR**: New features, backward compatible (1.2.0)
- **PATCH**: Bug fixes (1.1.1)

### Update Checklist

1. Update version in `pyproject.toml`
2. Update version in `app/__init__.py`
3. Update version in `app/settings.py`
4. Update `CHANGELOG.md` with changes
5. Commit changes
6. Create git tag: `git tag v1.1.0`
7. Build and test on TestPyPI
8. Upload to PyPI
9. Push tag: `git push origin v1.1.0`

## 🛠️ Automation Options

### GitHub Actions (Recommended)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## 📊 Package Statistics

After publishing, monitor your package:

- **PyPI Stats**: https://pypistats.org/packages/turkiye-api-py
- **Downloads**: https://pepy.tech/project/turkiye-api-py
- **Libraries.io**: https://libraries.io/pypi/turkiye-api-py

## ❓ Troubleshooting

### Common Issues

**Issue**: `twine: error: unrecognized arguments`
**Solution**: Upgrade twine: `pip install --upgrade twine`

**Issue**: `HTTPError: 403 Forbidden`
**Solution**: Check your API token in `~/.pypirc`

**Issue**: `Package already exists`
**Solution**: Version already published. Increment version number.

**Issue**: `Invalid distribution file`
**Solution**: Run `twine check dist/*` to see validation errors

### Getting Help

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- GitHub Issues: https://github.com/gencharitaci/turkiye-api-py/issues

## 📝 Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help Documentation](https://pypi.org/help/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
- [PEP 517 - Build System](https://peps.python.org/pep-0517/)
- [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/)

---

**Last Updated**: 2025-12-16
**Maintainer**: Adem Kurtipek (gncharitaci@gmail.com)
