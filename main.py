#!/usr/bin/env python3
"""Duskline Placard — one-line museum label from the year 3000.

The program writes a single 164-character placard line to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` as UTF-8, with no trailing newline.

It uses only the Python standard library, touches no network, clock or
randomness, and never writes inside this repository: if the requested
output directory resolves to the repository itself — directly, or
through a symlink — or cannot be written, it prints an error and exits
without writing anything.
"""

import os
import sys

# The placard line, exactly as it must appear in entry.txt.
PLACARD = (
    "Sticky Note, c. 2019. Yellowed fragment, adhesive reverse, "
    "inscribed 'CALL DAVE BACK'. Its purpose is lost; its urgency is "
    "eternal. Gift of the Accounts Department."
)

FILENAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def _fail(message):
    """Print an error to stderr and return a non-zero exit code."""
    print("error: " + message, file=sys.stderr)
    return 1


def _repo_root():
    """Absolute path of the directory holding this script."""
    return os.path.dirname(os.path.abspath(__file__))


def _is_inside(path, root):
    """True when ``path`` is ``root`` itself or lives beneath it."""
    path = os.path.realpath(path)
    root = os.path.realpath(root)
    return path == root or path.startswith(root + os.sep)


def _validate_text(text):
    """Check the placard line against the contest's text rules."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return "placard must be %d-%d characters, got %d" % (
            MIN_CHARS,
            MAX_CHARS,
            len(text),
        )
    if "\n" in text or "\r" in text:
        return "placard must be a single line"
    for ch in text:
        if ord(ch) < 0x20 and ch not in ("\t",):
            return "placard contains a control character"
    return None


def _place():
    problem = _validate_text(PLACARD)
    if problem:
        return _fail(problem)

    try:
        payload = PLACARD.encode("utf-8")
    except UnicodeEncodeError as exc:
        return _fail("placard is not valid UTF-8: %s" % exc)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    root = _repo_root()
    if _is_inside(out_dir, root):
        return _fail(
            "refusing to write into the repository directory: %r" % out_dir
        )

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        return _fail("cannot create output directory %r: %s" % (out_dir, exc))

    target = os.path.join(out_dir, FILENAME)
    try:
        with open(target, "wb") as handle:
            handle.write(payload)
    except OSError as exc:
        return _fail("cannot write %r: %s" % (target, exc))

    try:
        if os.path.getsize(target) != len(payload):
            return _fail("written file is incomplete: %r" % target)
    except OSError as exc:
        return _fail("cannot verify %r: %s" % (target, exc))

    print(
        "wrote %s (%d characters, %d bytes)"
        % (target, len(PLACARD), len(payload))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_place())
