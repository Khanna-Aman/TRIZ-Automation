## 04 — Sequence Flows

The following Mermaid sequence diagrams capture the main workflows aligned with the IIA concept and 02_Tech_Stack.md.

---

### 1) Problem Intake & Refinement (Master Orchestration)
```mermaid
sequenceDiagram
  autonumber
  participant User
  participant UI as Electron/React
  participant API as API Gateway
  participant ORCH as Orchestrator (FastAPI+LangGraph)
  participant LG as LangGraph Graph
  participant RAG as RAG‑Graph Service
  participant PG as Postgres

  User->>UI: Submit problem statement + context
  UI->>API: POST /problems/start
  API->>ORCH: Forward request (OIDC checked)
  ORCH->>LG: Start run (initialize state)
  LG->>LG: Refine Problem (prompting, constraints)
  LG->>RAG: Embed/ref context; retrieve related docs
  RAG-->>LG: Context passages + graph subview
  LG->>PG: Persist refined problem + context refs
  LG-->>ORCH: Refined statement, embeddings
  ORCH-->>UI: run_id, status=running
```

---

### 2) TRIZPipeline
```mermaid
sequenceDiagram
  autonumber
  participant LG as LangGraph Node: TRIZPipeline
  participant TRIZ as TRIZ Service
  participant RAG as RAG‑Graph Service
  participant LLM as vLLM/TGI

  LG->>TRIZ: Extract TRIZ params (improving/worsening)
  TRIZ->>TRIZ: Lookup 39×39 matrix → principles
  TRIZ->>LLM: Generate contextual solutions (low temp)
  LLM-->>TRIZ: Draft solutions
  TRIZ->>RAG: Retrieve similar cases/examples
  RAG-->>TRIZ: Case snippets + citations
  TRIZ->>LG: Refined TRIZ solutions + analysis
```

---

### 3) LateralThinkingPipeline
```mermaid
sequenceDiagram
  autonumber
  participant LG as LangGraph Node: LateralThinking
  participant LAT as Lateral Service
  participant LLM as vLLM/TGI

  LG->>LAT: Request lateral exploration
  LAT->>LLM: Six Hats perspectives
  LLM-->>LAT: Hat insights
  LAT->>LLM: PMI/CAF runs; provocations; random‑word stim
  LLM-->>LAT: Idea variants (+ PMI stats)
  LAT->>LG: Filtered creative ideas (score >= threshold)
```

---

### 4) Merge + Evolutionary Refinement + Playoffs
```mermaid
sequenceDiagram
  autonumber
  participant LG as LangGraph Nodes: Merge→Evolve→Evaluate
  participant EVAL as Evaluation & Evolution Service
  participant LLM as vLLM/TGI
  participant PG as Postgres

  LG->>EVAL: Merge TRIZ + Lateral candidates
  EVAL->>EVAL: Tournament selection
  EVAL->>LLM: Creative mutations (high temp)
  LLM-->>EVAL: Mutated variants
  EVAL->>EVAL: Crossover + elitist selection (N gens)
  EVAL->>EVAL: Build domain-specific framework (criteria)
  EVAL->>EVAL: Pairwise/league matches (Elo-like)
  EVAL->>PG: Persist scores, metrics, traces
  EVAL-->>LG: Top-N ranked ideas + explanations
```

---

### 5) RAG‑Graph Retrieval (Hybrid)
```mermaid
sequenceDiagram
  autonumber
  participant Client
  participant RAG as RAG‑Graph API
  participant Q as Qdrant
  participant G as Neo4j/ArangoDB
  participant LLM as Reranker/Embedder

  Client->>RAG: Query (text + filters)
  RAG->>Q: Vector search (kNN)
  RAG->>G: Graph expansion (k-hop, constraints)
  Q-->>RAG: Candidate chunks + scores
  G-->>RAG: Related entities/paths
  RAG->>LLM: Optional rerank/fusion
  LLM-->>RAG: Reranked set
  RAG-->>Client: Ranked passages + subgraph + citations
```

---

### 6) End-to-End Result Delivery
```mermaid
sequenceDiagram
  autonumber
  participant UI as Electron/React
  participant API as API Gateway
  participant ORCH as Orchestrator
  participant PG as Postgres

  UI->>API: GET /problems/{run_id}/results
  API->>ORCH: Fetch results
  ORCH->>PG: Load ranked ideas, metrics, trace
  PG-->>ORCH: Data
  ORCH-->>API: Structured result payload
  API-->>UI: Display Top-N, Elo, intuition metrics, trace
```

