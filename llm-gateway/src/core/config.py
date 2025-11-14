from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "LLM Gateway"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

    PROVIDER_PRIORITY: list[str] = ["openai", "anthropic"]

@lru_cache
def get_settings() -> Settings:
    return Settings()
