from __future__ import annotations

import argparse
import csv
import sys

from common import SECTION_NAMES, ensure_project, read_text, resolve_project_path, split_script_sections


TEMPLATE_BY_SECTION = {
    "HOOK": "symbolic object close-up",
    "ACT 1": "old city night scene",
    "ACT 2": "no-face historical atmosphere",
    "HIDDEN DEED": "hidden deed scene",
    "SPIRITUAL REVERSAL": "repentance scene",
    "FINAL REMINDER": "masjid dawn scene",
    "CLOSING LINE": "symbolic object close-up",
}


def short_reference(text: str) -> str:
    cleaned = " ".join(text.split())
    if not cleaned:
        return "[Add approved voiceover reference]"
    return cleaned[:140] + ("..." if len(cleaned) > 140 else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an operational beat map and shotlist from an approved script.")
    parser.add_argument("project", help="Project path, for example projects/SD_001_The_Deed_Nobody_Saw")
    args = parser.parse_args()

    project_path = resolve_project_path(args.project)
    ensure_project(project_path)
    script_path = project_path / "01_Script" / "final_script.txt"
    shotlist_dir = project_path / "02_Shotlist"
    script_text = read_text(script_path)
    sections = split_script_sections(script_text)

    if not script_text.strip():
        print(f"ERROR: Script is empty: {script_path}", file=sys.stderr)
        return 1

    if not sections:
        sections = {"UNSECTIONED SCRIPT": script_text.strip()}

    beat_map_lines = [
        "# Emotional Beat Map",
        "",
        "Operational draft from approved script. Fill creative decisions manually.",
        "",
    ]

    rows = []
    shot_number = 1
    ordered_names = SECTION_NAMES if "UNSECTIONED SCRIPT" not in sections else ["UNSECTIONED SCRIPT"]
    for section_name in ordered_names:
        if section_name not in sections:
            continue
        body = sections[section_name]
        shot_id = f"SH{shot_number:03d}"
        template_key = TEMPLATE_BY_SECTION.get(section_name, "symbolic object close-up")
        beat_map_lines.extend(
            [
                f"## {section_name}",
                "",
                f"- Emotional purpose: [Define the approved emotional purpose for {section_name}.]",
                f"- Voiceover reference: {short_reference(body)}",
                "- Creative decision needed: Confirm visual approach manually.",
                "",
            ]
        )
        rows.append(
            {
                "shot_id": shot_id,
                "section": section_name,
                "emotional_purpose": f"[Define approved emotional purpose for {section_name}]",
                "voiceover_reference": short_reference(body),
                "template_key": template_key,
                "visual_placeholder": "[Add approved visual direction]",
                "restrictions": "Avoid sacred depictions, invented claims, and generic AI spectacle.",
            }
        )
        shot_number += 1

    shotlist_dir.mkdir(parents=True, exist_ok=True)
    (shotlist_dir / "emotional_beat_map.md").write_text("\n".join(beat_map_lines), encoding="utf-8")

    fieldnames = [
        "shot_id",
        "section",
        "emotional_purpose",
        "voiceover_reference",
        "template_key",
        "visual_placeholder",
        "restrictions",
    ]
    with (shotlist_dir / "shotlist.csv").open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote beat map and shotlist for {project_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
