#!/usr/bin/env python3
"""Convert a "chords over lyrics" lead sheet into ChordPro, optionally rendering a PDF.

Input format (plain text):
    Song Title - Extra info
    Tempo: 124, Tonalidad: D
    [Section name]
        D        A
    lyrics line under the chords
    D C A# A          <- chord-only lines are fine too

Usage:
    python3 leadsheet2cho.py song.txt              # writes song.cho
    python3 leadsheet2cho.py song.txt --pdf        # also writes song.pdf (needs `chordpro`)
    python3 leadsheet2cho.py song.txt -o out.cho --pdf --transpose 2
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

# A, Bb, C#m7, Dsus4, F#m7b5, G/B, Cmaj7, A7(b9), N.C. ...
CHORD_RE = re.compile(
    r"^(?:N\.?C\.?|"
    r"[A-G][#b]?"
    r"(?:maj|min|m|M|dim|aug|sus|add|\+|-|°|ø)?"
    r"[0-9]*"
    r"(?:(?:maj|sus|add|b|#|\+|-)[0-9]+)*"
    r"(?:\([^)]*\))?"
    r"(?:/[A-G][#b]?)?)$"
)
# Bar lines / repeat marks that may appear on chord lines.
NEUTRAL_TOKENS = {"|", "||", "/", "%", "-", "x2", "x3", "x4", "(x2)", "(x3)", "(x4)"}

SECTION_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$")
META_RE = re.compile(
    r"(tempo|bpm|tonalidad|tono|key|capo|compás|compas|time)\s*:\s*([^,;]+)", re.I
)
META_MAP = {
    "tempo": "tempo", "bpm": "tempo",
    "tonalidad": "key", "tono": "key", "key": "key",
    "capo": "capo",
    "compás": "time", "compas": "time", "time": "time",
}
# Section names (lower-case prefix) rendered as a chorus block.
CHORUS_NAMES = ("coro", "chorus", "estribillo")
VERSE_NAMES = ("verso", "verse", "estrofa")
BRIDGE_NAMES = ("puente", "bridge")


def is_chord_line(line: str) -> bool:
    tokens = line.split()
    if not tokens:
        return False
    chords = [t for t in tokens if t not in NEUTRAL_TOKENS]
    return bool(chords) and all(CHORD_RE.match(t) for t in chords)


def chord_positions(line: str) -> list[tuple[int, str]]:
    return [(m.start(), m.group()) for m in re.finditer(r"\S+", line)
            if m.group() not in NEUTRAL_TOKENS]


def merge(chord_line: str, lyric_line: str) -> str:
    """Insert [Chord] markers into the lyric line at the chord column positions."""
    lyric = lyric_line.rstrip()
    out, cursor = [], 0
    for col, chord in chord_positions(chord_line):
        if col > len(lyric):
            # Chord sits past the end of the lyrics: pad so it still shows up.
            lyric = lyric + " " * (col - len(lyric))
        out.append(lyric[cursor:col])
        out.append(f"[{chord}]")
        cursor = col
    out.append(lyric[cursor:])
    return "".join(out).rstrip()


def chord_only(chord_line: str) -> str:
    """Render a chord line with no lyrics, keeping rough spacing between groups."""
    parts = re.split(r"(\s+)", chord_line.strip())
    out = []
    for p in parts:
        if not p:
            continue
        if p.isspace():
            out.append(" " if len(p) < 3 else "   ")
        elif p in NEUTRAL_TOKENS:
            out.append(p)
        else:
            out.append(f"[{p}]")
    return "".join(out)


def section_kind(name: str) -> str:
    n = name.strip().lower()
    if n.startswith(CHORUS_NAMES):
        return "chorus"
    if n.startswith(VERSE_NAMES):
        return "verse"
    if n.startswith(BRIDGE_NAMES):
        return "bridge"
    return "comment"


def convert(text: str) -> str:
    lines = [l.expandtabs(8).rstrip("\n") for l in text.splitlines()]
    out: list[str] = []
    i = 0

    # Skip leading blank lines; first line is the title.
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        parts = [p.strip() for p in re.split(r"\s+-\s+", lines[i].strip())]
        out.append(f"{{title: {parts[0]}}}")
        if len(parts) > 1:
            out.append(f"{{subtitle: {' - '.join(parts[1:])}}}")
        i += 1

    # Metadata lines directly after the title.
    while i < len(lines) and META_RE.search(lines[i]) and not SECTION_RE.match(lines[i]):
        for key, val in META_RE.findall(lines[i]):
            out.append(f"{{{META_MAP[key.lower()]}: {val.strip()}}}")
        i += 1

    open_env: str | None = None

    def close_env():
        nonlocal open_env
        if open_env:
            out.append(f"{{end_of_{open_env}}}")
            open_env = None

    while i < len(lines):
        line = lines[i]
        m = SECTION_RE.match(line)
        if m and not is_chord_line(m.group(1)):
            close_env()
            name = m.group(1).strip()
            kind = section_kind(name)
            out.append("")
            if kind == "comment":
                out.append(f"{{comment: {name}}}")
            else:
                out.append(f"{{start_of_{kind}: label=\"{name}\"}}")
                open_env = kind
            i += 1
            continue

        if not line.strip():
            # Blank line ends a section block.
            close_env()
            out.append("")
            i += 1
            continue

        if is_chord_line(line):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt.strip() and not is_chord_line(nxt) and not SECTION_RE.match(nxt):
                out.append(merge(line, nxt))
                i += 2
            else:
                out.append(chord_only(line))
                i += 1
            continue

        # Plain lyric line. Escape literal brackets so ChordPro doesn't read them as chords.
        out.append(line.rstrip().replace("[", "(").replace("]", ")"))
        i += 1

    close_env()
    # Collapse multiple blank lines.
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="lead sheet text file")
    ap.add_argument("-o", "--output", type=Path, help="output .cho file (default: <input>.cho)")
    ap.add_argument("--pdf", action="store_true", help="also render a PDF with chordpro")
    ap.add_argument("--transpose", type=int, default=0, help="semitones to transpose the PDF")
    ap.add_argument("--diagrams", action="store_true", help="show guitar chord diagrams in the PDF")
    ap.add_argument("--config", type=Path, help="chordpro JSON config (default: style.json next to this script, if present)")
    args = ap.parse_args(argv)

    cho_path = args.output or args.input.with_suffix(".cho")
    cho_path.write_text(convert(args.input.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"wrote {cho_path}")

    if args.pdf:
        exe = shutil.which("chordpro")
        if not exe:
            print("error: `chordpro` not found on PATH (install with: cpanm chordpro)", file=sys.stderr)
            return 1
        pdf_path = cho_path.with_suffix(".pdf")
        cmd = [exe, str(cho_path), "-o", str(pdf_path)]
        config = args.config or Path(__file__).with_name("style.json")
        if config.exists():
            cmd += ["--config", str(config)]
        if args.diagrams:
            cmd += ["--define", "diagrams.show=all"]
        if args.transpose:
            cmd += ["--transpose", str(args.transpose)]
        subprocess.run(cmd, check=True)
        print(f"wrote {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
