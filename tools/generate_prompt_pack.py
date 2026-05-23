from __future__ import annotations

import argparse
import csv
import sys

from common import ensure_project, load_yaml_json, read_text, repo_root, resolve_project_path


def build_prompt(row: dict[str, str], template: dict[str, str], style_guide: str) -> str:
    parts = [
        template.get("subject_action", "[Add approved subject/action]"),
        template.get("environment", "[Add approved environment]"),
        f"Emotion: {template.get('emotion', '[Add approved emotion]')}",
        f"Camera: {template.get('camera_movement', '[Add approved camera movement]')}",
        f"Lighting: {template.get('lighting', '[Add approved lighting]')}",
        f"Project style guide: {style_guide.strip() or '[Add approved visual style guide]'}",
        f"Shot placeholder: {row.get('visual_placeholder') or '[Add approved visual direction]'}",
    ]
    return " ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an operational visual prompt pack from a project shotlist.")
    parser.add_argument("project", help="Project path, for example projects/SD_001_The_Deed_Nobody_Saw")
    args = parser.parse_args()

    project_path = resolve_project_path(args.project)
    ensure_project(project_path)

    shotlist_path = project_path / "02_Shotlist" / "shotlist.csv"
    style_path = project_path / "02_Shotlist" / "visual_style_guide.txt"
    forbidden = load_yaml_json(repo_root() / "config" / "forbidden_visuals.yaml")
    templates = load_yaml_json(repo_root() / "config" / "prompt_templates.yaml").get("templates", {})
    style_guide = read_text(style_path)

    if not shotlist_path.exists():
        print(f"ERROR: Missing shotlist: {shotlist_path}", file=sys.stderr)
        return 1

    with shotlist_path.open(newline="", encoding="utf-8") as csvfile:
        rows = list(csv.DictReader(csvfile))

    if not rows:
        print(f"ERROR: Shotlist has no rows: {shotlist_path}", file=sys.stderr)
        return 1

    forbidden_items = forbidden.get("forbidden_or_high_risk_visuals", [])
    default_instruction = forbidden.get("default_instruction", "Avoid forbidden and high-risk visuals.")

    lines = [
        "# Prompt Pack",
        "",
        "Operational visual prompts for approved script material. Review manually before use.",
        "",
        "## Global Restrictions",
        "",
        default_instruction,
        "",
    ]
    for item in forbidden_items:
        lines.append(f"- {item}")
    lines.append("")

    for row in rows:
        template_key = row.get("template_key") or "symbolic object close-up"
        template = templates.get(template_key, {})
        prompt = build_prompt(row, template, style_guide)
        restrictions = [
            row.get("restrictions", "").strip(),
            template.get("restrictions", "").strip(),
            default_instruction,
        ]
        restrictions = [item for item in restrictions if item]

        lines.extend(
            [
                f"## {row.get('shot_id', '[shot ID]')}",
                "",
                f"- Emotional purpose: {row.get('emotional_purpose') or '[Add approved emotional purpose]'}",
                f"- Voiceover reference: {row.get('voiceover_reference') or '[Add approved voiceover reference]'}",
                f"- Template: {template_key}",
                "",
                "### Cinematic Visual Prompt",
                "",
                prompt,
                "",
                "### Restrictions",
                "",
            ]
        )
        for restriction in restrictions:
            lines.append(f"- {restriction}")
        lines.append("")

    output_path = project_path / "02_Shotlist" / "prompt_pack.md"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote prompt pack: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
