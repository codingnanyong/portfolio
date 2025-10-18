"""
Application configuration management
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings"""
    
    # Application settings
    app_name: str = "Realtime Service"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/schema")
    
    # External service URLs
    location_service_url: str = os.getenv("LOCATION_SERVICE_URL", "http://location-service:80")
    thresholds_service_url: str = os.getenv("THRESHOLDS_SERVICE_URL", "http://thresholds-service:80")
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    # Logging settings
    log_level: str = "INFO"
    
    # Environment
    environment: str = "development"
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


# Global settings instance
settings = Settings()