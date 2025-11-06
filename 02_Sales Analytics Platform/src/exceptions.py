"""
Custom exception classes for Sales Analytics Platform.

This module defines domain-specific exceptions for better error handling
and troubleshooting across the platform.
"""

class SalesAnalyticsException(Exception):
    """Base exception for all platform-specific errors."""
    pass

class DataValidationError(SalesAnalyticsException):
    """Raised when data fails validation checks."""
    def __init__(self, message: str, validation_errors: list = None):
        super().__init__(message)
        self.validation_errors = validation_errors or []

class DataLoadError(SalesAnalyticsException):
    """Raised when data loading fails."""
    pass

class ModelTrainingError(SalesAnalyticsException):
    """Raised when ML model training fails."""
    def __init__(self, message: str, model_name: str = None):
        super().__init__(message)
        self.model_name = model_name

class ModelPredictionError(SalesAnalyticsException):
    """Raised when model prediction fails."""
    pass

class APIConnectionError(SalesAnalyticsException):
    """Raised when external API connection fails."""
    def __init__(self, message: str, api_name: str = None, status_code: int = None):
        super().__init__(message)
        self.api_name = api_name
        self.status_code = status_code

class ConfigurationError(SalesAnalyticsException):
    """Raised when configuration is invalid or missing."""
    pass

class AuthenticationError(SalesAnalyticsException):
    """Raised when authentication fails."""
    pass

class AuthorizationError(SalesAnalyticsException):
    """Raised when user lacks required permissions."""
    def __init__(self, message: str, required_role: str = None):
        super().__init__(message)
        self.required_role = required_role

class StreamingConnectionError(SalesAnalyticsException):
    """Raised when real-time streaming connection fails."""
    pass

class FeatureEngineeringError(SalesAnalyticsException):
    """Raised when feature engineering fails."""
    pass

class DashboardRenderError(SalesAnalyticsException):
    """Raised when dashboard rendering fails."""
    pass
