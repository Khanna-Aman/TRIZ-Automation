from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IIA RAG-Graph Service")

class IngestRequest(BaseModel):
    url: str | None = None

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(req: IngestRequest):
    # Placeholder: crawl/parse/embed/index
    return {"status": "queued", "source": req.url}

@app.post("/query")
async def query(req: QueryRequest):
    # Placeholder: hybrid retrieval and fusion
    return {"passages": ["stub passage"], "subgraph": []}

