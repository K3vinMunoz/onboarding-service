import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

ADMIN_KEY = os.getenv("ADMIN_BOOTSTRAP_KEY")
if not ADMIN_KEY:
    raise RuntimeError("ADMIN_BOOTSTRAP_KEY no está definido en .env")


def require_admin(x_admin_key: str | None = Header(default=None, alias="X-Admin-Key")):
    if not x_admin_key or x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    return True
