import json
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENVIRONMENT: str = Field(default="development")
    PORT: int = Field(default=8000)
    HOST: str = Field(default="0.0.0.0")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "*"]
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v_trimmed = v.strip()
            if not v_trimmed:
                return ["*"]
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                try:
                    parsed = json.loads(v_trimmed)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
            return [i.strip() for i in v_trimmed.split(",") if i.strip()]
        return ["*"]

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


settings = Settings()

