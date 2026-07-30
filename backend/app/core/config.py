from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SwasthiQ EOD Billing API"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str

    GEMINI_API_KEY: str
    
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()