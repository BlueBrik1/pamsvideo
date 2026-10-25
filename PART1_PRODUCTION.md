# PAMS — Part 1: Mathematical Overview

The finished deliverable is `output/PAMS_Part_1.mp4`.

This film uses **3b1b ManimGL 1.7.2** (`manimlib`), not Manim Community.
It uses explanatory captions without narration. All mathematical artwork is
compiled from LaTeX using Tectonic, then converted from PDF into vector paths
for ManimGL. The mathematical source is the user's four-page `mlkem.pdf`;
the user explicitly authorized this PDF in place of the missing TeX source.

## Sources consulted

- User-supplied PDF: `C:/Users/Skyler Lee/Downloads/mlkem.pdf`
- User-supplied detailed Part 1 production request.
- https://github.com/3b1b/manim
- https://3b1b.github.io/manim/
- https://3b1b.github.io/manim/getting_started/installation.html
- https://3b1b.github.io/manim/getting_started/configuration.html
- https://3b1b.github.io/manim/getting_started/example_scenes.html
- https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf
  (Compression: Section 4.2.1; implicit rejection: Section 6.3.)

## Reproduction (PowerShell, from C:/PAMS)

```powershell
& .venv/Scripts/python.exe formulas.py
& .venv/Scripts/python.exe validate_math.py
$env:PAMS_PREVIEW='0'
& .venv/Scripts/manimgl.exe pams_part1.py PAMSPart1 -w --hd --file_name PAMS_Part_1 --video_dir C:/PAMS/output
```

The frame rate is configured as the integer 30 in `custom_config.yml`.
The local ManimGL version has a CLI parsing issue with `--fps`; use the
configuration value instead. For quick previews, set `PAMS_PREVIEW=1`.
Do not use preview mode for the delivered film: it shortens reading time.

The source has reusable text, equation, share, interval, communication,
transition, and caption helpers, with 16 chapter methods. Equation asset
filenames use hexadecimal keys to keep uppercase and lowercase symbols
distinct on Windows. `requirements-lock.txt` records the environment.

## Verification

- Exact rational arithmetic checks every supplied numerical example.
- Checks every original coefficient for each of the four compression widths.
- Compares the PAMS predicate with direct compression on 480,000 sampled
  combinations of canonical shares and public coefficients.
- These numerical tests are not a formal proof; Part 2 proofs are not included.
- `qa/` contains the validation report, reading-state images, preview renders,
  timeline, and render logs. The scene checks all visible object bounds against
  a consistent safe area. Full-resolution frames are visually reviewed.

The output ends at the masked comparison result. Secret selection is described
as the subsequent decapsulation step. Hardware gadgets and security proofs
are deliberately outside Part 1.

## Revision: typography and beginner explanations

The initial SVG importer erased the LaTeX fraction rules: MuPDF exports them
as stroked open paths, and ManimGL's `SVGMobject` defaults to a zero stroke
width. `outline_svg_strokes` now converts those strokes to filled vector
outlines using their original LaTeX geometry and thickness. This also restores
box rules. Nothing substitutes hand-positioned fraction text. Outlined assets
live in `assets/outlined/`; `qa/stroke-audit.json` records each converted rule.
The loader reads SVG as UTF-8 explicitly to avoid Windows ANSI decoding errors.

The revised captions introduce bits, public and secret keys, prime marks,
indices, ordinary shares, modular addition, compression intervals, scale
changes, Boolean results, XOR, and AND before using them in the main equations.
The original 16 chapters and canonical equations remain. All captions were
rewritten under the user's supplied plain-language requirements. A search of
installed skill names and SKILL.md contents found no available Sepia skill;
the revision does not claim to have used it.

Run `EquationDiagnostics` for rendered fraction, bracket, and substitution
checks. The complete film records each equation reveal and morph in
`qa/PAMSPart1-equations.json`. `verify_video.py` extracts the first stable video
frame after every fraction-bearing equation event, in addition to sampling
every chapter and decoding the entire video. Reading holds reuse identical
ManimGL camera pixels only when no updaters or live window require animation.
