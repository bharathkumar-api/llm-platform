from fastapi import FastAPI
from .routes import chat
from .core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "llm-gateway"}

app.include_router(chat.router)
