from app.llm.client import (
    DEFAULT_GEMINI_API_KEY,
    DEFAULT_GEMINI_MODEL,
    DEFAULT_GROQ_API_KEY,
    DEFAULT_GROQ_MODEL,
    BaseLLM,
    GeminiLLM,
    GroqLLM,
)


class LLMFactory:
    @staticmethod
    def create(
        provider: str,
        api_key: str | None,
        model: str | None,
    ) -> BaseLLM:
        if provider == "gemini":
            return GeminiLLM(
                api_key or DEFAULT_GEMINI_API_KEY, model or DEFAULT_GEMINI_MODEL
            )

        if provider == "groq":
            return GroqLLM(api_key or DEFAULT_GROQ_API_KEY, model or DEFAULT_GROQ_MODEL)

        raise ValueError("Unsupported provider")
