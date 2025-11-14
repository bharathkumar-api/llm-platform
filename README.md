# LLM Platform (Reusable, Production-Oriented)

This repo is a reusable LLM backend that multiple applications can integrate with.

## Structure

- llm-gateway/   → FastAPI service exposing unified LLM + RAG APIs
- agent-service/ → Domain-specific agents (RCA/chatbot, etc.) that call llm-gateway
- shared-sdk/    → Python client package used by other repos
- vector-store/  → Config + notes for Chroma / Pinecone
- infra/         → docker-compose + env for local/dev

Every app (healthcare, RCA, future apps) can call llm-gateway HTTP APIs
or import `shared-sdk` to talk to the platform.
