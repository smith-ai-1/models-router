"""Domain exceptions for model router."""


class ModelRouterException(Exception):
    """Base exception for model router."""
    pass


class ProviderNotFoundError(ModelRouterException):
    """Raised when a provider is not found for a model."""
    pass


class ProviderNotConfiguredError(ModelRouterException):
    """Raised when a provider is not configured."""
    pass


class ModelNotSupportedError(ModelRouterException):
    """Raised when a model is not supported by a provider."""
    pass


class ProviderAPIError(ModelRouterException):
    """Raised when a provider API returns an error."""
    pass