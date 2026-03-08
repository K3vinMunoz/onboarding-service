import hmac
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import ClientApp
from app.security import hash_api_key

API_KEY_PREFIX_LEN = 12


async def require_client_app(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db),
) -> ClientApp:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")

    if len(x_api_key) < API_KEY_PREFIX_LEN:
        raise HTTPException(status_code=401, detail="Invalid API key")

    prefix = x_api_key[:API_KEY_PREFIX_LEN]
    computed_hash = hash_api_key(x_api_key)

    res = await db.execute(select(ClientApp).where(ClientApp.api_key_prefix == prefix))
    client = res.scalar_one_or_none()

    if not client:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not hmac.compare_digest(client.api_key_hash, computed_hash):
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not client.is_active:
        raise HTTPException(status_code=403, detail="Client app is inactive")

    return client
