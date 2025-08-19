from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    # MongoDB
    mongodb_connect_uri: str
    database_name: str = "ultimate_library"
    
    # JWT Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Ultimate Library API"
    version: str = "1.0.0"
    description: str = "A FastAPI application for managing books and users"
    
    # Environment
    environment: str = "development"
    port: int = 8000

settings = Settings()
