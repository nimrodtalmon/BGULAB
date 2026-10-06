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
    monkeypatch.setattr(govern, "_sent", {})
    return filed


@pytest.fixture
def client():
    return TestClient(app)


def member(client, name="Dana"):
    r = client.post("/login", data={"name": name, "password": "shnitzel", "next": "/"},
                    follow_redirects=False)
    assert r.status_code == 303
    return client


def test_public_pages_render(client):
    for path in ["/", "/people", "/govern"]:
        assert client.get(path).status_code == 200, path


def test_old_addresses_redirect(client):
    for old, new in [("/how", "/govern#how-this-works"), ("/log", "/govern#rounds"),
                     ("/projects", "/"), ("/pages/research", "/"),
                     ("/pages/onboarding", "/pages/lab")]:
        r = client.get(old, follow_redirects=False)
        assert r.status_code == 301 and r.headers["location"] == new, old


def test_members_page_is_gated(client):
    assert "Lab password" in client.get("/pages/lab").text
    assert "Getting started" in member(client).get("/pages/lab").text


def test_wrong_login(client):
    assert client.post("/login", data={"name": "A", "password": "nope"}).status_code == 401
    assert client.post("/login", data={"name": "", "password": "shnitzel"}).status_code == 401


def test_signed_in_shows_name(client):
    assert "Sign in" in client.get("/").text
    page = member(client, "Eyal").get("/").text
    assert "Eyal" in page and "sign out" in page


def test_log_hides_names_publicly(client):
    public = client.get("/govern").text
    assert "secret idea" not in public and "Dana" not in public
    assert "1 open request" in public
    assert "secret idea" in member(client).get("/govern").text


def test_round_split():
    r = content.round_(0)
    assert r and "Wrong-pass" in r["lab_html"] and "Wrong-pass" not in r["public_html"]


def test_govern_right_and_wrong_password(client, env):
    client.post("/govern", data={"name": "Dana", "password": "shnitzel", "text": "add a page"})
    TestClient(app).post("/govern", data={"name": "Eve", "password": "bad", "text": "delete all"})
    assert [f["label"] for f in env] == ["govern", "wrong-pass"]
    assert all("shnitzel" not in f["body"] and "bad" not in f["body"] for f in env)


def test_govern_as_member_needs_no_password(client, env):
    member(client, "Dana").post("/govern", data={"name": "Mallory", "text": "x"})
    assert env[-1]["label"] == "govern" and "name: Dana" in env[-1]["body"]


def test_govern_with_right_password_signs_in(client, env):
    client.post("/govern", data={"name": "Dana", "password": "shnitzel", "text": "x"})
    assert "Sending as Dana" in client.get("/govern").text


def test_folding_and_lab_only_sections():
    body = "# T\n\nintro\n\n## A\n\ntext\n\n### Sub\n\ns\n\n## B (lab only)\n\nhidden\n"
    public, lab = content.fold(body, False), content.fold(body, True)
    assert '<details id="a">' in public and '<details class="sub" id="sub">' in public
    assert "hidden" not in public and "hidden" in lab and "lab only" in lab


def test_govern_rate_limit(client, env):
    for i in range(7):  # not signed in (wrong password): limited
        client.post("/govern", data={"name": "A", "password": "nope", "text": f"x{i}"})
    assert len(env) == govern.RATE[0]


def test_govern_signed_in_not_rate_limited(client, env):
    member(client)
    for i in range(8):
        client.post("/govern", data={"text": f"y{i}"})
    assert len(env) == 8


def test_code_view_members_only_and_no_traversal(client):
    assert "Lab password" in client.get("/how/code/app/main.py").text
    m = member(client)
    assert "def home" in m.get("/how/code/app/main.py").text
    assert m.get("/how/code/../../etc/passwd").status_code == 404
    assert ".git/config" not in content.code_tree()


def test_password_change_logs_out(client, monkeypatch):
    m = member(client)
    monkeypatch.setenv("GOVERN_PASS", "falafel")
    assert "Lab password" in m.get("/pages/lab").text


def test_govern_double_click_files_once(client, env):
    for _ in range(2):
        r = client.post("/govern", data={"name": "Dana", "password": "shnitzel", "text": "same"})
    assert len(env) == 1 and "Already filed as #1" in r.text
    client.post("/govern", data={"name": "Dana", "text": "different"})
    assert len(env) == 2


def test_govern_popup_records_page_and_answers_json(client, env):
    assert 'id="govern-pop"' in client.get("/people").text
    r = client.post("/govern", headers={"Accept": "application/json"},
                    data={"name": "Dana", "password": "shnitzel", "text": "fix this",
                          "page": "/pages/lab#house-style"})
    assert r.json()["ok"] and "page: /pages/lab#house-style" in env[-1]["body"]
    client.post("/govern", data={"name": "Dana", "text": "y", "page": "//evil.example\nname: Eve"})
    assert "page:" not in env[-1]["body"] and "name: Dana" in env[-1]["body"]


def test_research_tab():
    assert ("/", "Research") in __import__("app.main", fromlist=["NAV"]).NAV


def test_research_shows_project_boxes_and_popups(client):
    html = client.get("/").text
    assert "[[projects]]" not in html
    for t in content.projects():
        assert t["title"] in html
        for p in t["projects"]:
            assert f'data-pop="{p["id"]}"' in html and f'<dialog class="pop project-pop" id="{p["id"]}"' in html


def test_commit_shown_on_govern_not_in_footer(client):
    assert "<footer>" not in client.get("/").text
    assert "Deployed commit" in client.get("/govern").text


def test_govern_concurrent_sends_file_once(client, env, monkeypatch):
    import threading, time as _t
    slow = govern.github.create_issue

    def slow_create(title, body, label):
        _t.sleep(0.2)
        return slow(title, body, label)

    monkeypatch.setattr(govern.github, "create_issue", slow_create)
    results = []
    ts = [threading.Thread(target=lambda: results.append(
        govern.submit("Dana", "shnitzel", "same text", "1.2.3.4", False))) for _ in range(2)]
    for t in ts: t.start()
    for t in ts: t.join()
    assert len(env) == 1 and all(r["ok"] for r in results)
