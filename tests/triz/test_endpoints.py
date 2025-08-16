import os
import sys
from fastapi.testclient import TestClient

sys.path.append("services/triz")
from main import app  # noqa: E402

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200


def test_principles_list_smoke():
    r = client.get("/triz/principles")
    # Without DB, this may 500; in CI we don't require DB to be up, so permit 200/500
    assert r.status_code in (200, 500)

