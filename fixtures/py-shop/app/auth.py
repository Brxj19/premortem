"""Authentication dependencies."""
from fastapi import Depends, HTTPException, Header


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token = authorization[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    return {"user_id": 1, "email": "user@example.com"}
