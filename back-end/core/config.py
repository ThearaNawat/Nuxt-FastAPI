
import os
from typing import List, Optional


from pydantic import field_validator
from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "123456"
    POSTGRES_HOST: str = "postgres-service"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "erp_db"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    
    @property
    def database_url(self) -> str:
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        database_url,
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis-service:6379/0")

    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-very-long-secret-key-min-32-characters-here"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False
    # API
    API_TITLE: str = "ERP System API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Enterprise Resource Planning System API"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        return str(value).strip().lower() in {"1", "true", "yes", "on"}
        
settings = Setting()
