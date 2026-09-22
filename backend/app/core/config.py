import json
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    NyayaMitra Application Settings.

    CORS_ORIGINS is stored as a plain string to avoid pydantic-settings
    calling json.loads() on it before any validator runs (which causes
    JSONDecodeError when the value is not a JSON array).

    Use the `cors_origins_list` property wherever a List[str] is needed.
    Supported formats in the environment variable:
      - Single URL:               http://localhost:3000
      - Comma-separated URLs:     http://localhost:3000,https://app.vercel.app
      - JSON array string:        ["http://localhost:3000","https://app.vercel.app"]
      - Wildcard:                 *
      - Empty / unset:            (defaults to "*" = allow all)
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENVIRONMENT: str = Field(default="development")
    PORT: int = Field(default=8000)
    HOST: str = Field(default="0.0.0.0")

    # Stored as str so pydantic-settings never attempts json.loads() on it.
    # Parse it via the `cors_origins_list` property below.
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS_ORIGINS as a parsed list of strings."""
        raw = (self.CORS_ORIGINS or "").strip()
        if not raw:
            return ["*"]
        # JSON array format: ["https://a.com","https://b.com"]
        if raw.startswith("[") and raw.endswith("]"):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return [str(o).strip() for o in parsed if str(o).strip()]
            except Exception:
                pass
        # Comma-separated or single value
        return [o.strip() for o in raw.split(",") if o.strip()]

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
