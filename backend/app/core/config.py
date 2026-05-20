from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AMIS DynaFlow MVP API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    debug: bool = True

    database_url: str = "postgresql://placeholder:placeholder@localhost:5432/amis_dynaflow"
    redis_url: str = "redis://localhost:6379/0"
    artifact_base_path: str = "results/"

    jwt_secret_key: str = "unsafe-dev-placeholder"
    jwt_algorithm: str = "HS256"
    jwt_expires_in_seconds: int = 3600

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
