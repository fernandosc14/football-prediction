from fastapi import HTTPException, Header
import os

ENDPOINT_API_KEY = os.environ.get("ENDPOINT_API_KEY")


def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if authorization != f"Bearer {ENDPOINT_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
