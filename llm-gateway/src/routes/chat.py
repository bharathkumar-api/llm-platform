from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal, Dict, Any, Optional
from ..services.llm_client import call_llm

router = APIRouter(prefix="/llm", tags=["llm"])

Role = Literal["user", "assistant", "system"]

class ChatMessage(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    system_prompt: Optional[str] = None
    provider: Optional[Literal["openai", "anthropic"]] = None

class ChatResponse(BaseModel):
    provider: str
    model: str
    message: str | None = None
    error: str | None = None

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result: Dict[str, Any] = call_llm(
        messages=[m.model_dump() for m in req.messages],
        system_prompt=req.system_prompt,
        provider=req.provider,
    )
    return ChatResponse(
        provider=result.get("provider", ""),
        model=result.get("model", ""),
        message=result.get("message"),
        error=result.get("error"),
    )
