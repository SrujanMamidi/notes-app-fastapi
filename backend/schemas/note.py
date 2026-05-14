

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: str = ""


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class Note(NoteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime