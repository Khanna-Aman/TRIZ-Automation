from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IIA Lateral Service")

class LateralRequest(BaseModel):
    problem: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/lateral/generate")
async def lateral_generate(req: LateralRequest):
    # Placeholder: Six Hats, PMI, CAF, provocations, random-word
    ideas = [
        {"technique": "six_hats", "idea": "White hat facts summary"},
        {"technique": "pmi", "idea": "PMI analysis draft"},
    ]
    return {"ideas": ideas}

