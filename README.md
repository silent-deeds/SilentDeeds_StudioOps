# SilentDeeds_StudioOps

SilentDeeds_StudioOps is a local operations toolkit for Silent Deeds, a cinematic Islamic storytelling brand. It automates repeatable production tasks after a script has already been approved: creating project folders, splitting approved scripts into production sections, preparing voiceover files, assembling visual prompt packs, and validating upload packages.

This toolkit does not write final stories, make religious rulings, invent Islamic claims, fabricate sources, or replace creative judgment. It is a studio operations helper, not a scholar, writer, editor, or director.

## Setup

Use Python 3.10 or newer.

No heavy dependencies are required. The current tools use only the Python standard library.

```bash
python --version
```

## Create a New Video Project

From the repository root:

```bash
python tools/new_project.py SD_001 "The Deed Nobody Saw"
```

This creates:

```text
projects/SD_001_The_Deed_Nobody_Saw/
```

with the standard production folders and starter files for script, shotlist, voiceover, visuals, upload, and analytics.

## Script Usage

Create a project:

```bash
python tools/new_project.py SD_001 "The Deed Nobody Saw"
```

Create a beat map and starter shotlist from an approved final script:

```bash
python tools/script_to_beats.py projects/SD_001_The_Deed_Nobody_Saw
```

Generate a conservative visual prompt pack from the shotlist and style guide:

```bash
python tools/generate_prompt_pack.py projects/SD_001_The_Deed_Nobody_Saw
```

Split approved script sections into voiceover files:

```bash
python tools/prepare_voiceover.py projects/SD_001_The_Deed_Nobody_Saw
```

Validate upload readiness:

```bash
python tools/validate_upload_package.py projects/SD_001_The_Deed_Nobody_Saw
```

For historical projects or AI-assisted visuals:

```bash
python tools/validate_upload_package.py projects/SD_001_The_Deed_Nobody_Saw --project-type historical --ai-visuals true
```

## Recommended Workflow

1. Approve the final script outside this toolkit.
2. Create the project folder with `new_project.py`.
3. Paste the approved script into `01_Script/final_script.txt`.
4. Add source and accuracy notes manually where needed.
5. Run `script_to_beats.py` to create operational beat and shotlist placeholders.
6. Fill or refine the visual style guide manually.
7. Run `generate_prompt_pack.py`.
8. Run `prepare_voiceover.py`.
9. Produce visuals, sound, edit, thumbnail, and upload copy.
10. Run `validate_upload_package.py` before publishing.

## Approved Section Headings

The sectioning tools only recognize these headings:

- `HOOK`
- `ACT 1`
- `ACT 2`
- `HIDDEN DEED`
- `SPIRITUAL REVERSAL`
- `FINAL REMINDER`
- `CLOSING LINE`

If headings are missing, the tools create conservative placeholders rather than inventing creative decisions.
