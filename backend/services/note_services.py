from datetime import datetime
from uuid import UUID, uuid4

from schemas.note import NoteCreate, NoteUpdate
from utils.helpers import load_notes, save_notes


def get_all_notes() -> list[dict]:
    return load_notes()


def _find_note_index(notes: list[dict], note_id: UUID) -> int | None:
    note_id_str = str(note_id)
    for index, note in enumerate(notes):
        if note.get("id") == note_id_str:
            return index
    return None


def create_note(note: NoteCreate) -> dict:
    notes = load_notes()
    timestamp = datetime.utcnow().isoformat()

    new_note = {
        "id": str(uuid4()),
        "title": note.title,
        "content": note.content or "",
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    notes.append(new_note)
    save_notes(notes)
    return new_note


def get_note(note_id: UUID) -> dict | None:
    notes = load_notes()
    index = _find_note_index(notes, note_id)
    return notes[index] if index is not None else None


def update_note(note_id: UUID, note_update: NoteUpdate) -> dict | None:
    notes = load_notes()
    index = _find_note_index(notes, note_id)
    if index is None:
        return None

    existing = notes[index]
    if note_update.title is not None:
        existing["title"] = note_update.title
    if note_update.content is not None:
        existing["content"] = note_update.content

    existing["updated_at"] = datetime.utcnow().isoformat()
    notes[index] = existing
    save_notes(notes)
    return existing


def delete_note(note_id: UUID) -> bool:
    notes = load_notes()
    index = _find_note_index(notes, note_id)
    if index is None:
        return False

    notes.pop(index)
    save_notes(notes)
    return True


def search_notes(query: str) -> list[dict]:
    notes = load_notes()
    term = query.strip().lower()
    if not term:
        return notes

    results = []
    for note in notes:
        title = str(note.get("title", "")).lower()
        content = str(note.get("content", "")).lower()
        if term in title or term in content:
            results.append(note)

    return results
