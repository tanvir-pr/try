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

    def complete(self, note_id: int) -> Note:
        notes = self.store.load()
        for note in notes:
            if note.id == note_id:
                note.done = True
                self.store.save(notes)
                return note
        raise KeyError(f"no note with id {note_id}")

    def delete(self, note_id: int) -> None:
        notes = self.store.load()
        kept = [note for note in notes if note.id != note_id]
        if len(kept) == len(notes):
            raise KeyError(f"no note with id {note_id}")
        self.store.save(kept)