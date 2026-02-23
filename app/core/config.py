from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    APP_NAME: str = "Todo Backend"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = (
        "mssql+pyodbc://sa:YourStrong!Passw0rd@localhost%5CSQLEXPRESS/todo_db"
        "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
    SQL_ECHO: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
