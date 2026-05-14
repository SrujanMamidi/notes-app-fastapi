from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from schemas.note import Note, NoteCreate, NoteUpdate
from services.note_services import (
	create_note,
	delete_note,
	get_all_notes,
	get_note,
	search_notes,
	update_note,
)

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=list[Note])
def list_notes():
	return get_all_notes()


@router.get("/search", response_model=list[Note])
def search_notes_route(q: str = Query("", description="Search by title or content")):
	return search_notes(q)


@router.get("/{note_id}", response_model=Note)
def get_note_route(note_id: UUID):
	note = get_note(note_id)
	if note is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Note not found",
		)
	return note

@router.post("/", response_model=Note)
def add_note(note: NoteCreate):
	return create_note(note)


@router.patch("/{note_id}", response_model=Note)
def update_note_route(note_id: UUID, note_update: NoteUpdate):
	updated = update_note(note_id, note_update)
	if updated is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Note not found",
		)
	return updated


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_route(note_id: UUID):
	deleted = delete_note(note_id)
	if not deleted:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Note not found",
		)
