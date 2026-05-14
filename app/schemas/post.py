from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str
    content: str


class PostPatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
