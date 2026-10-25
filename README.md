# PAMS educational animations

Source for two captioned mathematical animations built with **3Blue1Brown's original ManimGL 1.7.2**, not Manim Community Edition.

- **Part 1 — Mathematical Overview:** ML-KEM context, arithmetic shares, compression intervals, PAMS equations and the masked comparison result.
- **Part 2 — Mathematical Derivations and Proofs:** the +2 rounding correction, 14-bit spacing, and comparison correctness including cyclic wraparound.

Both render at 1920 × 1080, 30 FPS, H.264. Equations use real LaTeX and filled SVG fraction rules so bars remain visible during animation. Explanations are burned-in captions; there is no voice narration.

## What is tracked

Animation and equation sources, dependency versions, mathematical checks, video verification scripts, production notes and the four reference PDFs in `references/`.

`.gitignore` excludes the virtual environment, downloaded executables, generated equation assets, videos, QA images, caches, logs and machine-specific configuration. Completed MP4 files remain local in `output/` and are not uploaded to GitHub. The old `revised_scenes.txt` is an intermediate draft; `pams_part1.py` is authoritative.

## Setup on Windows

Use Python 3.12, an OpenGL-capable graphics driver and the Segoe UI font. Run commands from the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe setup_project.py
```

`setup_project.py` creates the generated directories and a local `custom_config.yml` pointing to the FFmpeg executable provided by `imageio-ffmpeg`. It preserves an existing config.

Install [Tectonic](https://github.com/tectonic-typesetting/tectonic/releases) as `tools/tectonic.exe` (production used 0.17.0). It needs network access on first use to fetch LaTeX packages. Extract a Windows [FFmpeg build](https://www.gyan.dev/ffmpeg/builds/) beneath `tools/ffmpeg/<build-name>/bin/`, containing both `ffmpeg.exe` and `ffprobe.exe`; the verification scripts discover that directory automatically. These binaries are intentionally not tracked.

## Render

```powershell
# Compile LaTeX equations and check the mathematics
.\.venv\Scripts\python.exe formulas.py
.\.venv\Scripts\python.exe part2_lesson.py
.\.venv\Scripts\python.exe validate_math.py
.\.venv\Scripts\python.exe validate_part2.py

# Full-length renders; keep preview mode off
$env:PAMS_PREVIEW='0'
$env:PAMS_CHAPTERS=''
.\.venv\Scripts\manimgl.exe pams_part1.py PAMSPart1 -w --hd --file_name PAMS_Part_1 --video_dir output
.\.venv\Scripts\manimgl.exe pams_part2.py PAMSPart2 -w --hd --file_name PAMS_Part_2 --video_dir output

# Validate the encoded files and extract inspection frames
.\.venv\Scripts\python.exe verify_video.py
.\.venv\Scripts\python.exe verify_part2.py
```

Outputs: `output/PAMS_Part_1.mp4` and `output/PAMS_Part_2.mp4`. Part 2's verification embeds 25 chapter markers. Scripts save timing, equation events, mathematical reports and frames under `qa/`. Review the extracted frames visually in addition to automated checks.

Frame rate is configured as the integer 30 in the local configuration. Do not pass `--fps` with this installed ManimGL version. Quick previews use `PAMS_PREVIEW='1'`, `-l`, and, for Part 2, an optional selection such as `PAMS_CHAPTERS='8,12,16,20'`. Restore full-render settings afterward.

## Source map

| File | Purpose |
| --- | --- |
| `pams_part1.py` | Part 1 scenes and shared animation helpers |
| `formulas.py` | Part 1 LaTeX and reusable stroke-to-outline conversion |
| `pams_part2.py` | Part 2 animation, diagrams and equation transitions |
| `part2_lesson.py` | Part 2 equations, captions and LaTeX compilation |
| `validate_math.py`, `validate_part2.py` | Exact numerical and finite-domain checks |
| `verify_video.py`, `verify_part2.py` | Codec, timing, decode and encoded-frame checks |
| `PART1_PRODUCTION.md`, `PART2_PRODUCTION.md` | Production details and mathematical scope |

The checks support the mathematical explanations; numerical sampling alone is not a formal proof or a physical side-channel security claim.

## References

The mathematical notes are included in `references/mlkem.pdf`, `references/Zrounding.pdf`, `references/14bits.pdf`, and `references/inequality.pdf`.

- [Original ManimGL](https://github.com/3b1b/manim)
- [ManimGL documentation](https://3b1b.github.io/manim/)
- [FIPS 203: ML-KEM](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
