from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    app_name: str = "PostProber"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./data/postprober.db"

    # Security
    secret_key: str = "your-super-secret-jwt-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # OpenAI
    openai_api_key: Optional[str] = None

    # Social Media APIs
    twitter_client_id: Optional[str] = None
    twitter_client_secret: Optional[str] = None
    linkedin_client_id: Optional[str] = None
    linkedin_client_secret: Optional[str] = None
    instagram_client_id: Optional[str] = None
    instagram_client_secret: Optional[str] = None

    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_pass: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()