# Agents in the factory loop — web deck

reveal.js 5, no build step, same design as `../agentic-hw` (the hardware-in-the-loop talk, which is part two here).
Two languages, same slides: `index.html` (English) and `sv.html` (svenska, for Swedish industry); both use the
shared `deck.css` and `deck.js`, so a layout change applies to both. About 27 minutes plus questions, in three parts: what an agent is, hardware in the
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

## The live demos

Two slides use the testbed's own viewer as an interactive background: the sawline (information flow, UNS) and the kiln
with a drifting humidity probe at hour 48. `demos/testbed` is a symlink to `~/work/openind4agent` and is gitignored:
the testbed repository has no license yet, so nothing of it is published with the deck. The recordings are in
`~/work/openind4agent/runs/deck/`; recreate them with

    cd ~/work/openind4agent
    uv run industrial-testbed run --scenario sawmill_full_baseline_v1 --record runs/deck/sawline.jsonl --every 10
    uv run industrial-testbed run --scenario sawmill_full_segmented_v1 --record runs/deck/segmented.jsonl --every 10
    uv run industrial-testbed run --scenario kiln_rh_drift_v1 --record runs/deck/kiln-drift.jsonl --every 60

On GitHub Pages the demo slides are empty (no testbed there); every point they make is also on the slide before or
after as a screenshot, so the deck still works as a handout.

## Where the numbers come from

- Charts on "Green by accident, in a kiln" and "The alarm names the healthy probe": simulated with the testbed
  (`kiln_rh_drift_v1`, `k02_control_probe_offset_v1` seed 1234), drawn as inline SVG paths.
- Benchmark table: `docs/benchmarks/2026-09-22.md` (sawline) and `runs/benchmark/kiln-2026-09-25` (kiln) in the testbed.
- Screenshots in `assets/`: the viewer at 2× on those recordings.

## The Swedish version

`sv.html` is a full translation, including diagram labels, demo captions and speaker notes, using Swedish sawmill and
automation terms (virkestork, fuktgivare, styrgivare/kontrollgivare, förreglingar, zoner och kanaler, justering).
The screenshots and the live viewer stay in English; the notes on those slides say so. The two quotes from the
Cooja-NG paper are marked as translations. Keep the two files in step when a slide changes.
