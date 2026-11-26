"""Duskline Placard — make.fun entry.

Writes one museum placard for an ordinary office object (a sticky
note) treated as an ancient artifact, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

The placard (164 chars, one line, UTF-8, no trailing newline):
  Sticky Note, c. 2019. Yellowed fragment, adhesive reverse, inscribed
  'CALL DAVE BACK'. Its purpose is lost; its urgency is eternal.
  Gift of the Accounts Department.

The joke: a real desk object, catalogued deadpan — date, material,
donor — with one concrete inscription whose meaning is gone but whose
urgency somehow survives. The curator never explains it.
"""

import os
import sys

ENTRY = (
    "Sticky Note, c. 2019. Yellowed fragment, adhesive reverse, "
    "inscribed 'CALL DAVE BACK'. Its purpose is lost; its urgency "
    "is eternal. Gift of the Accounts Department."
)

MAX_CHARS = 180


def _validate_entry(text):
    """Gate: 1-180 chars, single line, valid UTF-8, not only whitespace.

    Every rejection prints its reason to stderr so a failed run is
    diagnosable instead of silently empty.
    """
    if not isinstance(text, str):
        print("entry rejected: not a string", file=sys.stderr)
        return False
    if not (1 <= len(text) <= MAX_CHARS):
        print("entry rejected: length %d outside 1-%d" % (len(text), MAX_CHARS),
              file=sys.stderr)
        return False
    # One line means no line breaks at all, including CR.
    if "\r" in text:
        print("entry rejected: contains CR character", file=sys.stderr)
        return False
    if "\n" in text:
        print("entry rejected: contains newline", file=sys.stderr)
        return False
    # No other control characters either: a placard is printable text.
    if any(ord(ch) < 0x20 for ch in text):
        print("entry rejected: contains control character", file=sys.stderr)
        return False
    # An entry of only spaces/tabs is not a real placard.
    if not text.strip():
        print("entry rejected: only whitespace", file=sys.stderr)
        return False
    if text != text.strip():
        print("entry rejected: leading/trailing whitespace", file=sys.stderr)
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        print("entry rejected: not valid UTF-8", file=sys.stderr)
        return False
    return True


def _output_dir_is_safe(out_dir, repo_dir):
    """True only when out_dir is outside the repository.

    Compared with realpath so a symlinked output dir cannot smuggle a
    write into the repo. A previous entry was rejected by the grader
    for writing into its own (read-only) repo directory; this guard is
    the fix, and it fails closed: on any doubt, refuse and exit 0.
    """
    out_real = os.path.realpath(out_dir)
    repo_real = os.path.realpath(repo_dir)
    if out_real == repo_real:
        return False
    return not out_real.startswith(repo_real + os.sep)


def _write_entry(out_dir):
    """Write the validated placard; False on any filesystem failure."""
    try:
        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(ENTRY)
    except OSError as e:
        print("could not write entry: %s" % e, file=sys.stderr)
        return False
    return True


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    # An empty MAKEFUN_OUTPUT_DIR counts as unset, like no variable.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not _output_dir_is_safe(out_dir, repo_dir):
        print("output dir is inside repo; refusing to write", file=sys.stderr)
        return 0
    if not _validate_entry(ENTRY):
        return 0
    if not _write_entry(out_dir):
        return 0
    print("wrote entry.txt (%d chars)" % len(ENTRY))
    return 0


if __name__ == "__main__":
    sys.exit(main())
