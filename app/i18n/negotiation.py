"""
Language Negotiation Utilities
Advanced language negotiation and validation for enterprise i18n support
"""
import re
from typing import List, Optional, Tuple

from app.i18n.loader import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


def parse_accept_language(accept_language: str) -> List[Tuple[str, float]]:
    """
    Parse Accept-Language header with quality values

    Example: "en-US,en;q=0.9,tr;q=0.8" -> [("en-US", 1.0), ("en", 0.9), ("tr", 0.8)]

    Args:
        accept_language: Accept-Language header value

    Returns:
        List of (language, quality) tuples sorted by quality (highest first)
    """
    if not accept_language:
        return []

    languages = []

    # Split by comma and process each language
    for lang_part in accept_language.split(","):
        lang_part = lang_part.strip()

        # Check for quality value
        if ";q=" in lang_part:
            lang, quality = lang_part.split(";q=")
            try:
                quality = float(quality)
            except ValueError:
                quality = 1.0
        else:
            lang = lang_part
            quality = 1.0

        # Extract base language code (e.g., "en-US" -> "en")
        lang = lang.strip().lower()
        base_lang = lang.split("-")[0]

        languages.append((base_lang, quality))

    # Sort by quality (highest first)
    languages.sort(key=lambda x: x[1], reverse=True)

    return languages


def negotiate_language(
    accept_language: str, supported_languages: List[str] = None, default_language: str = None
) -> str:
    """
    Negotiate best language match from Accept-Language header

    Args:
        accept_language: Accept-Language header value
        supported_languages: List of supported language codes (defaults to SUPPORTED_LANGUAGES)
        default_language: Default language if no match found (defaults to DEFAULT_LANGUAGE)

    Returns:
        Best matching language code
    """
    if supported_languages is None:
        supported_languages = SUPPORTED_LANGUAGES

    if default_language is None:
        default_language = DEFAULT_LANGUAGE

    # Parse the Accept-Language header
    requested_languages = parse_accept_language(accept_language)

    # Find first match
    for lang, _ in requested_languages:
        if lang in supported_languages:
            return lang

    # No match found, return default
    return default_language


def extract_language_from_path(path: str) -> Optional[str]:
    """
    Extract language code from URL path

    Supports patterns like:
    - /docs/en
    - /docs/tr
    - /api/v1/en/provinces

    Args:
        path: URL path

    Returns:
        Language code if found, None otherwise
    """
    # Pattern to match language codes in common positions
    patterns = [
        r"^/docs/([a-z]{2})(?:/|$)",  # /docs/en or /docs/en/
        r"^/api/v\d+/([a-z]{2})(?:/|$)",  # /api/v1/en/
        r"/([a-z]{2})(?:/|$)",  # Generic /en/ pattern
    ]

    for pattern in patterns:
        match = re.search(pattern, path)
        if match:
            lang = match.group(1)
            if is_valid_language(lang):
                return lang

    return None


def is_valid_language(language: str, supported_languages: List[str] = None) -> bool:
    """
    Validate if a language code is supported

    Args:
        language: Language code to validate
        supported_languages: List of supported languages (defaults to SUPPORTED_LANGUAGES)

    Returns:
        True if language is supported, False otherwise
    """
    if supported_languages is None:
        supported_languages = SUPPORTED_LANGUAGES

    return language in supported_languages


def normalize_language_code(language: str) -> str:
    """
    Normalize language code to lowercase base code

    Examples:
    - "en-US" -> "en"
    - "TR" -> "tr"
    - "en_GB" -> "en"

    Args:
        language: Language code to normalize

    Returns:
        Normalized language code
    """
    if not language:
        return DEFAULT_LANGUAGE

    # Convert to lowercase and extract base code
    language = language.lower()
    language = language.split("-")[0]  # Handle en-US
    language = language.split("_")[0]  # Handle en_GB

    return language if is_valid_language(language) else DEFAULT_LANGUAGE


def get_language_name(language: str) -> str:
    """
    Get human-readable name for a language code

    Args:
        language: Language code

    Returns:
        Human-readable language name
    """
    language_names = {
        "en": "English",
        "tr": "Türkçe",
        "de": "Deutsch",
        "fr": "Français",
        "es": "Español",
        "ar": "العربية",
    }

    return language_names.get(language, language.upper())


def get_language_flag(language: str) -> str:
    """
    Get flag emoji for a language code

    Args:
        language: Language code

    Returns:
        Flag emoji
    """
    language_flags = {
        "en": "🇬🇧",
        "tr": "🇹🇷",
        "de": "🇩🇪",
        "fr": "🇫🇷",
        "es": "🇪🇸",
        "ar": "🇸🇦",
    }

    return language_flags.get(language, "🌐")
