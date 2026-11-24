#!/usr/bin/env python3
"""Entry for make.fun bounty 'Sum up 23 November's world news in one image'.

Writes one image to /output/entry.png: a deterministic news poster
('The World in One Page', Monday 23 November 2026) rendered from the real
headlines of that day. The image is committed in this repository as
entry.png (built by build_image.py from the researched headlines) and this
program copies it byte-identically on every run.

Standard library only. No network, no randomness, no timestamps.
Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
