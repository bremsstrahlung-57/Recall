from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"

    gemini_api_key: str | None = None
    groq_api_key: str | None = None

    gemini_model: str = "gemini-2.5-flash"
    groq_model: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
