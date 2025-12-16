"""
i18n Localization Loader
Loads and caches translation files for multi-language support
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import Request

# Cache for loaded translations
_translations_cache: Dict[str, Dict[str, Any]] = {}

# Supported languages
SUPPORTED_LANGUAGES = ["en", "tr"]
DEFAULT_LANGUAGE = "en"


def get_locales_path() -> Path:
    """Get the path to the locales directory"""
    current_file = Path(__file__)
    locales_dir = current_file.parent.parent / "locales"
    return locales_dir


def load_translation_file(language: str) -> Dict[str, Any]:
    """Load a translation file from disk"""
    locales_path = get_locales_path()
    file_path = locales_path / f"{language}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Translation file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_translations(language: str) -> Dict[str, Any]:
    """
    Get translations for a specific language with caching

    Args:
        language: Language code (e.g., 'en', 'tr')

    Returns:
        Dictionary containing all translations for the language
    """
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    # Check cache first
    if language in _translations_cache:
        return _translations_cache[language]

    # Load from file and cache
    try:
        translations = load_translation_file(language)
        _translations_cache[language] = translations
        return translations
    except FileNotFoundError:
        # Fallback to default language
        if language != DEFAULT_LANGUAGE:
            return get_translations(DEFAULT_LANGUAGE)
        raise


def get_lang_content(language: str) -> Dict[str, Any]:
    """
    Alias for get_translations for compatibility

    Args:
        language: Language code (e.g., 'en', 'tr')

    Returns:
        Dictionary containing all translations for the language
    """
    return get_translations(language)


def detect_language(request: Request, header_name: str = "accept-language") -> str:
    """
    Detect language from HTTP headers

    Supports both 'Accept-Language' and custom 'X-Language' headers

    Args:
        request: FastAPI Request object
        header_name: Header to check (default: 'accept-language')

    Returns:
        Detected language code (defaults to 'en' if not found)
    """
    # Check custom X-Language header first
    x_language = request.headers.get("x-language", "").lower()
    if x_language in SUPPORTED_LANGUAGES:
        return x_language

    # Check Accept-Language header
    accept_language = request.headers.get(header_name, "").lower()

    # Simple language detection
    for lang in SUPPORTED_LANGUAGES:
        if lang in accept_language:
            return lang

    return DEFAULT_LANGUAGE


def get_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    Get a nested value from dictionary using dot notation

    Example:
        get_nested_value(data, "api.title") -> data["api"]["title"]

    Args:
        data: Dictionary to search
        path: Dot-separated path (e.g., "api.title")
        default: Default value if path not found

    Returns:
        Value at path or default
    """
    keys = path.split(".")
    value = data

    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


def translate(language: str, key: str, default: Optional[str] = None) -> str:
    """
    Translate a specific key

    Args:
        language: Language code
        key: Translation key (supports dot notation, e.g., "api.title")
        default: Default value if key not found

    Returns:
        Translated string
    """
    translations = get_translations(language)
    return get_nested_value(translations, key, default or key)


def clear_cache():
    """Clear the translations cache (useful for development/testing)"""
    global _translations_cache
    _translations_cache.clear()
