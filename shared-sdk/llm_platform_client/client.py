from __future__ import annotations
from pydantic import BaseModel
import httpx

class LLMConfig(BaseModel):
  base_url: str

class LLMClient:
  def __init__(self, base_url: str):
      self.config = LLMConfig(base_url=base_url.rstrip("/"))

  async def chat(self, question: str) -> str:
      async with httpx.AsyncClient(timeout=60) as client:
          resp = await client.post(
              f"{self.config.base_url}/llm/chat",
              json={
                  "messages": [{"role": "user", "content": question}],
                  "system_prompt": "You are a helpful assistant for a healthcare & SRE platform."
              },
          )
          resp.raise_for_status()
          data = resp.json()
      return data.get("message", "")
