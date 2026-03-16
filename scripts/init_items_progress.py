#!/usr/bin/env python3
"""Generate progress/items.json from items.json.

Each item gets a progress entry with:
- id, type: copied from items.json
- status: 'not_started' for formalizable items, 'not_applicable' for others
- lean_file: empty string (filled in Stage 3.1)
- aristotle_project_id: empty string (filled if escalated to Aristotle)
"""

import json
from pathlib import Path

FORMALIZABLE_TYPES = {"definition", "theorem", "lemma", "proposition", "corollary", "example"}

def main():
    repo_root = Path(__file__).resolve().parent.parent
    items_path = repo_root / "items.json"
    output_path = repo_root / "progress" / "items.json"

    with open(items_path) as f:
        items = json.load(f)

    progress = []
    for item in items:
        status = "not_started" if item["type"] in FORMALIZABLE_TYPES else "not_applicable"
        progress.append({
            "id": item["id"],
            "type": item["type"],
            "status": status,
            "lean_file": "",
            "aristotle_project_id": ""
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(progress, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(progress)} entries to {output_path}")

if __name__ == "__main__":
    main()
