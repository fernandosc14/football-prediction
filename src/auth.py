from fastapi import HTTPException, Header, status
import os

ENDPOINT_API_KEY = os.environ.get("ENDPOINT_API_KEY")
if not ENDPOINT_API_KEY:
    raise RuntimeError("ENDPOINT_API_KEY environment variable is not set")


def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing"
        )
    parts = authorization.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format"
        )
    token = parts[1]
    if token != ENDPOINT_API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return True
