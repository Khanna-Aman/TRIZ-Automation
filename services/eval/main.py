from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IIA Evaluation & Evolution Service")

class Candidates(BaseModel):
    items: list[str]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/evaluate")
async def evaluate(cands: Candidates):
    # Placeholder: MCDA + Elo-like ranking
    ranked = sorted(cands.items)
    return {"ranked": ranked, "metrics": {"novelty": 0.5}}

