from fastapi import FastAPI
from .routes import agent
from .core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "agent-service"}

app.include_router(agent.router)
