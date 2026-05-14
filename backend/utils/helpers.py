import json
import os
from datetime import datetime
from uuid import UUID, uuid4


DB_PATH = os.path.abspath(
	os.path.join(os.path.dirname(__file__), "..", "database", "notes.json")
)


def _ensure_db_dir() -> None:
	os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def _normalize_notes(notes: list[dict]) -> list[dict]:
	updated = False
	for note in notes:
		note_id = note.get("id")
		try:
			UUID(str(note_id))
		except (TypeError, ValueError):
			note["id"] = str(uuid4())
			updated = True

		if not note.get("created_at"):
			note["created_at"] = datetime.utcnow().isoformat()
			updated = True
		if not note.get("updated_at"):
			note["updated_at"] = note.get("created_at")
			updated = True

	if updated:
		save_notes(notes)
	return notes


def load_notes() -> list[dict]:
	if not os.path.exists(DB_PATH):
		return []

	try:
		with open(DB_PATH, "r", encoding="utf-8") as file:
			data = json.load(file)
			if not isinstance(data, list):
				return []
			return _normalize_notes(data)
	except json.JSONDecodeError:
		return []


def save_notes(notes: list[dict]) -> None:
	_ensure_db_dir()

	with open(DB_PATH, "w", encoding="utf-8") as file:
		json.dump(notes, file, indent=2)
