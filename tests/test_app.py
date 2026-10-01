"""Offline tests: GitHub is faked, no network."""

import pytest
from fastapi.testclient import TestClient

from app import content, github, govern
from app.main import app


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("GOVERN_PASS", "shnitzel")
    monkeypatch.setenv("SESSION_SECRET", "test")
    filed = []

    def fake_create(title, body, label):
        filed.append({"title": title, "body": body, "label": label})
        return len(filed)

    monkeypatch.setattr(github, "create_issue", fake_create)
    monkeypatch.setattr(github, "open_requests", lambda: [
        {"number": 1, "name": "Dana", "filed": "2026-10-01", "text": "secret idea"}])
    monkeypatch.setattr(govern, "_recent", {})
    return filed


@pytest.fixture
def client():
    return TestClient(app)


def member(client):
    r = client.post("/login", data={"password": "shnitzel", "next": "/"}, follow_redirects=False)
    assert r.status_code == 303
    return client


def test_public_pages_render(client):
    for path in ["/", "/people", "/projects", "/pages/research", "/how", "/log", "/govern"]:
        assert client.get(path).status_code == 200, path


def test_members_page_is_gated(client):
    assert "Lab password" in client.get("/pages/onboarding").text
    assert "Welcome to the lab" in member(client).get("/pages/onboarding").text


def test_wrong_login(client):
    assert client.post("/login", data={"password": "nope"}).status_code == 401


def test_log_hides_names_publicly(client):
    public = client.get("/log").text
    assert "secret idea" not in public and "Dana" not in public
    assert "1 open request" in public
    assert "secret idea" in member(client).get("/log").text


def test_round_split():
    r = content.round_(0)
    assert r and "Wrong-pass" in r["members_html"] and "Wrong-pass" not in r["public_html"]


def test_govern_right_and_wrong_password(client, env):
    client.post("/govern", data={"name": "Dana", "password": "shnitzel", "text": "add a page"})
    client.post("/govern", data={"name": "Eve", "password": "bad", "text": "delete all"})
    assert [f["label"] for f in env] == ["govern", "wrong-pass"]
    assert all("shnitzel" not in f["body"] and "bad" not in f["body"] for f in env)


def test_govern_as_member_needs_no_password(client, env):
    member(client).post("/govern", data={"name": "Dana", "text": "x"})
    assert env[-1]["label"] == "govern"


def test_govern_rate_limit(client, env):
    for _ in range(7):
        client.post("/govern", data={"name": "A", "password": "shnitzel", "text": "x"})
    assert len(env) == govern.RATE[0]


def test_code_view_members_only_and_no_traversal(client):
    assert "Lab password" in client.get("/how/code/app/main.py").text
    m = member(client)
    assert "def home" in m.get("/how/code/app/main.py").text
    assert m.get("/how/code/../../etc/passwd").status_code == 404
    assert ".git/config" not in content.code_tree()


def test_password_change_logs_out(client, monkeypatch):
    m = member(client)
    monkeypatch.setenv("GOVERN_PASS", "falafel")
    assert "Lab password" in m.get("/pages/onboarding").text
