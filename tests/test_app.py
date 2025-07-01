import json
import pytest  # type: ignore
import fakeredis  # type: ignore

import app as flask_app


@pytest.fixture()
def client(monkeypatch):
    """Create Flask test client with a fake Redis backend."""
    fake_redis = fakeredis.FakeStrictRedis(decode_responses=True)
    # Patch the redis_client inside the imported app module
    monkeypatch.setattr(flask_app, "redis_client", fake_redis)
    with flask_app.app.test_client() as client:
        yield client


def test_save_validation_error(client):
    """Missing parameters should return 400 and code -1."""
    res = client.post("/api/v1/clipboard/save", json={})
    assert res.status_code == 400
    body = res.get_json()
    assert body["code"] == -1


def test_list_validation_error(client):
    res = client.post("/api/v1/clipboard/list", json={})
    assert res.status_code == 400
    assert res.get_json()["code"] == -1


def test_save_and_list_success(client):
    payload = {"password": "123", "content": "hello"}
    save_res = client.post("/api/v1/clipboard/save", json=payload)
    assert save_res.status_code == 200
    assert save_res.get_json()["code"] == 0

    list_res = client.post("/api/v1/clipboard/list", json={"password": "123"})
    assert list_res.status_code == 200
    data = list_res.get_json()["data"]["clipboard_contents"]
    assert len(data) == 1
    assert data[0]["content"] == "hello"