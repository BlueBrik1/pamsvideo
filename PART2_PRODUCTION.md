# PAMS Part 2 production

The finished artifact is `output/PAMS_Part_2.mp4`. Part 1's source and video are preserved. This production uses the installed original ManimGL 1.7.2 and imports its existing Part 1 typography and static-frame hold helper.

## Sources and scope

The complete local references are `Zrounding.pdf` (4 pages), `14bits.pdf` (2 pages), and `inequality.pdf` (9 pages), from the user's Downloads directory. Extracted text and rendered page images are under `qa/part2`. The user-authored storyboard is the pasted request dated October 25, 2026.

All three derivations are included, with one-based share indices. Canonical shares are integers in [0,3329). The proof covers ML-KEM ciphertext compression widths 4, 5, 10, and 11. The modular share-sum identity is derived through an explicit integer multiple of 3329. The no-wrap bound is shown in two stages: first for G itself, then for G plus delta. The final claim is functional correctness, not physical side-channel security.

The requested Sepia writing skill was searched for by filename and SKILL.md contents in the local skill and plugin directories. It was unavailable. Captions follow the user's supplied plain-language requirements directly.

Official Manim references consulted:

- https://github.com/3b1b/manim
- https://3b1b.github.io/manim/
- https://3b1b.github.io/manim/getting_started/installation.html
- https://3b1b.github.io/manim/getting_started/configuration.html

## Files

- `part2_lesson.py`: 25 chapters, 172 caption/equation states, LaTeX compilation and semantic colors.
- `pams_part2.py`: animated fraction pieces, spacing lines, cyclic diagrams, boundary comparisons, and equation continuity.
- `validate_part2.py`: exact-integer checks and examples; no floating-point rounding is used in correctness checks.
- `verify_part2.py`: MP4 chapters, faststart, full decode, encoded-frame extraction, equation coverage and Part 1 preservation.

## Mathematical checks

`qa/part2/math-validation.json` records exhaustive checks of all 11,082,241 canonical starting-boundary/distance pairs, 31,159,440 coefficient comparisons (all public coefficients at four widths and all three error values), and 250,000 randomly sampled canonical share triples. Computational checks support the independently reviewed algebra; they are not a substitute for the proof.

## Rendering

LaTeX is compiled using the existing Tectonic installation. PDF-to-SVG fraction rules are converted from stroked paths to filled outlines at their original thickness before ManimGL imports them. Equation transitions move the preceding equation to a reference row and reveal the next equation below. Fraction glyphs and bars are never interpolated into unrelated paths. Sum and fraction expressions receive more height than single-line expressions.

The palette is applied after constructing ManimGL primitives, because Dot, Circle and Arrow have explicit fill/stroke defaults which otherwise override a generic color argument.

From `C:\PAMS`, use the existing virtual environment:

```powershell
.\.venv\Scripts\python.exe part2_lesson.py
.\.venv\Scripts\python.exe validate_part2.py
$env:PAMS_PREVIEW='0'
$env:PAMS_CHAPTERS=''
.\.venv\Scripts\manimgl.exe pams_part2.py PAMSPart2 -w --hd --file_name PAMS_Part_2 --video_dir C:\PAMS\output
.\.venv\Scripts\python.exe verify_part2.py
```

Preview chapters can be selected with `PAMS_CHAPTERS='8,12,16,20'`, `PAMS_PREVIEW='1'`, scene `Part2Preview`, and `-l`. Preview holds are shortened and must never be used for the final delivery.

## QA

Every caption state is saved to a PNG and checked against safe frame boundaries. Low-resolution moving previews and full-resolution layout frames were reviewed before the final render. The encoded-video audit samples every chapter, every fraction reveal, selected fractions during motion, and the ending. `qa/part2/video-validation.json` records final resolution, codec, frame rate, duration, complete decoding and chapter/equation coverage. The movie has embedded chapter navigation.
