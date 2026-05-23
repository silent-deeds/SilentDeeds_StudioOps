from __future__ import annotations

import json
import re
from pathlib import Path


SECTION_ORDER = [
    ("HOOK", "01_hook.txt"),
    ("ACT 1", "02_act_1.txt"),
    ("ACT 2", "03_act_2.txt"),
    ("HIDDEN DEED", "04_hidden_deed.txt"),
    ("SPIRITUAL REVERSAL", "05_spiritual_reversal.txt"),
    ("FINAL REMINDER", "06_final_reminder.txt"),
    ("CLOSING LINE", "07_closing_line.txt"),
]

SECTION_NAMES = [name for name, _ in SECTION_ORDER]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_project_path(project_arg: str) -> Path:
    path = Path(project_arg)
    if not path.is_absolute():
        path = repo_root() / path
    return path.resolve()


def load_yaml_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing config file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Could not parse {path}: {exc}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"Missing required file: {path}")


def section_heading_pattern() -> re.Pattern[str]:
    escaped = [re.escape(name) for name in SECTION_NAMES]
    return re.compile(r"^\s*(?P<heading>" + "|".join(escaped) + r")\s*:?\s*$", re.IGNORECASE)


def split_script_sections(script_text: str) -> dict[str, str]:
    pattern = section_heading_pattern()
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in script_text.splitlines():
        match = pattern.match(line)
        if match:
            heading = normalize_section_name(match.group("heading"))
            current = heading
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line)

    return {name: "\n".join(lines).strip() for name, lines in sections.items() if "\n".join(lines).strip()}


def normalize_section_name(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value.strip().upper())
    for name in SECTION_NAMES:
        if normalized == name:
            return name
    return normalized


def ensure_project(project_path: Path) -> None:
    if not project_path.exists() or not project_path.is_dir():
        raise SystemExit(f"Project folder does not exist: {project_path}")
