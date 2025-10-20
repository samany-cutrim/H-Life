from functools import lru_cache
from typing import Literal, Sequence

from pydantic import AnyUrl, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "H-Life API"
    environment: Literal["local", "staging", "production"] = "local"
    api_prefix: str = "/api"
    log_level: str = "INFO"

    database_url: AnyUrl = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/h_life"
    )
    redis_url: AnyUrl | None = Field(default=None)

    s3_endpoint_url: AnyUrl | None = None
    s3_region: str = "us-east-1"
    s3_bucket: str = "h-life-media"
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    s3_use_ssl: bool = True

    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 30
    jwt_refresh_expire_minutes: int = 60 * 24 * 7

    allowed_origins: Sequence[str] = ("http://localhost:3000", "http://127.0.0.1:3000")
    allowed_origin_regex: str | None = r"http://192\.168\.\d{1,3}\.\d{1,3}(:\d+)?"

    ai_provider: Literal["openai", "local"] = "openai"
    openai_api_key: str | None = None
    local_ai_endpoint: AnyUrl | None = None
    ai_timeout_seconds: int = 15

    vapid_public_key: str | None = None
    vapid_private_key: str | None = None
    fcm_server_key: str | None = None

    rate_limit_window_seconds: int = 60
    rate_limit_max_requests: int = 5

    sentry_dsn: AnyUrl | None = None
    prometheus_multiproc_dir: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: str | Sequence[str]) -> Sequence[str]:
        if isinstance(value, str):
            return tuple(filter(None, (origin.strip() for origin in value.split(","))))
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
