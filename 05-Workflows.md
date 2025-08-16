## 05 — Workflows (n8n & LangGraph MVP)

This document proposes minimal, practical n8n and LangGraph workflows that operate against the current service stubs:
- orchestrator: http://orchestrator:8000
- triz: http://triz:8000
- lateral: http://lateral:8000
- rag: http://rag:8000
- eval: http://eval:8000

n8n runs in the same Docker network, so service DNS names work directly.

---

### MVP scenario
Goal: Given a problem statement, retrieve a little context (optional), generate TRIZ and Lateral ideas, merge them, evaluate and return Top‑N.

We provide:
- An n8n “single-pass” orchestration that calls each service in sequence and returns a final payload
- A LangGraph internal graph that mirrors the same steps for programmatic use
- Optional ingestion scheduler and a human‑in‑the‑loop review workflow pattern

---

## A) n8n Workflows

### A.1 Single‑Pass Orchestration (Strictly Sequential)

- Trigger: Webhook (POST)
- Strict steps (linear):
  1) (Optional) Ingest context URL via rag:/ingest
  2) TRIZ ideas via triz:/triz/resolve
  3) Lateral ideas via lateral:/lateral/generate
  4) Merge results using a Merge node (Merge by Index)
  5) Flatten ideas in a Function node
  6) Evaluate via eval:/evaluate
  7) Respond to caller

Minimal n8n JSON export (import in n8n > Workflow > Import):
```json
{
  "name": "MVP-Orchestration-Sequential",
  "nodes": [
    {"parameters": {"path": "mvp/run"}, "name": "Webhook", "type": "n8n-nodes-base.webhook", "typeVersion": 1, "position": [200, 200]},
    {"parameters": {"url": "http://rag:8000/ingest", "method": "POST", "jsonParameters": true, "bodyParametersJson": "={\n  \"url\": {{$json.url}}\n}"}, "name": "RAG Ingest", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [460, 200]},
    {"parameters": {"url": "http://triz:8000/triz/resolve", "method": "POST", "jsonParameters": true, "bodyParametersJson": "={\n  \"problem\": {{$json.problem}}\n}"}, "name": "TRIZ", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [720, 200]},
    {"parameters": {"url": "http://lateral:8000/lateral/generate", "method": "POST", "jsonParameters": true, "bodyParametersJson": "={\n  \"problem\": {{$json.problem}}\n}"}, "name": "Lateral", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [980, 200]},
    {"parameters": {"mode": "mergeByIndex"}, "name": "Merge (TRIZ + Lateral)", "type": "n8n-nodes-base.merge", "typeVersion": 2, "position": [1240, 200]},
    {"parameters": {"functionCode": "const j = items[0].json;\nconst trizSolutions = (j.solutions || []).map(s => String(s));\nconst latIdeas = (j.ideas || []).map(i => i.idea);\nreturn [{ json: { items: [...trizSolutions, ...latIdeas] } }];"}, "name": "Flatten Ideas", "type": "n8n-nodes-base.function", "typeVersion": 2, "position": [1500, 200]},
    {"parameters": {"url": "http://eval:8000/evaluate", "method": "POST", "jsonParameters": true, "bodyParametersJson": "={{$json}}"}, "name": "Evaluate", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [1760, 200]},
    {"parameters": {"responseBody": "={{$json}}"}, "name": "Respond", "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1, "position": [2020, 200]}
  ],
  "connections": {
    "Webhook": {"main": [[{"node": "RAG Ingest", "type": "main", "index": 0}]]},
    "RAG Ingest": {"main": [[{"node": "TRIZ", "type": "main", "index": 0}]]},
    "TRIZ": {"main": [[{"node": "Lateral", "type": "main", "index": 0}, {"node": "Merge (TRIZ + Lateral)", "type": "main", "index": 0}]]},
    "Lateral": {"main": [[{"node": "Merge (TRIZ + Lateral)", "type": "main", "index": 1}]]},
    "Merge (TRIZ + Lateral)": {"main": [[{"node": "Flatten Ideas", "type": "main", "index": 0}]]},
    "Flatten Ideas": {"main": [[{"node": "Evaluate", "type": "main", "index": 0}]]},
    "Evaluate": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}
  }
}
```
Notes:
- If you skip ingestion, connect Webhook → TRIZ directly and remove the RAG node.
- The Merge node waits for both inputs and merges by index; the Function node then flattens solutions + ideas into a single array for evaluation.

