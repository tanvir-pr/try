from datetime import datetime, timezone
from pathlib import Path

from notes.models import Note
from notes.store import NoteStore


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Notebook:
    def __init__(self, path: Path) -> None:
        self.store = NoteStore(path)

    def add(self, text: str) -> Note:
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("note text is empty")
        notes = self.store.load()
        next_id = max((note.id for note in notes), default=0) + 1
        note = Note(id=next_id, text=cleaned, created_at=_now())
        notes.append(note)
        self.store.save(notes)
        return note

    def list_notes(self) -> list[Note]:
        return self.store.load()