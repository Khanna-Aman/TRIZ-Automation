# Product Requirements (Initial)

## Functional
- Accept a problem statement and produce ranked solution ideas
- Support structured TRIZ resolution and lateral thinking generation
- Provide evaluation metrics and traces for transparency
- Enable optional RAG ingestion for context

## Non-Functional
- Local MVP runs on Docker Compose
- Latency: initial end-to-end < 10s on stub services
- Availability: best-effort in dev; plan for >= 99.5% in prod
- Observability: basic metrics; traces planned

## Constraints
- Prefer OSS components; note license nuances for n8n and Redis