Payload to trigger (example):
```json
{
  "problem": "Reduce the weight of a drone without decreasing structural integrity",
  "url": "https://example.com/domain-docs/drone-materials.pdf"
}
```

---

### A.2 Content Ingestion Scheduler
- Trigger: Cron (e.g., hourly)
- Steps: HTTP Request to http://rag:8000/ingest with a predefined list of URLs (use Split In Batches over an array of URLs)
- Optional: Add notifications (Slack/Email) on success/failure

---

### A.3 Human‑in‑the‑Loop Review Pattern
- Webhook receives candidate ideas
- “Wait for Approval” pattern:
  - Store candidates (Postgres node)
  - Send Email/Slack with an approval link (a second Webhook)
  - Second Webhook updates status to approved/rejected
  - On approval, the workflow continues to Evaluation or to downstream systems

---

## B) LangGraph MVP Graph (Python)

This example uses simple HTTP calls to the microservices. It mirrors the n8n sequence: Refine → TRIZ + Lateral → Merge → Evaluate.

```python
# Minimal illustrative code (pseudo-real). Install: pip install httpx langgraph
from typing import TypedDict, List, Any
import httpx
from langgraph.graph import StateGraph, END

TRIZ_URL = "http://triz:8000"
LATERAL_URL = "http://lateral:8000"
EVAL_URL = "http://eval:8000"
RAG_URL = "http://rag:8000"

class RunState(TypedDict, total=False):
    problem: str
    url: str
    refined: str
    triz_solutions: List[str]
    lateral_ideas: List[str]
    merged: List[str]
    ranked: List[str]
    metrics: Any

async def refine_node(state: RunState) -> RunState:
    # Placeholder refinement: echo problem (could call orchestrator/RAG here)
    return {**state, "refined": state["problem"]}

async def triz_node(state: RunState) -> RunState:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{TRIZ_URL}/triz/resolve", json={"problem": state["refined"]})
        data = r.json()
    sols = [str(s) for s in data.get("solutions", [])]
    return {**state, "triz_solutions": sols}

async def lateral_node(state: RunState) -> RunState:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{LATERAL_URL}/lateral/generate", json={"problem": state["refined"]})
        data = r.json()
    ideas = [i.get("idea", "") for i in data.get("ideas", [])]
    return {**state, "lateral_ideas": ideas}

async def merge_node(state: RunState) -> RunState:
    merged = (state.get("triz_solutions", []) or []) + (state.get("lateral_ideas", []) or [])
    return {**state, "merged": merged}

async def evaluate_node(state: RunState) -> RunState:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{EVAL_URL}/evaluate", json={"items": state.get("merged", [])})
        data = r.json()
    return {**state, "ranked": data.get("ranked", []), "metrics": data.get("metrics", {})}

# Build the graph
workflow = StateGraph(RunState)
workflow.add_node("refine", refine_node)
workflow.add_node("triz", triz_node)
workflow.add_node("lateral", lateral_node)
workflow.add_node("merge", merge_node)
workflow.add_node("evaluate", evaluate_node)

workflow.set_entry_point("refine")
workflow.add_edge("refine", "triz")
workflow.add_edge("refine", "lateral")
workflow.add_edge("triz", "merge")
workflow.add_edge("lateral", "merge")
workflow.add_edge("merge", "evaluate")
workflow.add_edge("evaluate", END)

# Later: app = workflow.compile(); await app.ainvoke({"problem": "..."})
```

Notes:
- Replace refine_node with a call to RAG for retrieving context, or orchestrator for stateful runs.
- You can fan-in TRIZ and Lateral using a barrier pattern if desired (LangGraph supports conditional routing and tool nodes).

---

## C) End-to-end testing

- Ensure containers are running and n8n is reachable (default: http://localhost:5678)
- Import the MVP-Orchestration-SinglePass workflow JSON into n8n
- In n8n, open the Webhook node to get the test URL (production vs test URL differs)
- Trigger with a JSON payload as shown above; confirm response contains ranked ideas
- For LangGraph, install dependencies and run an async entry that calls app.ainvoke({"problem": "..."})

---

## D) Future enhancements

- Replace stubs with real logic (TRIZ DB-backed lookup, lateral techniques, RAG hybrid retrieval)
- Add retries/timeouts to HTTP nodes (both n8n and LangGraph httpx)
- Persist runs and traces (Postgres) and add Langfuse for prompt/trace governance
- Human approval checkpoints before Evaluate (both n8n and LangGraph conditional nodes)

