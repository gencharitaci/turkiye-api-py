"""
Language Context Manager
Thread-safe language context for request-scoped language access
"""
from contextvars import ContextVar
from typing import Optional

from app.i18n.loader import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

# Context variable for current language (thread-safe)
_current_language: ContextVar[str] = ContextVar("current_language", default=DEFAULT_LANGUAGE)


def get_current_language() -> str:
    """
    Get the current language for the active request

    Returns:
        Current language code (defaults to DEFAULT_LANGUAGE)
    """
    return _current_language.get()


def set_current_language(language: str) -> None:
    """
    Set the current language for the active request

    Args:
        language: Language code to set
    """
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    _current_language.set(language)


class LanguageContext:
    """
    Context manager for temporary language changes

    Usage:
        with LanguageContext("tr"):
            # Code here uses Turkish
            translations = get_translations(get_current_language())
    """

    def __init__(self, language: str):
        """
        Initialize language context

        Args:
            language: Language code to use in this context
        """
        self.language = language
        self.previous_language: Optional[str] = None

    def __enter__(self):
        """Enter the context and set language"""
        self.previous_language = get_current_language()
        set_current_language(self.language)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and restore previous language"""
        if self.previous_language:
            set_current_language(self.previous_language)


def reset_language_context():
    """
    Reset language context to default
    Useful for testing and cleanup
    """
    _current_language.set(DEFAULT_LANGUAGE)
