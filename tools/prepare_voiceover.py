from __future__ import annotations

import argparse
import sys

from common import SECTION_ORDER, ensure_project, read_text, resolve_project_path, split_script_sections


def main() -> int:
    parser = argparse.ArgumentParser(description="Split approved script sections into voiceover text files.")
    parser.add_argument("project", help="Project path, for example projects/SD_001_The_Deed_Nobody_Saw")
    args = parser.parse_args()

    project_path = resolve_project_path(args.project)
    ensure_project(project_path)
    script_path = project_path / "01_Script" / "final_script.txt"
    script_text = read_text(script_path)

    if not script_text.strip():
        print(f"ERROR: Script is empty: {script_path}", file=sys.stderr)
        return 1

    sections = split_script_sections(script_text)
    if not sections:
        print("ERROR: No approved section headings found. Voiceover files were not created.", file=sys.stderr)
        return 1

    output_dir = project_path / "03_Voiceover" / "sections"
    output_dir.mkdir(parents=True, exist_ok=True)

    for _, filename in SECTION_ORDER:
        existing = output_dir / filename
        if existing.exists():
            existing.unlink()

    written = []
    for section_name, filename in SECTION_ORDER:
        body = sections.get(section_name)
        if not body:
            continue
        target = output_dir / filename
        target.write_text(body.strip() + "\n", encoding="utf-8")
        written.append(filename)

    print(f"Wrote {len(written)} voiceover section file(s): {', '.join(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
