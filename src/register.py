"""Append-only AI use-case register (data/register.jsonl)."""
import json
from pathlib import Path

from src.triage import Triage

REGISTER = Path(__file__).resolve().parent.parent / "data" / "register.jsonl"


def add(result: Triage, path: Path = REGISTER) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(result.to_dict()) + "\n")


def load(path: Path = REGISTER) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
