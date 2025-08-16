## Roadmap

### Phase 1 — MVP (current)
- Service scaffolds (orchestrator, triz, lateral, rag, eval, worker)
- Orchestrator integration with TRIZ/Lateral/Eval
- TRIZ DB schema + import; lookup endpoints
- n8n & LangGraph MVP workflows

### Phase 2 — RAG & TRIZ integration
- Implement RAG ingestion (embedding + Qdrant + Neo4j)
- Hybrid retrieval endpoint
- TRIZ param extraction from text; use lookup in resolve

### Phase 3 — Evaluation & Playoffs
- MCDA scoring + criteria generation
- League matches + Elo ratings; top-N selection with traces

### Phase 4 — Observability & Security
- Prometheus + Grafana + OTel collector in Compose
- API Gateway (Traefik/Kong) + Keycloak SSO
- Structured logging, request IDs

### Phase 5 — UI & Ops
- Electron + React MVP UI
- CI/CD (tests, lint, images, scans)
- Backups, DR, and SLOs

