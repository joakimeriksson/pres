# Edge AI in the loop — web deck

reveal.js 5, no build step, same design as `../agents-in-the-factory` (shared tokens; this folder has its own copy of
`deck.css`, `deck.js` and `vendor/`, so it stands alone). A guest lecture for IoT, computer science and electrical
engineering students, 40+ minutes in all: about 26 minutes of planned slide time (32 slides), then about 8 minutes of
live CandyTron 4000 demo and questions. Three parts:

1. **Edge AI** — the October 2025 guest lecture ("Edge AI in Action", Uppsala), compressed and updated: the IoT
   timeline, edge vs. cloud, the hardware range, the software stack, use cases, risks, and "the hard part is building it".
2. **Hardware in the agentic loop** — the short version of `../agentic-hw`: oracle / calibrator / proxy, Contiki-NG 5.2,
   Cooja-NG, the FPGA CPU, esp32sim and the 500 KB bug, the live demo, two stories, the six rules, where the agents
   stopped, then "now flip it".
3. **Edge AI that acts** — CandyTron 4000: vision-language-action as the direction, one year on (2025 vs. 2026),
   the architecture, what a noisy fair found, the guard at the hardware boundary, take-home, demo handoff.

## Run

    python3 -m http.server 8000      # from ~/work/presentations, then open
                                     # http://localhost:8000/edge-ai-in-the-loop/

## Presenting

| key | does |
|---|---|
| `S` | speaker view — notes with the timing plan, next slide, pacing (total 25:50) |
| `F` | full screen |
| `D` | reboot the emulator on the demo slide |
| `↻` `‹` `›` buttons | on the demo slide: reboot, or leave it with the mouse after clicking inside the emulator |
| `Esc` / `O` | overview |

`?fragments=false` shows every slide fully built (screenshots, PDF: `index.html?print-pdf&fragments=false`).

## The live demos

- **esp32sim** (slide 18, plus one extra below it with `↓`): the same wiring as `../agentic-hw`. `demos/esp32sim` is a
  local symlink to `~/work/esp32sim/web` (gitignored); on GitHub Pages the slide loads `mikroverk.github.io/esp32sim`.
  Serve over HTTP, not file://.
- **CandyTron 4000** runs outside the deck, after the "Live: CandyTron 4000" slide: `~/work/mcp-agents/start-candytron.sh` (see its README;
  `--sim` without the arm, `--direct-audio` for the one-call speech path the "one year on" slide describes).

## Where the facts come from

- Part 1: the 2025 lecture (`~/Documents/Presentations/AI-and-ML/EdgeAI-in-Action-Guest-Lecture-20251017.pptx`);
  the photos in `assets/lecture/` are taken from it, resized. Accelerator figures: Coral 4 TOPS, Hailo-8 26 TOPS,
  Jetson Orin Nano 8 GB 40–67 TOPS at 7–25 W (vendor specs).
- Part 2: `../agentic-hw` and its sources (Contiki-NG 5.2 release issue #3190, the Cooja-NG paper, SNCNW 2026).
- Part 3: `~/work/mcp-agents` — README, and the commits "Fix the five failure modes seen at the fair" (01ae58f),
  "Guard the arm at the hardware boundary" (f6a09d7), "Voice identity" (4afbd77). The 2025 column of "one year on"
  is the 2025 lecture's CandyTron slides (Razer laptop with RTX 5070 Ti, Whisper → Gemma 3 → Piper, YOLO11).

## If time runs short

Skip, in this order: the extra below the demo (`→` instead of `↓`), "Why the cause was 500 KB from the crash" (25 s),
"Where the agents stopped" (40 s), "Two stories" (45 s), the FPGA slide (50 s), the live esp32sim demo (45 s).
That is 3:25 back without touching parts 1 or 3.

## Editing

Speaker-note time stamps are the cumulative plan from each slide's `data-timing`; after changing timings, recompute
them (a slide's note starts with `M:SS.`) and keep `totalTime` in `deck.js` equal to the sum.
