from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Optional full database URL (e.g. sqlite+pysqlite:///:memory:)
    DATABASE_URL: str | None = None

    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MIDTRANS_SERVER_KEY: str | None = None
    MIDTRANS_CLIENT_KEY: str | None = None
    MIDTRANS_ENVIRONMENT: str = "sandbox"
    MIDTRANS_BASE: str | None = None
    PAYMENT_WEBHOOK_SECRET: str | None = None
    EMAIL_SYSTEM: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()