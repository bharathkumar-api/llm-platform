from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "Agent Service"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    LLM_GATEWAY_URL: str = os.getenv("LLM_GATEWAY_URL", "http://llm-gateway:9000")

@lru_cache
def get_settings() -> Settings:
    return Settings()
