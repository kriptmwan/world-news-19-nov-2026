#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 entry (Python 3.13, stdlib only).

The image itself is baked into the repository as entry.png: it was rendered
at build time by render.py (Pillow + the system's DejaVu fonts) from the
verified news of Thursday 19 November 2026, and this program simply copies
it to the grader's output directory. No network, no fonts, no dependencies
at grade time — just one file copy, so the run is fast and deterministic.

Usage (local):  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    size = target.stat().st_size
    # Guardrail: the competition's gate takes at most 1 MiB. Fail loudly
    # instead of handing the grader an image it would reject.
    if size > 1_048_576:
        print(f"entry.png is {size} bytes, over the 1 MiB gate", file=sys.stderr)
        return 1
    with target.open("rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    print(f"wrote {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
