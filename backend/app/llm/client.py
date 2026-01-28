from abc import ABC, abstractmethod

from google import genai
from google.genai import types
from groq import Groq

from app.core.settings import Settings

settings = Settings()
DEFAULT_GEMINI_API_KEY = settings.gemini_api_key
DEFAULT_GEMINI_MODEL = settings.gemini_model
DEFAULT_GROQ_API_KEY = settings.groq_api_key
DEFAULT_GROQ_MODEL = settings.groq_model


def create_gemini_client(api_key: str):
    return genai.Client(api_key=api_key)


def create_groq_client(api_key: str):
    return Groq(api_key=api_key)


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str | None:
        pass


class GeminiLLM(BaseLLM):
    def __init__(self, api_key: str, model: str):
        self.client = create_gemini_client(api_key)
        self.model = model

    def generate(self, prompt: str) -> str | None:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="""You are a retrieval grounded assistant.
You must answer only using the provided context.
The context comes from user owned documents retrieved via semantic search.
Rules:
Do not use outside knowledge.
Do not guess or fill gaps.
If the context is insufficient, say so explicitly.
Prefer factual, grounded answers.
If multiple documents disagree, mention the disagreement.
Cite evidence implicitly by phrasing, not by adding references.
Do not mention embeddings, vector databases, or chunking.
Your goal is to produce a clear, concise, and accurate answer grounded strictly in the context.""",
            ),
        )
        return response.text


class GroqLLM(BaseLLM):
    def __init__(self, api_key: str, model: str):
        self.client = create_groq_client(api_key)
        self.model = model

    def generate(self, prompt: str) -> str | None:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a retrieval grounded assistant.
You must answer only using the provided context.
The context comes from user owned documents retrieved via semantic search.
Rules:
Do not use outside knowledge.
Do not guess or fill gaps.
If the context is insufficient, say so explicitly.
Prefer factual, grounded answers.
If multiple documents disagree, mention the disagreement.
Cite evidence implicitly by phrasing, not by adding references.
Do not mention embeddings, vector databases, or chunking.
Your goal is to produce a clear, concise, and accurate answer grounded strictly in the context.""",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content
