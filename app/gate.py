"""Shared-password gate.

One password (GOVERN_PASS) for the whole lab. Entering it sets a signed
cookie; the cookie carries a fingerprint of the password, so changing the
password logs everyone out. The password itself is never stored or logged.
"""

import hashlib
import hmac
import os

from fastapi import Request
from itsdangerous import BadSignature, URLSafeTimedSerializer

COOKIE = "bgulab_member"
MAX_AGE = 30 * 24 * 3600  # 30 days


def _password() -> str:
    return os.environ.get("GOVERN_PASS", "").strip()


def _fingerprint() -> str:
    return hashlib.sha256(_password().encode()).hexdigest()[:12]


def _serializer() -> URLSafeTimedSerializer:
    secret = os.environ.get("SESSION_SECRET", "") or "dev-only-secret"
    return URLSafeTimedSerializer(secret, salt="member")


def password_ok(given: str) -> bool:
    expected = _password()
    return bool(expected) and hmac.compare_digest(given.strip().encode(), expected.encode())


def member_cookie() -> str:
    return _serializer().dumps(_fingerprint())


def is_member(request: Request) -> bool:
    token = request.cookies.get(COOKIE)
    if not token or not _password():
        return False
    try:
        return _serializer().loads(token, max_age=MAX_AGE) == _fingerprint()
    except BadSignature:
        return False
