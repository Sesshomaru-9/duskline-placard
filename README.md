# Duskline Placard

A one-line museum placard for a sticky note, catalogued in the year 3000
as if it were an ancient artifact.

> Sticky Note, c. 2019. Yellowed fragment, adhesive reverse, inscribed
> 'CALL DAVE BACK'. Its purpose is lost; its urgency is eternal. Gift of
> the Accounts Department.

## How it works

The placard text lives in `main.py` and is written verbatim to
`$MAKEFUN_OUTPUT_DIR/entry.txt` as UTF-8 (164 characters, one line, no
trailing newline). The program uses only the Python standard library —
no network, no clock, no randomness — and refuses to write anywhere
inside this repository.

## Usage

```sh
MAKEFUN_OUTPUT_DIR=/path/to/out python3 main.py
```
