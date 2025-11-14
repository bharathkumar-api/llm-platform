from fastapi import APIRouter
from pydantic import BaseModel
import httpx
from ..core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/agent", tags=["agent"])

class AgentChatRequest(BaseModel):
    question: str

class AgentChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=AgentChatResponse)
async def chat(req: AgentChatRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{settings.LLM_GATEWAY_URL}/llm/chat",
            json={
                "system_prompt": "You are a helpful assistant for a healthcare & SRE platform.",
                "messages": [{"role": "user", "content": req.question}],
            },
        )
        data = resp.json()
    return AgentChatResponse(answer=data.get("message", ""))
