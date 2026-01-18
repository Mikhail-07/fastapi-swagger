from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TermCreate(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100, description="Ключевое слово термина")
    description: str = Field(..., min_length=1, description="Описание термина")


class TermUpdate(BaseModel):
    keyword: Optional[str] = Field(None, min_length=1, max_length=100, description="Ключевое слово термина")
    description: Optional[str] = Field(None, min_length=1, description="Описание термина")


class TermResponse(BaseModel):
    id: int
    keyword: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

