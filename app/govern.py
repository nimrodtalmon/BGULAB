"""The Govern button: name + password + text -> a GitHub issue.

Right password (or signed in): label `govern`, counted in the next round.
Wrong password: label `wrong-pass`, listed in the round, never acted on.
The password itself is never stored. The issue records the page the request
was sent from. The same text from the same name within a few minutes is
filed once (double clicks).
"""

import time
from datetime import datetime, timezone

from app import github
from app.gate import clean_name, password_ok

MAX_TEXT = 3000
RATE = (5, 600)  # at most 5 submissions per 10 minutes per address
DEDUPE = 300  # seconds: same name + same text is filed once
_recent: dict[str, list[float]] = {}
_sent: dict[tuple, tuple[float, int]] = {}


def _rate_ok(addr: str) -> bool:
    now = time.time()
    hits = [t for t in _recent.get(addr, []) if now - t < RATE[1]]
    _recent[addr] = hits
    if len(hits) >= RATE[0]:
        return False
    hits.append(now)
    return True


def clean_page(page: str) -> str:
    """The site address the request was sent from, or "" if it does not look like one."""
    page = (page or "").strip()
    if not page.startswith("/") or page.startswith("//") or any(c.isspace() for c in page):
        return ""
    return page[:200]


def submit(name: str, password: str, text: str, addr: str, signed_in: bool,
           page: str = "") -> dict:
    name = clean_name(name)
    text = text.strip()[:MAX_TEXT]
    if not name or not text:
        return {"ok": False, "message": "Please fill in your name and your request."}
    counted = signed_in or password_ok(password)
    key = (name.lower(), text, counted)
    now = time.time()
    if key in _sent and now - _sent[key][0] < DEDUPE:
        number = _sent[key][1]
        return {"ok": True, "counted": counted, "number": number,
                "message": f"Already filed as #{number}."}
    if not _rate_ok(addr):
        return {"ok": False, "message": "Too many submissions; try again in a few minutes."}
    label = "govern" if counted else "wrong-pass"
    first_line = text.splitlines()[0]
    title = first_line[:70] + ("…" if len(first_line) > 70 else "")
    filed = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    page = clean_page(page)
    body = (f"{text}\n\n---\nname: {name}\nfiled: {filed}\n"
            + (f"page: {page}\n" if page else "") + "via: Govern form\n")
    number = github.create_issue(title, body, label)
    if number is None:
        return {"ok": False, "message": "Could not file the request (GitHub unreachable). "
                                        "Nothing was saved; please try again later."}
    _sent[key] = (now, number)
    if counted:
        return {"ok": True, "counted": True, "number": number,
                "message": f"Filed as request #{number}. It will be decided in the next round."}
    return {"ok": True, "counted": False, "number": number,
            "message": f"Password not recognized. Recorded as #{number}, but it will not be counted."}
