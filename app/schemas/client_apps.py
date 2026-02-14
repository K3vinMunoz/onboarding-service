from pydantic import BaseModel, Field


class ClientAppCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class ClientAppCreated(BaseModel):
    id: str
    name: str
    api_key: str
    created_at: str


class ClientAppOut(BaseModel):
    id: str
    name: str
    is_active: bool
    created_at: str
    updated_at: str


class ClientAppRotateOut(BaseModel):
    id: str
    name: str
    api_key: str
    rotated_at: str


class ClientAppStatusUpdate(BaseModel):
    is_active: bool
