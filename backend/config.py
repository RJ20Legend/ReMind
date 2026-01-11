import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./remind.db')
    OPENAI_API_KEY: str | None = None

settings = Settings()
