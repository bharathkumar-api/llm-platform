from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "LLM Gateway"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

    PROVIDER_PRIORITY: list[str] = ["groq"]

@lru_cache
def get_settings() -> Settings:
    return Settings()
