from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import os
import asyncio
import httpx
from prometheus_fastapi_instrumentator import Instrumentator

TRIZ_URL = os.getenv("TRIZ_URL", "http://triz:8000")
LATERAL_URL = os.getenv("LATERAL_URL", "http://lateral:8000")
EVAL_URL = os.getenv("EVAL_URL", "http://eval:8000")
API_KEY = os.getenv("API_KEY")

DEFAULT_TIMEOUT = httpx.Timeout(connect=3.0, read=10.0, write=10.0, pool=5.0)
MAX_RETRIES = 3

app = FastAPI(title="IIA Orchestrator")
Instrumentator().instrument(app).expose(app)

class StartProblemRequest(BaseModel):
    problem_statement: str
    context: str | None = None
    url: str | None = None  # optional RAG ingestion URL (future)

def require_api_key(x_api_key: str | None = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

async def _post_with_retries(client: httpx.AsyncClient, url: str, json: dict):
    last_exc = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = await client.post(url, json=json)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            last_exc = e
            await asyncio.sleep(0.5 * (2 ** attempt))
    raise last_exc

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/problems/start")
async def start_problem(req: StartProblemRequest, _: None = Depends(require_api_key)):
    # Sequential MVP: TRIZ → Lateral → Merge → Evaluate
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        # TRIZ
        try:
            triz = await _post_with_retries(client, f"{TRIZ_URL}/triz/resolve", {"problem": req.problem_statement})
        except Exception as e:
            raise HTTPException(status_code=502, detail={"stage": "triz", "error": str(e)})

        # Lateral
        try:
            lat = await _post_with_retries(client, f"{LATERAL_URL}/lateral/generate", {"problem": req.problem_statement})
        except Exception as e:
            raise HTTPException(status_code=502, detail={"stage": "lateral", "error": str(e)})

        # Merge
        triz_solutions = [str(s) for s in (triz.get("solutions") or [])]
        lat_ideas = [i.get("idea", "") for i in (lat.get("ideas") or [])]
        items = [*triz_solutions, *lat_ideas]

        # Evaluate
        try:
            eval_res = await _post_with_retries(client, f"{EVAL_URL}/evaluate", {"items": items})
        except Exception as e:
            raise HTTPException(status_code=502, detail={"stage": "evaluate", "error": str(e)})

    return {
        "status": "completed",
        "input": {"problem_statement": req.problem_statement, "context": req.context},
        "triz": triz,
        "lateral": lat,
        "evaluation": eval_res,
    }

