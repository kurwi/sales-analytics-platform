"""
Configuration management for Sales Analytics Platform.

This module centralizes all configuration parameters, environment variables,
and system settings for the analytics platform.
"""
import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    database: str = os.getenv("DB_NAME", "sales_analytics")
    username: str = os.getenv("DB_USER", "analytics_user")
    password: str = os.getenv("DB_PASSWORD", "")
    connection_pool_size: int = 10
    connection_timeout: int = 30

@dataclass
class APIConfig:
    """External API configuration."""
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_temperature: float = 0.2
    openai_max_tokens: int = 400
    api_rate_limit: int = 100  # requests per minute

@dataclass
class DashboardConfig:
    """Dashboard application configuration."""
    host: str = os.getenv("DASH_HOST", "0.0.0.0")
    port: int = int(os.getenv("DASH_PORT", "8050"))
    debug: bool = os.getenv("DASH_DEBUG", "False").lower() == "true"
    title: str = "Sales Analytics Platform"
    update_interval: int = 5000  # milliseconds
    
@dataclass
class StreamingConfig:
    """Real-time streaming configuration."""
    socketio_host: str = os.getenv("SOCKETIO_HOST", "0.0.0.0")
    socketio_port: int = int(os.getenv("SOCKETIO_PORT", "8001"))
    event_queue_size: int = 1000
    broadcast_interval: int = 5  # seconds
    ping_timeout: int = 60
    ping_interval: int = 25

@dataclass
class MLConfig:
    """Machine learning model configuration."""
    model_path: str = "models/"
    random_state: int = 42
    test_size: float = 0.2
    cross_validation_folds: int = 5
    n_estimators: int = 100
    max_depth: int = 10
    feature_importance_threshold: float = 0.01

@dataclass
class DataConfig:
    """Data processing configuration."""
    data_path: str = "data/"
    raw_data_path: str = "data/raw/"
    processed_data_path: str = "data/processed/"
    max_file_size_mb: int = 500
    date_format: str = "%Y-%m-%d"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = "logs/application.log"
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5

@dataclass
class SecurityConfig:
    """Security and authentication configuration."""
    secret_key: str = os.getenv("SECRET_KEY", "change-this-in-production")
    jwt_expiration_hours: int = 24
    password_min_length: int = 8
    enable_ssl: bool = os.getenv("ENABLE_SSL", "False").lower() == "true"
    ssl_cert_path: Optional[str] = os.getenv("SSL_CERT_PATH")
    ssl_key_path: Optional[str] = os.getenv("SSL_KEY_PATH")

class Config:
    """
    Main configuration class aggregating all config sections.
    
    Usage:
        config = Config()
        api_key = config.api.openai_api_key
        port = config.dashboard.port
    """
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.dashboard = DashboardConfig()
        self.streaming = StreamingConfig()
        self.ml = MLConfig()
        self.data = DataConfig()
        self.logging = LoggingConfig()
        self.security = SecurityConfig()
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create required directories if they don't exist."""
        directories = [
            self.ml.model_path,
            self.data.data_path,
            self.data.raw_data_path,
            self.data.processed_data_path,
            Path(self.logging.file_path).parent if self.logging.file_path else None
        ]
        
        for directory in directories:
            if directory:
                Path(directory).mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> bool:
        """
        Validate critical configuration parameters.
        
        Returns:
            bool: True if configuration is valid
        
        Raises:
            ValueError: If critical configuration is invalid
        """
        if self.security.secret_key == "change-this-in-production":
            raise ValueError("SECRET_KEY must be changed in production environment")
        
        if self.security.enable_ssl and (not self.security.ssl_cert_path or not self.security.ssl_key_path):
            raise ValueError("SSL enabled but certificate paths not configured")
        
        return True
    
    def to_dict(self) -> dict:
        """
        Export configuration as dictionary (excludes sensitive data).
        
        Returns:
            dict: Configuration dictionary
        """
        return {
            "dashboard": {
                "host": self.dashboard.host,
                "port": self.dashboard.port,
                "title": self.dashboard.title
            },
            "streaming": {
                "port": self.streaming.socketio_port,
                "broadcast_interval": self.streaming.broadcast_interval
            },
            "ml": {
                "random_state": self.ml.random_state,
                "n_estimators": self.ml.n_estimators
            },
            "api": {
                "model": self.api.openai_model,
                "temperature": self.api.openai_temperature
            }
        }

# Global configuration instance
config = Config()
