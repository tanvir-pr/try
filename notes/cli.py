import argparse
from pathlib import Path

from notes.service import Notebook

DEFAULT_PATH = Path(".notes.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="notes", description="Local scratch notes")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_PATH,
        help="JSON file used to store notes",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="save a note")
    add.add_argument("text")

    listing = sub.add_parser("list", help="show notes")
    listing.add_argument("--open", action="store_true", help="hide notes already done")

    done = sub.add_parser("done", help="mark a note done")
    done.add_argument("id", type=int)

    remove = sub.add_parser("delete", help="remove a note")
    remove.add_argument("id", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    book = Notebook(args.file)

    if args.command == "add":
        note = book.add(args.text)
        print(f"added #{note.id}")
        return 0

    if args.command == "list":
        notes = book.list_notes(include_done=not args.open)
        if not notes:
            print("no notes yet")
            return 0
        for note in notes:
            mark = "x" if note.done else " "
            print(f"[{mark}] {note.id}: {note.text}")
        return 0

    if args.command == "done":
        note = book.complete(args.id)
        print(f"done #{note.id}")
        return 0

    if args.command == "delete":
        book.delete(args.id)
        print(f"deleted #{args.id}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())