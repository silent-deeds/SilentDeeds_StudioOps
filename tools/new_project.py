from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROJECT_FOLDERS = [
    "01_Script",
    "02_Shotlist",
    "03_Voiceover",
    "04_Visuals/inbox",
    "04_Visuals/anchor_shots",
    "04_Visuals/supporting_shots",
    "04_Visuals/rejected",
    "05_Sound",
    "06_FinalCut",
    "07_Thumbnail",
    "08_Shorts",
    "09_Upload",
    "10_Analytics",
]

STARTER_FILES = {
    "01_Script/final_script.txt": "",
    "01_Script/islamic_accuracy_notes.md": "# Islamic Accuracy Notes\n\n- Human review required.\n",
    "02_Shotlist/shotlist.csv": "shot_id,section,emotional_purpose,voiceover_reference,template_key,visual_placeholder,restrictions\n",
    "02_Shotlist/visual_style_guide.txt": "Describe approved visual style choices here. Keep guidance operational and restrained.\n",
    "03_Voiceover/voice_direction.txt": "Voice direction notes:\n- Calm\n- Sincere\n- Restrained\n",
    "09_Upload/title_options.txt": "",
    "09_Upload/description.txt": "",
    "09_Upload/pinned_comment.txt": "",
    "10_Analytics/48h_review.md": "# 48h Review\n\n- Views:\n- Retention:\n- Comments:\n- Lessons:\n",
    "10_Analytics/7d_review.md": "# 7d Review\n\n- Views:\n- Retention:\n- Comments:\n- Lessons:\n",
    "10_Analytics/28d_review.md": "# 28d Review\n\n- Views:\n- Retention:\n- Comments:\n- Lessons:\n",
}


def slugify_title(title: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title.strip())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "Untitled"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Silent Deeds production project.")
    parser.add_argument("project_id", help="Project ID, for example SD_001")
    parser.add_argument("title", help="Approved project title")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    projects_root = repo_root / "projects"
    project_name = f"{args.project_id}_{slugify_title(args.title)}"
    project_path = projects_root / project_name

    if project_path.exists():
        print(f"ERROR: Project already exists: {project_path}", file=sys.stderr)
        return 1

    try:
        for folder in PROJECT_FOLDERS:
            (project_path / folder).mkdir(parents=True, exist_ok=False)
        for relative_path, content in STARTER_FILES.items():
            target = project_path / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Could not create project: {exc}", file=sys.stderr)
        return 1

    print(f"Created project: {project_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
