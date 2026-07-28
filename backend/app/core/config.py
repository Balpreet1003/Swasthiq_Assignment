from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SwasthiQ EOD Billing API"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str

    OPENAI_API_KEY: str

    MODEL: str = "gpt-5.5"

    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()