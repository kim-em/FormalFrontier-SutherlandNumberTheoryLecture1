#!/usr/bin/env python3
"""Check that items.json provides complete, gap-free, overlap-free coverage of all page files."""

import json
import sys
from pathlib import Path

def main():
    root = Path(__file__).parent.parent
    items_path = root / "items.json"
    pages_dir = root / "pages"

    with open(items_path) as f:
        items = json.load(f)

    # Determine page order from filenames
    page_files = sorted(pages_dir.glob("*.md"), key=lambda p: p.name)
    page_files = [p for p in page_files if p.name != "CONVENTIONS.md"]

    # Map page name -> line count
    page_lines = {}
    page_order = []
    for pf in page_files:
        name = pf.stem  # e.g. "1", "2", "backmatter-1"
        with open(pf) as f:
            lines = f.readlines()
        page_lines[name] = len(lines)
        page_order.append(name)

    print(f"Pages found: {page_order}")
    print(f"Line counts: {page_lines}")
    print(f"Items found: {len(items)}")
    print()

    # Build a coverage map: for each page, track which lines are covered
    coverage = {}
    for name in page_order:
        coverage[name] = [None] * (page_lines[name] + 1)  # 1-indexed

    errors = []

    for item in items:
        item_id = item["id"]
        sp = item["start_page"]
        ep = item["end_page"]
        sl = item["start_line"]
        el = item["end_line"]

        if sp not in page_lines:
            errors.append(f"Item {item_id}: start_page '{sp}' not found")
            continue
        if ep not in page_lines:
            errors.append(f"Item {item_id}: end_page '{ep}' not found")
            continue

        # Determine which pages this item spans
        sp_idx = page_order.index(sp)
        ep_idx = page_order.index(ep)

        if ep_idx < sp_idx:
            errors.append(f"Item {item_id}: end_page '{ep}' comes before start_page '{sp}'")
            continue

        for pi in range(sp_idx, ep_idx + 1):
            page_name = page_order[pi]
            max_line = page_lines[page_name]

            if pi == sp_idx and pi == ep_idx:
                # Same page
                line_start = sl
                line_end = el
            elif pi == sp_idx:
                # First page of multi-page item
                line_start = sl
                line_end = max_line
            elif pi == ep_idx:
                # Last page of multi-page item
                line_start = 1
                line_end = el
            else:
                # Middle page (entire page)
                line_start = 1
                line_end = max_line

            if line_start < 1 or line_end > max_line:
                errors.append(
                    f"Item {item_id}: line range {line_start}-{line_end} "
                    f"out of bounds for page '{page_name}' (1-{max_line})"
                )
                continue

            if line_end < line_start:
                errors.append(
                    f"Item {item_id}: end_line {line_end} < start_line {line_start} "
                    f"on page '{page_name}'"
                )
                continue

            for line in range(line_start, line_end + 1):
                if coverage[page_name][line] is not None:
                    errors.append(
                        f"OVERLAP: page '{page_name}' line {line} claimed by both "
                        f"'{coverage[page_name][line]}' and '{item_id}'"
                    )
                else:
                    coverage[page_name][line] = item_id

    # Check for gaps
    for page_name in page_order:
        max_line = page_lines[page_name]
        for line in range(1, max_line + 1):
            if coverage[page_name][line] is None:
                errors.append(f"GAP: page '{page_name}' line {line} not covered by any item")

    if errors:
        print("ERRORS FOUND:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("CONTIGUITY CHECK PASSED")
        print("All lines in all pages are covered by exactly one item.")
        print("No gaps or overlaps detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
