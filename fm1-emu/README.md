# Emulating a synthesizer before it arrived — web deck

reveal.js 5, no build step, the same look as `agentic-hw/`. Everything is in `index.html`; 20 slides, about 15 minutes.

## Run

    python3 -m http.server 8000      # then open http://localhost:8000/fm1-emu/

## Presenting

| key | does |
|---|---|
| `S` | speaker view: notes, next slide, clock and per-slide pacing (12:00 total) |
| `F` | full screen |
| `D` | reboot the emulator on the demo slide |
| `‹` `›` buttons | leave the demo slide with the mouse (the emulator page has the keyboard once you click in it) |
| `Esc` / `O` | overview |

Speaker notes are the `<aside class="notes">` in each `<section>`; each slide's `data-timing` (seconds) matches
the time stamps in them and they sum to 720.

## The live demo (slide 9)

The emulator's hosted page with `?embed=1` (only the device and its controls) as an interactive slide background:
`https://joakimeriksson.github.io/fm1-emu/?embed=1&mhz=240&fw=<id>`. `data-demo-fw` on each demo section picks the
firmware (`felucca`; the extras below it: `sid`, `fm1doom`; any id in fm1-emu's `web/firmwares.json`). The page fetches
each firmware from its author's site, so **the demo needs the network**. Click Start in it for sound.

## Assets

All rendered by the emulator itself (`fm1-live --bench` with `FM1_BENCH_PANEL`, at 240 MHz):

* `assets/panel-felucca.png`: Felucca with a chord held (`FM1_BENCH_KEYS="1500:C4,1500:E4,1500:G4,1500:B4"`, 3000 ms).
* `assets/lcd/*.png`: the 480×480 screen cropped from the panel (x 370–850, y 42–522), after the catalog check's
  key script (`2000:C4,2000:m903c64,3500:C4^,3500:m803c00,5000:PLAY`, 6500 ms).
* `assets/wall.jpg`: 71 of those screens, 12 per row (look-alike builds of the same firmware left out).

## Numbers

From fm1-emu's tech report (`docs/paper/`, 13 Oct 2026; slides 12-15 from its section "Tuning towards the real
hardware", added 24-26 Oct: the rounds, the probes, the cycle table) and the repository on 27 Oct 2026 (commits, pull
requests, stars, forks, the catalog). The probes themselves: joakimeriksson/fm1-dock, `probes/`. Speeds: `fm1-live --bench 8000` on an M5 Max.
