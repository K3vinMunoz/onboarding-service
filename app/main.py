import secrets
from datetime import datetime, UTC

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.admin_auth import require_admin
from app.auth.client import require_client_app
from app.db import get_db
from app.models import ClientApp
from app.schemas.client_apps import (
    ClientAppCreate,
    ClientAppCreated,
    ClientAppOut,
    ClientAppRotateOut,
    ClientAppStatusUpdate,
)
from app.security import hash_api_key

app = FastAPI(title="Onboarding Service")


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


@app.post(
    "/client-apps",
    response_model=ClientAppCreated,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
async def create_client_app(payload: ClientAppCreate, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(ClientApp).where(ClientApp.name == payload.name))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Client app name already exists")

    api_key = generate_api_key()
    client = ClientApp(
        name=payload.name,
        api_key_hash=hash_api_key(api_key),
        api_key_prefix=api_key[:12],
        is_active=True,
    )
    db.add(client)
    await db.commit()
    await db.refresh(client)

    return ClientAppCreated(
        id=str(client.id),
        name=client.name,
        api_key=api_key,
        created_at=client.created_at.isoformat(),
    )


@app.get("/client-apps", response_model=list[ClientAppOut], dependencies=[Depends(require_admin)])
async def list_client_apps(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ClientApp).order_by(ClientApp.created_at.desc()))
    rows = res.scalars().all()
    return [
        ClientAppOut(
            id=str(c.id),
            name=c.name,
            is_active=c.is_active,
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat(),
        )
        for c in rows
    ]


@app.post(
    "/client-apps/{client_app_id}/rotate-key",
    response_model=ClientAppRotateOut,
    dependencies=[Depends(require_admin)],
)
async def rotate_client_app_key(client_app_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ClientApp).where(ClientApp.id == client_app_id))
    client = res.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="ClientApp not found")

    api_key = generate_api_key()
    client.api_key_hash = hash_api_key(api_key)
    client.api_key_prefix = api_key[:12]

    await db.commit()
    await db.refresh(client)

    return ClientAppRotateOut(
        id=str(client.id),
        name=client.name,
        api_key=api_key,
        rotated_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    )


@app.patch(
    "/client-apps/{client_app_id}/status",
    response_model=ClientAppOut,
    dependencies=[Depends(require_admin)],
)
async def set_client_app_status(
    client_app_id: str,
    payload: ClientAppStatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(ClientApp).where(ClientApp.id == client_app_id))
    client = res.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="ClientApp not found")

    client.is_active = payload.is_active
    await db.commit()
    await db.refresh(client)

    return ClientAppOut(
        id=str(client.id),
        name=client.name,
        is_active=client.is_active,
        created_at=client.created_at.isoformat(),
        updated_at=client.updated_at.isoformat(),
    )

@app.get("/me")
async def me(client: ClientApp = Depends(require_client_app)):
    return {
        "id": str(client.id),
        "name": client.name,
        "is_active": client.is_active,
    }
