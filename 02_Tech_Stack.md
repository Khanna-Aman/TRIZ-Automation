## 02 — Tech Stack and Software Architecture (Open Source)

### Executive Summary
This document translates the Intuitive Inventive Agent (IIA) concept into a concrete, open‑source tech stack and architecture. It operationalizes: (1) TRIZ automation for contradiction resolution, (2) lateral thinking pipelines, (3) a RAG‑Graph world model, and (4) dual orchestration using LangGraph (internal cognition) and n8n (external flows). It also incorporates AlphaEvolve‑inspired evolutionary refinement and a playoff evaluation framework for idea ranking.

---

### Guiding Principles (from IIA concept)
- Dual cognition: combine System‑2 (TRIZ, deterministic lookup) with System‑1 (lateral thinking, creative exploration)
- Knowledge-centric: build a RAG‑Graph to preserve semantics and relationships
- Transparent orchestration: LangGraph for internal agent state, n8n for external tools and auditability
- Evolutionary improvement: iterative generate‑select loops with fitness functions and playoffs
- Human‑in‑the‑loop: reviewable traces, checkpoints, and explainability

---

## 1) High-Level Architecture
- Experience layer: Desktop UI (Electron + React) with knowledge graph exploration and workflow transparency
- Orchestration layer: LangGraph (internal agent flow state) + n8n (external workflow, integrations)
- Intelligence layer: LLM(s) + prompt/templates, deterministic TRIZ matrix, lateral thinking tools, evaluators
- Knowledge layer: RAG‑Graph atop a graph DB + vector DB; document ingestion and enrichment
- Services layer: FastAPI microservices for TRIZ, Lateral, RAG, Evaluation, and Orchestrator
- Data & infra layer: Postgres (metadata), Neo4j/ArangoDB (graph), Qdrant (vectors), Redis (cache), RabbitMQ (queue)
- Observability & ops: Prometheus, Grafana, OpenTelemetry, Loki; CI/CD via GitHub Actions; containerized with Docker/Kubernetes

---

## 2) Component Choices (Open Source)

### Frontend (Desktop + Web)
- Electron (desktop shell), React (UI), Vite (bundling), TypeScript
- State mgmt: Redux Toolkit or Zustand
- Graph viz: Cytoscape.js (graph UI), D3.js (aux charts)
- Styling: Tailwind CSS

### Backend (Python)
- FastAPI (HTTP APIs), Uvicorn (ASGI), Pydantic (schemas)
- Task/queue: Celery + RabbitMQ (background jobs), or Arq + Redis
- Caching: Redis
- File/object store: MinIO (S3‑compatible) for corpora and traces

### LLM & Serving
- Base models (OSI‑approved licenses): Qwen2.5‑Instruct (7B/14B/32B, Apache‑2.0), DeepSeek‑Coder‑V2 (MIT) for code‑heavy tasks; optionally Mistral/Mixtral community builds where license permits
- Serving: vLLM or TGI (Text Generation Inference); Ollama for local dev
- Embeddings: bge‑large‑en‑v1.5 or e5‑large‑v2 (Apache‑2.0, via SentenceTransformers); rerankers: bge‑reranker‑large

### Knowledge and Retrieval
- Graph DB: Neo4j Community (as in concept) or ArangoDB (Apache‑2.0 alternative)
- Vector DB: Qdrant (default) or Weaviate/Milvus
- Indexing: LangChain or LlamaIndex; hybrid search with BM25 + dense vectors
- Optional: Neo4j Graph Data Science for path/centrality; GraphCypherQA for Cypher‑based RAG

### Orchestration & Agents
- Internal cognition: LangGraph (agent state machine, memory)
- External automation: n8n (HTTP, web search, scraping, schedulers, human approval)
- Optional multi‑agent tooling: CrewAI or AutoGen (coordination patterns)

### Data & Storage
- Postgres (metadata, audits, runs, idea scores)
- Neo4j/ArangoDB (RAG‑Graph of entities/relations/principles/cases)
- Qdrant (embeddings; HNSW index)
- MinIO (raw docs, PDFs, artifacts)

### Observability, Security, DevEx
- Metrics/Logs/Traces: Prometheus + Grafana, Loki, OpenTelemetry SDKs
- Feature tracking for LLM apps: Langfuse (prompt/version/feedback telemetry)
- AuthN/Z: Keycloak (OIDC), API Gateway: Traefik or Kong
- Secrets: HashiCorp Vault (prod) / dotenv (dev)
- QA & style: Ruff/Black/mypy/pytest; pre‑commit hooks; GitHub Actions CI

---

## 3) Service Decomposition

1) API Gateway
- Traefik/Kong routes requests; rate‑limits and enforces auth

2) Orchestrator Service (FastAPI)
- Owns session state, exposes high‑level endpoints (start_problem, status, results)
- Invokes LangGraph graphs; triggers n8n external workflows

3) TRIZ Service
- Holds 39×39 contradiction matrix + 40 principles (JSON/DB)
- Extracts improving/worsening parameters, resolves to principles, prompts LLM for contextual solutions

4) Lateral Thinking Service
- Implements Six Thinking Hats, PMI, CAF, provocations, random‑word stimulation
- Produces creative variants with higher‑temperature LLM prompts

