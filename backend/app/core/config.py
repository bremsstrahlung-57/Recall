from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    qdrant_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
