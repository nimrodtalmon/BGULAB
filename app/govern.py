"""The Govern button: name + password + text -> a GitHub issue.

Right password (or a member cookie): label `govern`, counted in the next round.
Wrong password: label `wrong-pass`, listed in the round, never acted on.
The password itself is never stored.
"""

import time
from datetime import datetime, timezone

from app import github
from app.gate import password_ok

MAX_TEXT = 3000
MAX_NAME = 60
RATE = (5, 600)  # at most 5 submissions per 10 minutes per address
_recent: dict[str, list[float]] = {}


def _rate_ok(addr: str) -> bool:
    now = time.time()
    hits = [t for t in _recent.get(addr, []) if now - t < RATE[1]]
    _recent[addr] = hits
    if len(hits) >= RATE[0]:
        return False
    hits.append(now)
    return True


def submit(name: str, password: str, text: str, addr: str, member: bool) -> dict:
    name = " ".join(name.split())[:MAX_NAME]
    text = text.strip()[:MAX_TEXT]
    if not name or not text:
        return {"ok": False, "message": "Please fill in your name and your request."}
    if not _rate_ok(addr):
        return {"ok": False, "message": "Too many submissions; try again in a few minutes."}
    counted = member or password_ok(password)
    label = "govern" if counted else "wrong-pass"
    first_line = text.splitlines()[0]
    title = first_line[:70] + ("…" if len(first_line) > 70 else "")
    filed = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = f"{text}\n\n---\nname: {name}\nfiled: {filed}\nvia: Govern form\n"
    number = github.create_issue(title, body, label)
    if number is None:
        return {"ok": False, "message": "Could not file the request (GitHub unreachable). "
                                        "Nothing was saved; please try again later."}
    if counted:
        return {"ok": True, "number": number,
                "message": f"Filed as request #{number}. It will be decided in the next round."}
    return {"ok": True, "number": number,
            "message": f"Password not recognized. Recorded as #{number}, but it will not be counted."}
