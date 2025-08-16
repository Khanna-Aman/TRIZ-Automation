import sys
from fastapi.testclient import TestClient

sys.path.append("services/lateral")
from main import app  # noqa: E402

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

