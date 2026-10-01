"""Shared-password sign-in.

One password (GOVERN_PASS) for the whole lab. Signing in once (name +
password) sets a signed cookie for a year; it carries the name (self-declared)
and a fingerprint of the password, so changing the password signs everyone
out. The password itself is never stored or logged.
"""

import hashlib
import hmac
import os

from fastapi import Request
from itsdangerous import BadSignature, URLSafeTimedSerializer

COOKIE = "bgulab_lab"
MAX_AGE = 365 * 24 * 3600  # one year
MAX_NAME = 60


def _password() -> str:
    return os.environ.get("GOVERN_PASS", "").strip()


def _fingerprint() -> str:
    return hashlib.sha256(_password().encode()).hexdigest()[:12]


def _serializer() -> URLSafeTimedSerializer:
    secret = os.environ.get("SESSION_SECRET", "") or "dev-only-secret"
    return URLSafeTimedSerializer(secret, salt="lab")


def clean_name(name: str) -> str:
    return " ".join(name.split())[:MAX_NAME]


def password_ok(given: str) -> bool:
    expected = _password()
    return bool(expected) and hmac.compare_digest(given.strip().encode(), expected.encode())


def lab_cookie(name: str) -> str:
    return _serializer().dumps({"f": _fingerprint(), "n": clean_name(name)})


def lab_name(request: Request) -> str | None:
    """The signed-in member's name, or None if not signed in."""
    token = request.cookies.get(COOKIE)
    if not token or not _password():
        return None
    try:
        data = _serializer().loads(token, max_age=MAX_AGE)
    except BadSignature:
        return None
    if not isinstance(data, dict) or data.get("f") != _fingerprint():
        return None
    return data.get("n") or None
