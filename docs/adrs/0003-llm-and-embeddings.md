# ADR 0003: LLMs and Embeddings

## Context
We need OSS-friendly LLMs/embeddings for generation and retrieval.

## Decision
- Models: Qwen2.5-Instruct, DeepSeek-Coder (where code reasoning helps), Mistral/Mixtral (license permitting)
- Embeddings: e5-large-v2 or bge-large-en-v1.5

## Status
Accepted (MVP). Verify per-model license constraints for commercial use.

## Consequences
- Use vLLM/TGI/Ollama for serving; SentenceTransformers for embeddings

