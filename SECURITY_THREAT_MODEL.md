# Threat Model (High-Level STRIDE)

## Assets
- Problem statements, generated ideas, evaluation metrics
- TRIZ matrix data, RAG-Graph knowledge store
- Credentials and API keys

## Actors
- Authenticated users (future SSO)
- Anonymous callers (dev)
- External data sources (web, wiki, patents)

## Entry Points
- Orchestrator API, n8n webhooks
- Internal service APIs (TRIZ, Lateral, RAG, Eval)

## STRIDE
- Spoofing: Add SSO (Keycloak) and API keys; mTLS internally (prod)
- Tampering: Validate inputs, use JSON schemas, apply WAF/limits at gateway; DB RBAC
- Repudiation: Structured logging, request IDs, audit trails
- Information Disclosure: TLS; secrets management; PII scrubbing on ingestion
- Denial of Service: Rate limiting, timeouts, circuit breakers, resource quotas
- Elevation of Privilege: Least privilege for containers, DB users; network policies

## Mitigations (MVP → Prod)
- MVP: API key for orchestrator, timeouts/retries; non-root containers; .env for dev
- Prod: Gateway + SSO; OTel + central logging; scanning in CI; backups; key rotation

