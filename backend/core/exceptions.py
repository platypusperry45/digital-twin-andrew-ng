"""
Global exceptions.
"""


class ApplicationException(Exception):
    """Base application exception."""


class ConfigurationError(ApplicationException):
    """Configuration failed."""


class DependencyError(ApplicationException):
    """Dependency missing."""


class ProviderError(ApplicationException):
    """LLM provider failed."""