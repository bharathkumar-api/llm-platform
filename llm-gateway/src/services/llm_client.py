from __future__ import annotations
from typing import Literal, Any, Dict, List
from groq import Groq
from ..core.config import get_settings

settings = get_settings()

Provider = Literal["groq"]

def _choose_provider() -> Provider | None:
    for p in settings.PROVIDER_PRIORITY:
        if p == "groq" and settings.GROQ_API_KEY:
            return "groq"
    return None

def call_llm(
    messages: List[Dict[str, str]],
    system_prompt: str | None = None,
    provider: Provider | None = None,
) -> Dict[str, Any]:
    provider = provider or _choose_provider()
    if provider is None:
        return {"error": "No LLM provider configured"}

    if provider == "groq":
        client = Groq(api_key=settings.GROQ_API_KEY)
        full_messages: List[Dict[str, str]] = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        resp = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=full_messages,
        )
        content = resp.choices[0].message.content
        if isinstance(content, list):
            text = "".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in content])
        else:
            text = content
        return {
            "provider": "groq",
            "model": settings.GROQ_MODEL,
            "message": text,
        }

    return {"error": f"Unknown provider {provider}"}
