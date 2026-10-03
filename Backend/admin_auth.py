import os
import hashlib
import hmac

from dotenv import load_dotenv
from fastapi import Request, HTTPException

load_dotenv()

ADMIN_SECRET = os.getenv("ADMIN_SECRET")

if not ADMIN_SECRET:
    raise RuntimeError("ADMIN_SECRET is missing in .env")


def create_admin_token():
    return hmac.new(
        ADMIN_SECRET.encode(),
        b"AI_CAREER_HUB_ADMIN",
        hashlib.sha256
    ).hexdigest()


def verify_admin(request: Request):
    token = request.cookies.get("admin_token")

    if not token:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    expected_token = create_admin_token()

    if not hmac.compare_digest(
        token,
        expected_token
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid admin access"
        )

    return True