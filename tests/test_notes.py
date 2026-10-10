import tempfile
import unittest
from pathlib import Path

from notes.service import Notebook


class NotebookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "notes.json"
        self.book = Notebook(self.path)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_add_and_list(self) -> None:
        self.book.add("buy milk")
        notes = self.book.list_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, "buy milk")
        self.assertFalse(notes[0].done)

    def test_empty_text_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.book.add("   ")

    def test_complete_and_delete(self) -> None:
        note = self.book.add("read a chapter")
        self.book.complete(note.id)
        self.assertTrue(self.book.list_notes()[0].done)
        self.book.delete(note.id)
        self.assertEqual(self.book.list_notes(), [])

    def test_missing_id(self) -> None:
        with self.assertRaises(KeyError):
            self.book.complete(99)


if __name__ == "__main__":
    unittest.main()