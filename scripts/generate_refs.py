#!/usr/bin/env python3
"""Generate .refs.md files for formalizable items (Stage 2.7)."""
import json
import os

def main():
    # Load data
    with open("progress/items.json") as f:
        items = json.load(f)
    with open("research/mathlib-coverage.json") as f:
        mathlib = {e["item_id"]: e for e in json.load(f)}
    with open("research/external-coverage.json") as f:
        ext_cov = {e["ext_id"]: e for e in json.load(f)}
    with open("dependencies/external.json") as f:
        ext_deps = json.load(f)

    # Build reverse index: item_id -> list of ext deps
    item_ext_deps = {}
    for dep in ext_deps:
        for item_id in dep.get("used_by", []):
            item_ext_deps.setdefault(item_id, []).append(dep)

    # Formalizable items (not_applicable items are excluded)
    formalizable = [it for it in items if it["status"] != "not_applicable"]
    manifest = []

    for item in formalizable:
        item_id = item["id"]
        mc = mathlib.get(item_id)
        eds = item_ext_deps.get(item_id, [])

        has_mathlib = mc and mc.get("mathlib_matches")
        has_ext = bool(eds)

        if not has_mathlib and not has_ext:
            manifest.append({"item_id": item_id, "has_refs": False, "reason": "no_references"})
            continue

        lines = [f"# References for {item_id}", ""]

        if has_mathlib:
            coverage = mc["coverage"]
            lines.append("## Mathlib Coverage")
            lines.append("")
            lines.append(f"**Status:** {coverage}")
            lines.append("")
            for m in mc["mathlib_matches"]:
                name = m["name"]
                match_type = m["type"]
                notes = m["notes"]
                lines.append(f"### `{name}`")
                lines.append("")
                lines.append(f"- **Match type:** {match_type}")
                lines.append(f"- **Notes:** {notes}")
                lines.append("")

        if has_ext:
            lines.append("## External Dependencies")
            lines.append("")
            for dep in eds:
                ext_id = dep["id"]
                ec = ext_cov.get(ext_id, {})
                ec_matches = ec.get("mathlib_matches", [])
                ec_coverage = ec.get("coverage", "unknown")
                description = dep["description"]
                category = dep["category"]
                lines.append(f"### `{ext_id}`")
                lines.append("")
                lines.append(f"- **Description:** {description}")
                lines.append(f"- **Category:** {category}")
                lines.append(f"- **Mathlib coverage:** {ec_coverage}")
                if ec_matches:
                    for ecm in ec_matches:
                        ecm_name = ecm["name"]
                        ecm_type = ecm["type"]
                        ecm_notes = ecm["notes"]
                        lines.append(f"  - `{ecm_name}` ({ecm_type}): {ecm_notes}")
                lines.append("")

        # Write file
        filename = item_id.replace("/", "_") + ".refs.md"
        filepath = os.path.join("blobs", filename)
        with open(filepath, "w") as f:
            f.write("\n".join(lines))

        manifest.append({"item_id": item_id, "has_refs": True, "refs_file": f"blobs/{filename}"})
        print(f"Created {filepath}")

    # Write manifest
    with open("research/refs-manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(f"\nCreated research/refs-manifest.json with {len(manifest)} entries")
    print(f"  - {sum(1 for m in manifest if m['has_refs'])} items with refs")
    print(f"  - {sum(1 for m in manifest if not m['has_refs'])} items without refs")

if __name__ == "__main__":
    main()
