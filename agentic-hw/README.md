# Hardware in the agentic loop — web deck

reveal.js 5, no build step, works offline. Everything is in `index.html`.

## Run

    python3 -m http.server 8000      # then open http://localhost:8000/
    
Opening `index.html` directly from disk also works (the demo slide embeds its WASM as bytes so it needs no fetch).
A local server is required once your own WASM build uses `fetch()` or SharedArrayBuffer.

## Presenting

| key | does |
|---|---|
| `S` | speaker view — notes, next slide, elapsed clock and per-slide pacing (set to 10:00 total) |
| `F` | full screen |
| `D` | reboot the emulator on the demo slide (if it wedges mid-talk) |
| `Esc` / `O` | slide overview |
| `B` | black out |

Speaker notes are the `<aside class="notes">` inside each `<section>`; the time stamps in them are the 10-minute plan,
and each slide's `data-timing` (seconds) matches it, so the speaker view's pacing bar is honest. They sum to 600.

## PDF / handout

Open `index.html?print-pdf` in Chrome and print to PDF (landscape, no margins). Fragments are collapsed onto one page per slide.

## The live demo (slide 9)

Slide 9 is esp32sim's own web page as a full-bleed, interactive slide background. It is a vertical stack:
`↓` goes to two extra scenarios (two Contiki-NG motes on one 802.15.4 medium; the C64 SID jukebox) that
are not part of the 10-minute plan (`data-timing="0"`). Skip them with `→`.

    <section data-background-iframe="demos/esp32sim/index.html?wasm&fw=atech" data-background-interactive>

`demos/esp32sim` is a symlink to `~/work/esp32sim/web` (the WASM build plus `wasm/fw/`), so the deck
always shows the current build and nothing is copied. **Serve with `python3 -m http.server`** — the page
fetches the WASM and firmware, so file:// will not do. The slide has no `data-preload` on purpose: the
emulator boots when you arrive, so the audience sees the ROM → bootloader → app sequence. `D` reboots it.

* Other scenarios: change `fw=atech` to any name in `demos/esp32sim/wasm/fw/demos.json`
  (`atech-sid` = C64 SID jukebox, `c6-contiki-net` = two Contiki-NG motes on one radio, `c6-rpl-net` = RPL root + client).
* The demo sections carry `data-demo-fw="<name>"`; a few lines at the top of the script turn that into the iframe URL:
  the local symlink when served from localhost, `https://joakimeriksson.github.io/esp32sim/` when the deck is on GitHub Pages.
* Taking the deck to another machine without network: replace the symlink with a copy of `~/work/esp32sim/web`
  (about 80 MB with all firmware; the Espressif mask ROM in `wasm/fw/` is not redistributable, keep it off public hosts).

## Hosting on GitHub Pages

Everything is static and nothing needs special headers, so a plain Pages site works: push this directory (the symlink is
git-ignored) and enable Pages. The demo slides then load the emulator from the esp32sim Pages site, which is the same origin,
so `D` (reboot) keeps working. Speaker view (`S`) opens a popup, allow it once.
* `demos/hello-wasm.html` is the original 52-byte placeholder; it still works in an ordinary `<iframe>` slide.

## The other animated bits

* **Slide 5, run strip**: 15 `<i>` cells in `.runs`, one per CI run; `class="ok"` is the green one. Edit the markup to change the count.
* **Slide 6, frame player**: `assets/rv32-boot-frames.png` is a sprite of the first 24 Verilator frames (top 320 px of each
  640×480 frame, side by side), stepped at 4 fps while the slide is showing. Regenerate after a core or firmware change:

      cd ~/work/FPGA/rv32/sim && obj_dir_video8/Vsoc_video +hex=../../contiki/examples/rv32-demo/build/rv32soc/clk1000000/rv32-demo.hex +frames=24 +frameprefix=boot_ +cycles=11000000

  then crop each `boot_NNN.png` to 640×320, paste them left to right into one image, and set `data-frames` on `#player` to the count.
* **Slide 10, LED grids**: `data-p7` / `data-p11` on `#grids` are `GRID_PHYSICAL_PORT7` / `GRID_PHYSICAL_PORT11` from
  `esp32sim/esp32s3/src/board/atech14.rs` (chain index → row-major glass cell). The animation lights chain LED 0..8 on both.
* All three stop when you leave the slide and respect `prefers-reduced-motion`.

## Editing

* Bullets appear one at a time because they carry `class="fragment rise"`. Remove the class for a static slide.
* The role chips at the top-right of each example slide (`<div class="role">`) show which node of the loop the example exercises; `class="on"` highlights, `class="human"` marks the human's part.
* Stats with `class="count" data-to="N"` count up when the slide is shown.
* Colours and type are CSS variables at the top of `index.html`.
