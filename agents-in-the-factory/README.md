# Agents in the OT loop — web deck

reveal.js 5, no build step, same design as `../agentic-hw` (the hardware-in-the-loop talk, which is part two here).
Two languages, same slides: `index.html` (English) and `sv.html` (svenska, for Swedish industry); both use the
shared `deck.css` and `deck.js`, so a layout change applies to both. About 23 minutes of planned slide time (26 slides) plus questions, for a 30-minute slot, in three parts: what an agent is, hardware in the
agentic loop, and the OTTO testbed (IT/OT, zones, a kiln fault that never alarms, LLM benchmark results).

## Run

    python3 -m http.server 8000      # from ~/work/presentations, then open
                                     # http://localhost:8000/agents-in-the-factory/         (English)
                                     # http://localhost:8000/agents-in-the-factory/sv.html  (svenska)

## Presenting

| key | does |
|---|---|
| `S` | speaker view — notes with a 27-minute timing plan, next slide, pacing |
| `F` | full screen |
| `D` | reload the demo on a demo slide |
| `‹` `›` buttons | leave a demo slide with the mouse; arrow keys are forwarded from inside the viewer too |
| `Esc` / `O` | overview |

`?fragments=false` shows every slide fully built (handy for screenshots and a PDF: `index.html?print-pdf&fragments=false`).

## The demos

Two slides use the testbed's own viewer as an interactive background, replaying recorded runs: the sawline
(information flow, namespace, zones) and, in the backup, the kiln with a drifting humidity probe at hour 48. The deck is
self-contained: `demos/viewer/` is a copy of the testbed viewer (index.html and dashboard.html, no dependencies) and
`demos/runs/` holds the recordings (the sawline trimmed to its first 480 s). No testbed and no network are needed, and
the demos work from GitHub Pages too. To refresh them, copy `viewer/*.html` from the testbed and re-record with

    cd ~/work/openind4agent
    uv run industrial-testbed run --scenario sawmill_full_baseline_v1 --record runs/deck/sawline.jsonl --every 10
    uv run industrial-testbed run --scenario kiln_rh_drift_v1 --record runs/deck/kiln-drift.jsonl --every 60


## Where the numbers come from

- Charts on "Green by accident, in a kiln" and "The alarm names the healthy probe": simulated with the testbed
  (`kiln_rh_drift_v1`, `k02_control_probe_offset_v1` seed 1234), drawn as inline SVG paths.
- Benchmark table: `docs/benchmarks/2026-09-22.md` (sawline) and `runs/benchmark/kiln-2026-09-25` (kiln) in the testbed;
  Claude rows and the frontier slide: `runs/claude-code/kiln-{opus,sonnet,haiku}` (Opus 5.5, Sonnet 5, Haiku 4.5 via
  `scripts/bench_claude_code.py`, 2026-09-26).
- Screenshots in `assets/`: the viewer at 2× on those recordings.

## The Swedish version

`sv.html` is a full translation, including diagram labels, demo captions and speaker notes, using Swedish sawmill and
automation terms (virkestork, fuktgivare, styrgivare/kontrollgivare, förreglingar, zoner och kanaler, justering).
The screenshots and the live viewer stay in English; the notes on those slides say so. The two quotes from the
Cooja-NG paper are marked as translations. Keep the two files in step when a slide changes.

## Structure and backup

26 slides in the talk (23 minutes planned, paced for a calm delivery), then a grey "Backup" divider and six
uncounted backup slides for questions: "In a year", "The loop is its own", "Emulator and silicon", the
hardware-loop "six rules", the kiln demo and "Built the same way". The slide counter counts the talk only
(backup slides show "+"); the speaker-note timestamps are the cumulative plan. Written for a broad OT
audience (energy and grids, water and waste, property and heating, IoT, forestry, process industry): the
slide "The sawmill is the example — the patterns are yours" maps each testbed fault to their plants.

The sawmill and kiln are the worked example throughout part three; each slide names the counterpart in heating,
water, grids or buildings where it fits ("the kiln is a heating substation with timber in it"). The folder keeps
its original name, agents-in-the-factory.
