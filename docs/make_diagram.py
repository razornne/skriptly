"""Render the architecture diagram, light and dark, from one definition.

    python docs/make_diagram.py

GitHub picks the file by the reader's theme via <picture> in the README, so
two files have to exist — and two hand-drawn files drift. This is the one
source; both outputs are generated and committed.

Colours are GitHub's own canvas palette, so the diagram sits on the README as
if it belonged there rather than as a pasted image with its own background.
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).parent

THEMES = {
    "light": {
        "bg": "#ffffff",
        "box": "#f6f8fa",
        "rule": "#d1d9e0",
        "ink": "#1f2328",
        "muted": "#59636e",
        "accent": "#0969da",
        "accent_soft": "#ddf4ff",
        "gpu": "#8250df",
        "gpu_soft": "#fbefff",
    },
    "dark": {
        "bg": "#0d1117",
        "box": "#161b22",
        "rule": "#30363d",
        "ink": "#e6edf3",
        "muted": "#9198a1",
        "accent": "#4493f8",
        "accent_soft": "#121d2f",
        "gpu": "#ab7df8",
        "gpu_soft": "#1d1327",
    },
}

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

W, H = 900, 760

# title, subs, x, y, w, h, style: plain | hot | gpu | inset
BOXES = [
    (
        "Browser",
        ["record or upload · mic + tab audio", "MediaRecorder → IndexedDB autosave"],
        310, 28, 280, 74, "plain",
    ),
    (
        "Flask API",
        [
            "CPU container · scales to zero",
            "verify JWT · check plan · inject vocabulary",
            "route on duration",
        ],
        280, 166, 340, 90, "hot",
    ),
    ("GPU worker", ["transcribe_full", "one container, whole file"], 40, 332, 250, 76, "gpu"),
    (
        "CPU orchestrator",
        [
            "silence-aware split, ≤10 chunks",
            "parallel fan-out, one container per chunk",
            "a failed chunk becomes a gap, not a failed job",
        ],
        470, 332, 330, 90, "plain",
    ),
    ("GPU", ["chunk 1"], 470, 462, 92, 52, "gpu"),
    ("GPU", ["chunk 2"], 589, 462, 92, 52, "gpu"),
    ("GPU", ["chunk n"], 708, 462, 92, 52, "gpu"),
    (
        "global speaker stitching",
        ["voice embeddings + agglomerative", "clustering with a cannot-link rule"],
        470, 556, 330, 76, "hot",
    ),
    (
        "inside every GPU worker",
        [
            "ffmpeg preprocess  →  whisper",
            "→  pyannote diarize  →  merge",
            "→  LLM correction (+ new vocab)",
        ],
        120, 462, 300, 96, "inset",
    ),
    (
        "Postgres · row-level security",
        ["transcripts · workspaces", "per-user vocabulary"],
        40, 660, 340, 70, "plain",
    ),
    (
        "summary · action items",
        ["separate CPU container, cloud LLM"],
        470, 660, 330, 70, "plain",
    ),
]

ARROWS = [
    (450, 102, 450, 158),   # browser -> flask
    (450, 256, 450, 278),   # flask -> routing bus
    (165, 286, 165, 324),   # bus -> short GPU
    (635, 286, 635, 324),   # bus -> orchestrator
    (516, 422, 516, 454),   # orchestrator -> chunk 1
    (635, 422, 635, 454),   # orchestrator -> chunk 2
    (754, 422, 754, 454),   # orchestrator -> chunk n
    (635, 532, 635, 548),   # gathered chunks -> stitching
    (70, 408, 70, 652),     # short result -> Postgres
    (212, 646, 212, 652),   # stitched result -> Postgres
    (388, 695, 462, 695),   # Postgres -> summary
]

# Horizontal runs and elbows, drawn as raw path data.
PATHS = [
    ("M165,282 H635", False),                 # the routing bus under Flask
    ("M516,514 V532 H754 V514", False),       # chunk outputs gather
    ("M635,632 V646 H212", False),            # stitching result heads for storage
    ("M250,408 V462", True),                  # what the inset describes
    ("M40,690 H16 V196 H272", True),          # vocabulary loop back into Flask
]

LABELS = [
    ("JWT · audio goes straight to the backend,", 466, 128, MONO, 10.5),
    ("not through the CDN proxy", 466, 143, MONO, 10.5),
    ("< 30 min", 108, 306, MONO, 11),
    ("> 30 min", 578, 306, MONO, 11),
    ("the vocabulary a correction learns is", 30, 176, MONO, 10),
    ("prepended to the next transcription", 30, 188, MONO, 10),
    ("on request", 392, 686, MONO, 10),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(theme: str) -> str:
    c = THEMES[theme]
    styles = {
        "plain": (c["box"], c["rule"], c["ink"]),
        "hot": (c["accent_soft"], c["accent"], c["ink"]),
        "gpu": (c["gpu_soft"], c["gpu"], c["ink"]),
        "inset": (c["bg"], c["rule"], c["muted"]),
    }
    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Skriptly architecture: the browser records or uploads audio and '
        f"sends it with a JWT straight to a Flask container, which checks the plan, "
        f"injects the user's vocabulary and routes on duration. Short recordings go to "
        f"one GPU worker; long ones go to a CPU orchestrator that splits them at "
        f"silences and fans the chunks out across several GPUs, then re-identifies "
        f"speakers globally. Every worker runs preprocess, whisper, diarization, merge "
        f'and LLM correction. Results and learned vocabulary persist in Postgres.">'
    )
    p.append(
        f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c["muted"]}"/></marker>'
        f'<marker id="b" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c["accent"]}"/></marker></defs>'
    )
    p.append(f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>')

    for d, is_loop in PATHS:
        if is_loop:
            p.append(
                f'<path d="{d}" stroke="{c["accent"]}" stroke-width="1.5" fill="none" '
                f'stroke-dasharray="5 4" marker-end="url(#b)"/>'
            )
        else:
            p.append(f'<path d="{d}" stroke="{c["muted"]}" stroke-width="1.5" fill="none"/>')

    for ax1, ay1, ax2, ay2 in ARROWS:
        if (ax1, ay1) == (ax2, ay2):
            continue
        p.append(
            f'<path d="M{ax1},{ay1} L{ax2},{ay2}" stroke="{c["muted"]}" '
            f'stroke-width="1.5" fill="none" marker-end="url(#a)"/>'
        )

    for title, subs, x, y, w, h, style in BOXES:
        fill, stroke, title_ink = styles[style]
        dash = ' stroke-dasharray="4 3"' if style == "inset" else ""
        p.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"{dash}/>'
        )
        size = 11.5 if style == "gpu" and w < 120 else 13.5
        p.append(
            f'<text x="{x + 13}" y="{y + 22}" font-family="{SANS}" font-size="{size}" '
            f'font-weight="600" fill="{title_ink}">{esc(title)}</text>'
        )
        for i, sub in enumerate(subs):
            p.append(
                f'<text x="{x + 13}" y="{y + 40 + i * 15}" font-family="{MONO}" '
                f'font-size="10.5" fill="{c["muted"]}">{esc(sub)}</text>'
            )

    for text, x, y, font, size in LABELS:
        p.append(
            f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'fill="{c["muted"]}">{esc(text)}</text>'
        )

    p.append("</svg>\n")
    return "\n".join(p)


def main() -> None:
    for theme in THEMES:
        path = OUT / f"architecture-{theme}.svg"
        path.write_text(render(theme), encoding="utf-8")
        print(f"wrote {path.relative_to(OUT.parent)}")


if __name__ == "__main__":
    main()
