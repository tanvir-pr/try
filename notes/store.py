import json
from pathlib import Path

from notes.models import Note


class NoteStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[Note]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Note.from_dict(item) for item in data]

    def save(self, notes: list[Note]) -> None:
        payload = [note.to_dict() for note in notes]
        text = json.dumps(payload, indent=2) + "\n"
        self.path.write_text(text, encoding="utf-8")