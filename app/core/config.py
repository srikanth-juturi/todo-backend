from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    APP_NAME: str = "Todo Backend"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = (
        "mssql+pyodbc://@localhost/todo"
        "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"
    )
    SQL_ECHO: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
