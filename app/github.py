"""The only outside service: GitHub issues (requests) and commits (diffs).

Configured by GITHUB_REPO and GITHUB_TOKEN. Without them the site still
runs; requests cannot be filed and pending/diff views say so.
Reads are cached in memory for a minute (a cache only, never state).
"""

import os
import re
import time

import httpx

API = "https://api.github.com"
_cache: dict[str, tuple[float, object]] = {}


def config() -> tuple[str, str] | None:
    repo = os.environ.get("GITHUB_REPO", "").strip()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    return (repo, token) if repo and token else None


def _headers(token: str) -> dict:
    return {
        "authorization": f"Bearer {token}",
        "accept": "application/vnd.github+json",
        "user-agent": "bgulab",
    }


def _get(path: str, params: dict | None = None, ttl: int = 60):
    cfg = config()
    if not cfg:
        return None
    repo, token = cfg
    key = f"{path}?{params}"
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < ttl:
        return hit[1]
    r = httpx.get(f"{API}/repos/{repo}{path}", params=params, headers=_headers(token), timeout=15)
    r.raise_for_status()
    data = r.json()
    _cache[key] = (time.time(), data)
    return data


def _field(body: str, name: str) -> str:
    m = re.search(rf"^{name}: (.*)$", body or "", flags=re.M)
    return m.group(1).strip() if m else ""


def open_requests() -> list[dict] | None:
    """Open requests (label `govern`), oldest first. None if not configured."""
    try:
        issues = _get("/issues", {"labels": "govern", "state": "open", "per_page": 100})
    except httpx.HTTPError:
        return None
    if issues is None:
        return None
    out = []
    for i in sorted(issues, key=lambda i: i["number"]):
        body = i.get("body") or ""
        out.append(
            {
                "number": i["number"],
                "name": _field(body, "name") or "?",
                "filed": _field(body, "filed")[:10],
                "text": body.split("\n---\n")[0].strip(),
            }
        )
    return out


def create_issue(title: str, body: str, label: str) -> int | None:
    """File an issue; returns its number, or None if that failed."""
    cfg = config()
    if not cfg:
        return None
    repo, token = cfg
    url = f"{API}/repos/{repo}/issues"
    try:
        r = httpx.post(url, json={"title": title, "body": body, "labels": [label]},
                       headers=_headers(token), timeout=15)
        if r.status_code == 422:  # label missing and not creatable: file it bare
            r = httpx.post(url, json={"title": f"[{label}] {title}", "body": body},
                           headers=_headers(token), timeout=15)
        r.raise_for_status()
    except httpx.HTTPError:
        return None
    _cache.clear()
    return r.json()["number"]


def commit(sha: str) -> dict | None:
    if not re.fullmatch(r"[0-9a-f]{7,40}", sha):
        return None
    try:
        c = _get(f"/commits/{sha}", ttl=3600)
    except httpx.HTTPError:
        return None
    if not c:
        return None
    return {
        "sha": c["sha"],
        "message": c["commit"]["message"],
        "date": c["commit"]["author"]["date"][:10],
        "files": [{"name": f["filename"], "patch": f.get("patch", "(no text diff)")}
                  for f in c.get("files", [])],
    }
