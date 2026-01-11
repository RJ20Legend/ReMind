import os

class AIService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 768 for _ in texts]
