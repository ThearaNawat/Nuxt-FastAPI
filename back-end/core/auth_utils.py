from __future__ import annotations

from fastapi import Request


def extract_token(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        if token:
            return token

    for cookie_name in ("ACCESS_TOKEN", "TOKEN"):
        token = request.cookies.get(cookie_name)
        if token:
            return token

    return None
