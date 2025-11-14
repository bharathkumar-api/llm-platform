from __future__ import annotations
from typing import Literal, Any, Dict, List
from openai import OpenAI
from anthropic import Anthropic
from ..core.config import get_settings

settings = get_settings()

Provider = Literal["openai", "anthropic"]

def _choose_provider() -> Provider | None:
    for p in settings.PROVIDER_PRIORITY:
        if p == "openai" and settings.OPENAI_API_KEY:
            return "openai"
        if p == "anthropic" and settings.ANTHROPIC_API_KEY:
            return "anthropic"
    return None

def call_llm(
    messages: List[Dict[str, str]],
    system_prompt: str | None = None,
    provider: Provider | None = None,
) -> Dict[str, Any]:
    provider = provider or _choose_provider()
    if provider is None:
        return {"error": "No LLM provider configured"}

    if provider == "openai":
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        resp = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=full_messages,
        )
        content = resp.choices[0].message.content
        text = "".join([c.text for c in content]) if isinstance(content, list) else content
        return {
            "provider": "openai",
            "model": settings.OPENAI_MODEL,
            "message": text,
        }

    if provider == "anthropic":
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        conv: List[dict] = []
        if system_prompt:
            conv.append({"role": "user", "content": system_prompt})
        conv.extend(messages)
        resp = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            messages=conv,
            max_tokens=512,
        )
        return {
            "provider": "anthropic",
            "model": settings.ANTHROPIC_MODEL,
            "message": resp.content[0].text,
        }

    return {"error": f"Unknown provider {provider}"}
