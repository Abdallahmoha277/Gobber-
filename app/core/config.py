from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Gobber"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str

    REDIS_URL: str

    DEEPSEEK_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
