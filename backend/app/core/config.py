import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development")
    PORT: int = Field(default=8000)
    HOST: str = Field(default="0.0.0.0")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"]
    )

    # Groq API Configuration
    GROQ_API_KEY: str = Field(default="")
    GROQ_MODEL_SMALL: str = Field(default="llama-3.1-8b-instant")
    GROQ_MODEL_LARGE: str = Field(default="llama-3.3-70b-versatile")

    # Upstash Redis / In-memory Fallback
    UPSTASH_REDIS_REST_URL: str = Field(default="")
    UPSTASH_REDIS_REST_TOKEN: str = Field(default="")
    REDIS_URL: str = Field(default="")
    MAX_REQUESTS_PER_MINUTE: int = Field(default=30)

    # Supabase Configuration
    SUPABASE_URL: str = Field(default="")
    SUPABASE_KEY: str = Field(default="")

    # 2024 Legal Mandate
    LEGAL_YEAR_ENFORCED: int = Field(default=2024)
    REJECT_REPEALED_IPC: bool = Field(default=True)

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