5) RAG‑Graph Service
- Ingestion: crawl/scrape (Playwright/Crawlee), parse (unstructured.io), chunk & embed (bge/e5)
- Storage: create/update entities and relations in Graph DB; store vectors in Qdrant
- Retrieval: hybrid query → vector candidates → graph expansion (k‑hop) → fusion

6) Evaluation & Evolution Service
- AlphaEvolve‑style loop: tournament selection, mutation (prompted edits), crossover of ideas
- Playoff evaluator: domain‑specific criteria (generated by a “framework creation agent”) + MCDA scoring
- Outputs rankings, intuition metrics, and traces

7) Worker(s)
- Celery workers for long‑running tasks (ingestion, batch evaluations, graph builds)

---

## 4) Data Flow (Aligned to the Concept’s Algorithms)

A) Problem Intake & Refinement (Master Orchestration)
- User submits problem → Orchestrator → LangGraph “Refine” node → embedding for context join

B) Dual‑Path Generation
- Analytical path: TRIZPipeline
  - Map to TRIZ params → lookup principles → LLM syntheses (temperature≈0.2–0.4)
  - RAG‑augment with similar cases via Graph + vectors → refine
- Creative path: LateralThinkingPipeline
  - Hats/PMI/CAF/Provocations/Random‑word → ideas → PMI scores → filter

C) Merge & Evolution
- Merge candidate solutions; run N generations of evolutionary refinement
- Apply mutation/crossover; include creative LLM mutations (temperature≈0.7–0.9)

D) Validation & Playoffs
- Build domain‑specific evaluation framework (e.g., Five Forces, feasibility, ideality, risk)
- Run pairwise/league matches; compute Elo‑like ratings; produce Top‑N with traces

E) Results & Explainability
- Persist solutions, scores, intuition metrics; expose reasoning trace and checkpoints

---

## 5) Data Model (Essentials)
- Graph nodes: Problem, Parameter(Improving|Worsening), Principle, Concept, Entity, Document, CaseStudy, Idea
- Relationships: CONTRADICTS, SUGGESTS (Param→Principle), DERIVES_FROM (Idea→Principle/Case), SUPPORTS (Doc→Idea)
- Vector records: chunk_id, embedding, doc_id, tags (domain, date, source)
- Metadata (Postgres): run_id, session_id, prompt_id, eval_scores, intuition_metrics, playoff_matches

---

## 6) APIs (Representative)
- POST /problems/start → {problem_statement, context} → {run_id}
- GET /problems/{run_id}/status → orchestration progress
- GET /problems/{run_id}/results → ranked ideas, traces
- POST /ingest → {url|file} → pipeline status
- GET /graph/entity/{id} → node + neighborhood

---

## 7) Orchestration Topology
- LangGraph:
  - Nodes: Refine → TRIZ → Lateral → Merge → Evolve → Evaluate → Rank
  - Memory: per‑run state (problem vectors, applied principles, idea lineage)
- n8n:
  - Flows: Web search, Wikipedia, patent search connectors; human approval steps; notifications; scheduled re‑index

---

## 8) Deployment

### Dev (single machine)
- Docker Compose services: gateway, api, triz, lateral, rag, eval, workers, neo4j, qdrant, postgres, redis, minio, n8n, grafana, prometheus, loki
- Ollama/TGI for local model serving

### Prod (Kubernetes)
- Ingress (Traefik), Horizontal Pod Autoscaling for workers/LLM serving
- StatefulSets for Neo4j/Qdrant/Postgres/MinIO, PVs with backups
- Secrets via Vault injectors; telemetry with OTel Collector → Prometheus/Grafana

---

## 9) Security & Governance
- SSO via Keycloak; per‑project RBAC and scoped API tokens
- Prompt/trace governance with Langfuse; PII scrubbing on ingestion (Presidio)
- Rate limiting, content filters, and allowed‑tools allowlist in n8n

---

## 10) Evaluation & Metrics
- Novelty (semantic distance), feasibility (rules/constraints), ideality, resource efficiency
- Intuition quality (pattern match to expert exemplars; elegance; cognitive balance)
- Playoff statistics (win rate, Elo delta, stability across seeds)

---

## 11) Build Plan (Phased)
1. Foundations: repos, CI, FastAPI skeletons, Docker Compose, Postgres/Redis
2. RAG‑Graph MVP: ingestion → Qdrant + Neo4j; hybrid retrieval
3. TRIZ engine: param extraction → matrix lookup → LLM synthesis
4. Lateral module: hats/PMI/CAF/Provocations + filtering
5. Orchestration: LangGraph graph + n8n external flows; basic tracing
6. Evaluation: MCDA, playoff loop, intuition metrics; dashboards
7. Hardening: Auth, gateway, observability, k8s manifests, backups

---

### Notes & Alternatives
- Knowledge Graph: Neo4j CE (as per concept) is fine; ArangoDB is Apache‑2.0 alternative
- Vector DB: Qdrant recommended for simplicity and performance
- Model serving: vLLM for throughput; TGI for multi‑model serving; Ollama for offline dev
- Libraries: LangChain or LlamaIndex are both viable; pick one to reduce duplication

This stack delivers a fully open‑source path to the IIA framework described in “A Concept for Automated Creative Problem‑Solving,” preserving the dual‑path reasoning, orchestration strategy, and evolutionary/playoff evaluation while ensuring transparency, reproducibility, and vendor independence.
