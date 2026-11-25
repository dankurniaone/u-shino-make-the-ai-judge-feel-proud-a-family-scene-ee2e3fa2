#!/usr/bin/env python3
"""Make the AI Judge Feel Proud: A Family Scene — make.fun entry.

Writes one short family scene (one or two lines, at most 280
characters) to /output/entry.txt. The scene is warm, funny and
heartfelt: a small domestic moment with one telling detail.
"""

import argparse
import sys
from pathlib import Path

# Tournament record (specificity / surprise / freshness, 1-5):
#   wobbly table, folded cardboard underneath — 5/4/4 = 13
#   brother eats Dad's dumpling, blames the dog — 5/4/4 = 13
#   Grandma sets a place for Grandpa — 5/3/3 = 11
#   burned rice, "Good. Now it's yours." — 5/5/4 = 14 (winner)
#   Dad irons his good shirt, photo nobody takes — 5/4/5 = 14
#   lights out, ghost stories, best night — 4/4/4 = 12
#   fridge drawing, cat as big as the house — 5/4/4 = 13
# The winner and the runner-up tied at 14; the winner took the
# tie-break on the judge's second criterion, genuine affection in
# the turn, where the burned rice becomes the point, not the failure.
SCENE = (
    "Mum taught me her recipe by taste, not measurements, "
    "then watched me burn the rice and said, \"Good. Now it's yours.\""
)

MAX_CHARS = 280


def check_scene(text):
    """Return a list of gate problems; empty means the scene is valid."""
    problems = []
    if not text or not text.strip():
        problems.append("scene is empty or only whitespace")
    if len(text) > MAX_CHARS:
        problems.append(
            "scene is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if text != text.strip():
        problems.append("scene has leading or trailing whitespace")
    return problems


def write_scene(output_path):
    text = SCENE
    problems = check_scene(text)
    if problems:
        for problem in problems:
            print("gate FAIL: %s" % problem, file=sys.stderr)
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = output_path.write_text(text, encoding="utf-8")
    print("wrote %d bytes to %s" % (written, output_path))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="/output/entry.txt",
        help="where to write the scene (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the scene against the gate without writing",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write to a temp file and verify the bytes read back",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "entry.txt"
            if write_scene(target) != 0:
                return 1
            read_back = target.read_text(encoding="utf-8")
            if read_back != SCENE:
                print("self-test FAIL: bytes read back differ", file=sys.stderr)
                return 1
            print("self-test OK: %d bytes round-trip" % len(read_back))
            return 0

    if args.check:
        problems = check_scene(SCENE)
        if problems:
            for problem in problems:
                print("gate FAIL: %s" % problem, file=sys.stderr)
            return 1
        print("gate OK: %d characters, 1 line" % len(SCENE))
        print("scene: %s" % SCENE)
        return 0

    return write_scene(Path(args.output))


if __name__ == "__main__":
    raise SystemExit(main())
