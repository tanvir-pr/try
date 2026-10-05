from dataclasses import asdict, dataclass


@dataclass
class Note:
    id: int
    text: str
    created_at: str
    done: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict) -> "Note":
        return cls(
            id=int(raw["id"]),
            text=str(raw["text"]),
            created_at=str(raw["created_at"]),
            done=bool(raw.get("done", False)),
        )