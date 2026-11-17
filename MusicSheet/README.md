# MusicSheet

Turn a plain-text "chords over lyrics" lead sheet into a clean PDF (chord names + lyrics, no notation).

Pipeline: `leadsheet2cho.py` converts your text to [ChordPro](https://www.chordpro.org) format, then the `chordpro` CLI renders the PDF using `style.json`.

## Install (macOS)

```bash
brew install harfbuzz pkg-config cpanminus
```

```bash
cpanm --notest chordpro
```

```bash
chordpro --version
```

Python 3.9+ is the only other requirement (no pip packages needed).

## Usage

```bash
python3 leadsheet2cho.py examples/isidora.txt --pdf
```

Writes `examples/isidora.cho` and `examples/isidora.pdf`.

Options:

| Flag | Effect |
|---|---|
| `--pdf` | Also render the PDF (otherwise only the `.cho` file) |
| `-o FILE.cho` | Output path (PDF goes next to it) |
| `--transpose N` | Transpose chords by N semitones in the PDF |
| `--diagrams` | Show guitar chord diagrams at the bottom of the page |
| `--config FILE.json` | Use a different ChordPro style (default: `style.json`) |

## Input format

```
Title - Subtitle
Tempo: 124, Tonalidad: D
[Intro]
D C A# A
[Coro]
    D           B7   Em       A            D
Isidora, Isidora, Isidora Callao Calipso Queen
```

- First line: title (text after ` - ` becomes the subtitle).
- Metadata line(s): `Tempo/BPM`, `Tonalidad/Tono/Key`, `Capo`, `Compás/Time`.
- `[Section]` lines become headings; `Coro/Chorus/Estribillo`, `Verso/Verse/Estrofa` and `Puente/Bridge` become indented blocks with a side label.
- A chord line is merged into the lyric line below it by column position (use a monospace editor when aligning). Chord lines with no lyrics are printed as a row of chords.
- Use spaces, not tabs, for alignment (tabs are expanded to 8 columns).

## Styling

Edit `style.json` (fonts, colors, paper size, header). See the ChordPro config reference: https://www.chordpro.org/chordpro/chordpro-configuration/
