"""Entry point for the news-image-20261117 bounty (Python 3.13, stdlib only).

The image is rendered ahead of time by draw_news.py from the researched
news data in news.json and shipped in this repository as entry.png. This
program only copies that image to the grader's output directory, so both
grading runs write byte-identical output with no network access.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
