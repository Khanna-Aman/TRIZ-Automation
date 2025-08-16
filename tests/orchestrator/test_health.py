import os
import pytest
from fastapi.testclient import TestClient

import sys
sys.path.append("services/orchestrator")
from main import app  # noqa: E402

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

