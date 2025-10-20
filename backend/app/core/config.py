from functools import lru_cache
from typing import Literal, Sequence

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "H-Life API"
    environment: Literal["local", "staging", "production"] = "local"
    api_prefix: str = "/api"

    database_url: AnyUrl = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/h_life"
    )

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

    allowed_origins: Sequence[str] = ("*",)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
