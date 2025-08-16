import os
from typing import List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="IIA TRIZ Service")
Instrumentator().instrument(app).expose(app)

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://iia:iia@postgres:5432/iia")

class TRIZRequest(BaseModel):
    problem: str
    improving: int | None = None
    worsening: int | None = None

class PrincipleOut(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None

def _fetchone(cur, q: str, args: tuple):
    cur.execute(q, args)
    return cur.fetchone()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/triz/lookup", response_model=List[int])
async def triz_lookup(improving: int = Query(..., ge=1, le=39), worsening: int = Query(..., ge=1, le=39)):
    try:
        with psycopg.connect(POSTGRES_URL) as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT principle_id
                FROM triz_matrix_link
                WHERE improving_param=%s AND worsening_param=%s
                ORDER BY principle_id
                """,
                (improving, worsening),
            )
            rows = cur.fetchall()
            return [r[0] for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/triz/principles", response_model=List[PrincipleOut])
async def list_principles():
    try:
        with psycopg.connect(POSTGRES_URL) as conn, conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM triz_principle ORDER BY id")
            rows = cur.fetchall()
            return [PrincipleOut(id=r[0], name=r[1], description=r[2]) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/triz/parameters", response_model=List[PrincipleOut])
async def list_parameters():
    try:
        with psycopg.connect(POSTGRES_URL) as conn, conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM triz_parameter ORDER BY id")
            rows = cur.fetchall()
            return [PrincipleOut(id=r[0], name=r[1], description=r[2]) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/triz/resolve")
async def triz_resolve(req: TRIZRequest):
    # MVP: if improving/worsening provided, return principle IDs via DB lookup, with placeholder solutions
    if req.improving and req.worsening:
        ids = await triz_lookup(req.improving, req.worsening)  # type: ignore[arg-type]
        return {"principles": ids, "solutions": [f"Apply principle {pid}" for pid in ids]}
    # Otherwise, placeholder (future: extract params from problem text)
    return {"principles": [1, 35], "solutions": ["Example solution A", "Example solution B"]}

