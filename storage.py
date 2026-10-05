"""Read and write JSON files: processed email IDs and run reports."""

import json
from datetime import datetime
from pathlib import Path


def load_processed_ids(path: Path) -> set[str]:
    """Load processed Message-IDs. Missing file = first run = empty set."""
    try:
        with path.open(encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()
    except json.JSONDecodeError as e:
        # Fail loudly: treating a broken file as empty would re-process
        # every email and create duplicates in the database.
        raise RuntimeError(f"Corrupted state file {path}: {e}") from e


def save_json(path: Path, data) -> None:
    """Write JSON atomically: write a temp file, then replace the target."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        # ensure_ascii=False keeps Cyrillic readable; indent makes diffs readable
        json.dump(data, f, ensure_ascii=False, indent=2)
    # replace() is atomic: a crash mid-write never leaves a half-written file
    tmp_path.replace(path)


def save_processed_ids(path: Path, ids: set[str]) -> None:
    """Save processed Message-IDs (sorted, so the file is stable between runs)."""
    save_json(path, sorted(ids))


def save_run_report(path: Path, accepted: list[dict], skipped: list[tuple[str, str]]) -> None:
    """Save a summary of one run: what was accepted, what was skipped and why."""
    report = {
        "run_at": datetime.now().isoformat(timespec="seconds"),
        "accepted": [
            {"message_id": e["message_id"], "date": e["date"], "city": e["city"]}
            for e in accepted
        ],
        "skipped": [{"message_id": m, "reason": r} for m, r in skipped],
    }
    save_json(path, report)