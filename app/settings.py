from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database settings
    database_url: str
    secret_key: str
    test_database_url: str | None = None
    # DB_HOST: str
    # DB_PORT: int
    # DB_NAME: str
    # DB_USER


settings = Settings()
