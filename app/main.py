import copy
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.i18n import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    get_current_language,
    get_language_flag,
    get_language_name,
    get_translations,
)
from app.logging_config import setup_logging
from app.middleware.language import LanguageMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.rate_limit import setup_rate_limiting
from app.middleware.security import SecurityHeadersMiddleware
from app.monitoring import set_app_info, setup_prometheus_metrics, update_data_loader_metrics
from app.routers import districts, neighborhoods, provinces, towns, villages
from app.scalar_docs import setup_scalar_docs
from app.services.data_loader import data_loader
from app.settings import settings
from app.versioning import get_version_info

# Configure logging before app initialization
setup_logging(level=settings.effective_log_level, environment=settings.environment)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown events."""
    # Startup
    app.state.start_time = time.time()
    logger.info("Application starting up...")

    # Pre-load and cache data
    try:
        province_count = len(data_loader.provinces)
        district_count = len(data_loader.districts)
        logger.info(f"Data loaded successfully: {province_count} provinces, {district_count} districts")

        # Update Prometheus metrics with data loader stats
        if settings.prometheus_enabled:
            update_data_loader_metrics(data_loader)
            set_app_info(settings.app_version, settings.environment)

    except Exception as e:
        logger.error(f"Failed to load data: {e}")

    yield

    # Shutdown
    logger.info("Application shutting down...")


app = FastAPI(
    title=settings.app_name,
    description=(
        "This REST API allows you to get data about settlements such as "
        "provinces, districts, neighborhoods and villages in Turkiye."
    ),
    version=settings.app_version,
    docs_url=None,
    redoc_url=None,
    contact={
        "name": "Adem Kurtipek",
        "email": "gncharitaci@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)

# Add Security Headers middleware (OWASP compliance)
# Must be added first to ensure security headers on all responses
app.add_middleware(SecurityHeadersMiddleware, expose_server_header=settings.expose_server_header)

# Add CORS middleware with environment-aware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins_list(),
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
    max_age=settings.cors_max_age,
)

# Add language detection middleware with environment-aware security
app.add_middleware(
    LanguageMiddleware,
    cookie_name=settings.language_cookie_name,
    cookie_max_age=settings.language_cookie_max_age,
    cookie_path=settings.language_cookie_path,
    cookie_secure=settings.cookie_secure,  # True in production (HTTPS only)
    cookie_httponly=False,  # Allow JavaScript access for language switcher
    cookie_samesite=settings.cookie_samesite,  # Strict in production for CSRF protection
)

# Add metrics middleware for request tracking
app.add_middleware(MetricsMiddleware)

# Add GZip compression middleware for bandwidth optimization (60-70% reduction for JSON)
# Must be added after other middleware to compress the final response
app.add_middleware(GZipMiddleware, minimum_size=1000)  # Only compress responses > 1KB

# Setup rate limiting with Redis support (if enabled in settings)
setup_rate_limiting(
    app,
    enabled=settings.rate_limit_enabled,
    limit_per_minute=settings.rate_limit_per_minute,
    storage=settings.rate_limit_storage,
    redis_url=settings.redis_url,
)

# Setup Prometheus metrics (if enabled in settings)
setup_prometheus_metrics(app, enabled=settings.prometheus_enabled)


@app.get("/")
async def root():
    """Root"""
    return {"status": "OK", "message": "Welcome to the TurkiyeAPI"}


@app.get("/health")
async def health(request: Request):
    """
    Enhanced health check endpoint with environment-aware detail level.

    In production or when health_check_detailed=False:
        Returns minimal status information for security
    In development or when health_check_detailed=True:
        Returns detailed status including uptime, version, and data loader info

    Returns:
        Health status (minimal or detailed based on settings)
    """
    # Authentication check if enabled
    if settings.health_check_auth_enabled:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"status": "error", "error": "Authentication required"},
                headers={"WWW-Authenticate": "Basic"},
            )

        # Basic auth validation
        import base64

        try:
            auth_type, credentials = auth_header.split(" ", 1)
            if auth_type.lower() != "basic":
                raise ValueError("Invalid auth type")

            decoded = base64.b64decode(credentials).decode("utf-8")
            username, password = decoded.split(":", 1)

            if username != settings.health_check_username or password != settings.health_check_password:
                return JSONResponse(
                    status_code=401,
                    content={"status": "error", "error": "Invalid credentials"},
                    headers={"WWW-Authenticate": "Basic"},
                )
        except Exception:
            return JSONResponse(
                status_code=401,
                content={"status": "error", "error": "Invalid authorization header"},
                headers={"WWW-Authenticate": "Basic"},
            )

    # Minimal health check for production (security best practice)
    if not settings.health_check_detailed:
        return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}

    # Detailed health check for development/authenticated access
    uptime_seconds = time.time() - app.state.start_time

    # Check data loader health
    data_status = "ok"
    data_details = {}

    try:
        province_count = len(data_loader.provinces)
        district_count = len(data_loader.districts)

        # Verify expected counts
        if province_count != 81:
            data_status = "degraded"
            data_details["warning"] = f"Expected 81 provinces, found {province_count}"
        else:
            data_details["provinces"] = province_count
            data_details["districts"] = district_count

    except Exception as e:
        logger.error(f"Health check data error: {e}")
        data_status = "error"
        data_details["error"] = str(e)

    # Determine overall status
    overall_status = "ok" if data_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "uptime_seconds": int(uptime_seconds),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": settings.environment,
        "version": settings.app_version,
        "checks": {"data_loader": {"status": data_status, **data_details}},
    }


# Language preference endpoints
@app.get("/api/v1/language")
async def get_language_preference(request: Request):
    """Get current language preference"""
    lang = get_current_language()
    return {"language": lang, "name": get_language_name(lang), "flag": get_language_flag(lang)}


@app.post("/api/v1/language")
async def set_language_preference(request: Request, language: str):
    """Set language preference"""
    from app.i18n import is_valid_language, set_current_language

    if not is_valid_language(language):
        return JSONResponse(
            status_code=400,
            content={"status": "ERROR", "error": f"Unsupported language: {language}", "supported": SUPPORTED_LANGUAGES},
        )

    set_current_language(language)
    return {
        "status": "OK",
        "language": language,
        "name": get_language_name(language),
        "flag": get_language_flag(language),
    }


@app.get("/api/v1/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    languages = [
        {"code": lang, "name": get_language_name(lang), "flag": get_language_flag(lang)} for lang in SUPPORTED_LANGUAGES
    ]
    return {"languages": languages, "default": DEFAULT_LANGUAGE}


@app.get("/api/versions")
async def get_api_versions():
    """
    Get information about supported API versions.

    Returns version information including current, default, and deprecated versions.
    """
    return get_version_info()


app.include_router(provinces.router, prefix="/api/v1", tags=["Provinces"])
app.include_router(districts.router, prefix="/api/v1", tags=["Districts"])
app.include_router(neighborhoods.router, prefix="/api/v1", tags=["Neighborhoods"])
app.include_router(villages.router, prefix="/api/v1", tags=["Villages"])
app.include_router(towns.router, prefix="/api/v1", tags=["Towns"])

setup_scalar_docs(app)


# Multi-language OpenAPI specs using i18n
def get_openapi_for_language(language: str) -> Dict[str, Any]:
    """
    Generate OpenAPI specification for a specific language using i18n system

    Args:
        language: Language code (e.g., 'en', 'tr')

    Returns:
        OpenAPI schema dictionary
    """
    # Load translations for the language
    translations = get_translations(language)

    # Save and clear the cached schema to force regeneration
    cached_schema = app.openapi_schema
    app.openapi_schema = None

    openapi_schema = copy.deepcopy(app.openapi())

    # Apply translations
    openapi_schema["info"]["title"] = translations["api"]["title"]
    openapi_schema["info"]["description"] = translations["api"]["description"]

    # Translate tags
    openapi_schema["tags"] = [
        {
            "name": translations["tags"]["provinces"]["name"],
            "description": translations["tags"]["provinces"]["description"],
        },
        {
            "name": translations["tags"]["districts"]["name"],
            "description": translations["tags"]["districts"]["description"],
        },
        {
            "name": translations["tags"]["neighborhoods"]["name"],
            "description": translations["tags"]["neighborhoods"]["description"],
        },
        {
            "name": translations["tags"]["villages"]["name"],
            "description": translations["tags"]["villages"]["description"],
        },
        {"name": translations["tags"]["towns"]["name"], "description": translations["tags"]["towns"]["description"]},
    ]

    # Tag mapping for path updates (only for non-English languages)
    if language != "en":
        tag_name_map = {
            "Provinces": translations["tags"]["provinces"]["name"],
            "Districts": translations["tags"]["districts"]["name"],
            "Neighborhoods": translations["tags"]["neighborhoods"]["name"],
            "Villages": translations["tags"]["villages"]["name"],
            "Towns": translations["tags"]["towns"]["name"],
        }

        # Update tag references in paths
        for path, methods in openapi_schema.get("paths", {}).items():
            for method, details in methods.items():
                if "tags" in details:
                    details["tags"] = [tag_name_map.get(tag, tag) for tag in details["tags"]]

        # Translate endpoint summaries
        summary_map = {
            # New language API endpoints
            "Root": translations["endpoints"]["root"],
            "Health Check": translations["endpoints"]["health"],
            "Get current language preference": translations["endpoints"]["get_language_preference"],
            "Set language preference": translations["endpoints"]["set_language_preference"],
            "Get list of supported languages": translations["endpoints"]["get_supported_languages"],
            # Province endpoints
            "Get all provinces": translations["endpoints"]["provinces"]["list"],
            "Get province by ID": translations["endpoints"]["provinces"]["get"],
            # District endpoints
            "Get all districts": translations["endpoints"]["districts"]["list"],
            "Get district by ID": translations["endpoints"]["districts"]["get"],
            # Neighborhood endpoints
            "Get all neighborhoods": translations["endpoints"]["neighborhoods"]["list"],
            "Get neighborhood by ID": translations["endpoints"]["neighborhoods"]["get"],
            # Village endpoints
            "Get all villages": translations["endpoints"]["villages"]["list"],
            "Get village by ID": translations["endpoints"]["villages"]["get"],
            # Town endpoints
            "Get all towns": translations["endpoints"]["towns"]["list"],
            "Get town by ID": translations["endpoints"]["towns"]["get"],
        }

        # Parameter description translations
        param_desc_map = {
            # Province parameters
            "The province name": translations["parameter_descriptions"]["province_name"],
            "The minimum population of the province": translations["parameter_descriptions"]["min_population_province"],
            "The maximum population of the province": translations["parameter_descriptions"]["max_population_province"],
            "The minimum area of the province": translations["parameter_descriptions"]["min_area_province"],
            "The maximum area of the province": translations["parameter_descriptions"]["max_area_province"],
            "The minimum altitude of the province": translations["parameter_descriptions"]["min_altitude_province"],
            "The maximum altitude of the province": translations["parameter_descriptions"]["max_altitude_province"],
            "The province is coastal or not": translations["parameter_descriptions"]["is_coastal"],
            "The province is metropolitan or not": translations["parameter_descriptions"]["is_metropolitan"],
            "The province ID / plate number": translations["parameter_descriptions"]["province_id_plate"],
            "Extend the response with additional data (neighborhoods and villages)": translations[
                "parameter_descriptions"
            ]["extend_response"],
            # District parameters
            "The district name": translations["parameter_descriptions"]["district_name"],
            "The minimum population of the district": translations["parameter_descriptions"]["min_population_district"],
            "The maximum population of the district": translations["parameter_descriptions"]["max_population_district"],
            "The minimum area of the district": translations["parameter_descriptions"]["min_area_district"],
            "The maximum area of the district": translations["parameter_descriptions"]["max_area_district"],
            "The district ID": translations["parameter_descriptions"]["district_id"],
            # Neighborhood parameters
            "The neighborhood name": translations["parameter_descriptions"]["neighborhood_name"],
            "The minimum population of the neighborhood": translations["parameter_descriptions"][
                "min_population_neighborhood"
            ],
            "The maximum population of the neighborhood": translations["parameter_descriptions"][
                "max_population_neighborhood"
            ],
            "The neighborhood ID": translations["parameter_descriptions"]["entity_id"],
            # Village parameters
            "The village name": translations["parameter_descriptions"]["village_name"],
            "The minimum population of the village": translations["parameter_descriptions"]["min_population_village"],
            "The maximum population of the village": translations["parameter_descriptions"]["max_population_village"],
            "The village ID": translations["parameter_descriptions"]["entity_id"],
            # Town parameters
            "The town name": translations["parameter_descriptions"]["town_name"],
            "The minimum population of the town": translations["parameter_descriptions"]["min_population_town"],
            "The maximum population of the town": translations["parameter_descriptions"]["max_population_town"],
            "The town ID": translations["parameter_descriptions"]["entity_id"],
            # Common filter parameters
            "The province ID": translations["parameter_descriptions"]["province_id"],
            "Activate postal codes": translations["parameter_descriptions"]["activate_postal_codes"],
            "Filter by postal code": translations["parameter_descriptions"]["postal_code_filter"],
            # Pagination parameters
            "The offset of the provinces list": translations["parameter_descriptions"]["offset_list"],
            "The offset of the districts list": translations["parameter_descriptions"]["offset_list"],
            "The offset of the neighborhoods list": translations["parameter_descriptions"]["offset_list"],
            "The offset of the villages list": translations["parameter_descriptions"]["offset_list"],
            "The offset of the towns list": translations["parameter_descriptions"]["offset_list"],
            "The limit of the provinces list": translations["parameter_descriptions"]["limit_list"],
            "The limit of the districts list": translations["parameter_descriptions"]["limit_list"],
            "The limit of the neighborhoods list": translations["parameter_descriptions"]["limit_list"],
            "The limit of the villages list": translations["parameter_descriptions"]["limit_list"],
            "The limit of the towns list": translations["parameter_descriptions"]["limit_list"],
            # Response formatting parameters
            "The fields to be returned (comma separated)": translations["parameter_descriptions"]["fields_return"],
            "The sorting of the provinces list (put '-' before the field name for descending order)": translations[
                "parameter_descriptions"
            ]["sort_order"],
            "The sorting of the districts list (put '-' before the field name for descending order)": translations[
                "parameter_descriptions"
            ]["sort_order"],
            "The sorting of the neighborhoods list (put '-' before the field name for descending order)": translations[
                "parameter_descriptions"
            ]["sort_order"],
            "The sorting of the villages list (put '-' before the field name for descending order)": translations[
                "parameter_descriptions"
            ]["sort_order"],
            "The sorting of the towns list (put '-' before the field name for descending order)": translations[
                "parameter_descriptions"
            ]["sort_order"],
        }

        # Translate summaries and parameters
        for path, methods in openapi_schema.get("paths", {}).items():
            for method, details in methods.items():
                # Translate summary
                if "summary" in details and details["summary"] in summary_map:
                    details["summary"] = summary_map[details["summary"]]

                # Translate query parameters
                if "parameters" in details:
                    for param in details["parameters"]:
                        if "description" in param and param["description"] in param_desc_map:
                            param["description"] = param_desc_map[param["description"]]

                # Translate request body and responses if needed
                if "responses" in details:
                    for status_code, response in details["responses"].items():
                        if status_code == "200" and "description" in response:
                            response["description"] = translations["responses"]["successful"]
                        elif status_code == "422" and "description" in response:
                            response["description"] = translations["responses"]["validation_error"]

        # Translate model schemas
        if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
            schemas = openapi_schema["components"]["schemas"]
            if "HTTPValidationError" in schemas:
                schemas["HTTPValidationError"]["title"] = translations["models"]["http_validation_error"]
            if "ValidationError" in schemas:
                schemas["ValidationError"]["title"] = translations["models"]["validation_error"]

    # Restore cached schema
    app.openapi_schema = cached_schema

    return openapi_schema


@app.get("/openapi-{lang}.json", include_in_schema=False)
async def get_openapi_language_endpoint(lang: str):
    """
    Get OpenAPI specification for a specific language

    Supports: en, tr (and future languages)
    """
    # Validate language, fallback to 'en' if not supported
    supported_languages = ["en", "tr"]
    if lang not in supported_languages:
        lang = "en"

    return get_openapi_for_language(lang)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors with i18n support"""
    # Use language from context (set by middleware)
    lang = get_current_language()
    translations = get_translations(lang)

    return JSONResponse(status_code=404, content={"status": "ERROR", "error": translations["errors"]["not_found"]})


@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc):
    """Handle 405 errors with i18n support"""
    # Use language from context (set by middleware)
    lang = get_current_language()
    translations = get_translations(lang)

    return JSONResponse(
        status_code=405, content={"status": "ERROR", "error": translations["errors"]["method_not_allowed"]}
    )
