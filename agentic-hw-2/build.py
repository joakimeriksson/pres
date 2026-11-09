# Builds agentic-hw-2/index.html. Run from the repo root:  python3 agentic-hw-2/build.py
# Takes part one's styles, its "agent grades its own tests" diagram and the robot arm from agentic-hw/index.html.
import re
src = open('agentic-hw/index.html').read()
style = src[src.index('<style>')+7 : src.index('</style>')]

def static(svg):
    svg = svg.replace('class="arrow fragment"', 'class="arrow"').replace(' class="fragment rise"', '').replace(' class="fragment"', '')
    return re.sub(r' data-fragment-index="\d"', '', svg)
a = src.index('<!-- ============ 2 · The problem ============ -->')
selfloop = static(src[src.index('<svg', a) : src.index('</svg>', a)+6])
b = src.index('<!-- ============ 14 · Thanks ============ -->')
arm = src[src.index('<svg', b) : src.index('</svg>', b)+6]

# ---------- the board: part one's IoT board (the one the robot arm presses), defined once as a symbol ----------
BOARD_DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="pcb2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6F4F5"/><stop offset="1" stop-color="#cfe9eb"/></linearGradient>
<symbol id="devboard" viewBox="290 236 282 128">
  <rect x="296" y="282" width="222" height="54" rx="6" fill="url(#pcb2)" stroke="#009BA5" stroke-width="2.5"/>
  <rect x="312" y="298" width="46" height="24" rx="3" fill="#fff" stroke="#009BA5" stroke-width="1.5"/>
  <text x="335" y="315" text-anchor="middle" font-size="11" fill="#009BA5" font-weight="700" font-family="Helvetica,Arial,sans-serif">MCU</text>
  <rect x="366" y="302" width="18" height="16" rx="2" fill="#fff" stroke="#009BA5" stroke-width="1.5"/>
  <rect x="388" y="302" width="18" height="16" rx="2" fill="#fff" stroke="#009BA5" stroke-width="1.5"/>
  <path d="M502 282 L502 246" stroke="#009BA5" stroke-width="2.5" fill="none"/><circle cx="502" cy="243" r="4" fill="#009BA5"/>
  <path d="M518 306 C 546 306, 546 360, 566 360" stroke="#666" stroke-width="5" fill="none" stroke-linecap="round"/>
  <rect x="510" y="298" width="12" height="16" rx="2" fill="#666"/>
  <circle cx="490" cy="310" r="7" fill="#ddd" stroke="#999" stroke-width="1.2"><animate attributeName="fill" values="#ddd;#ddd;#009BA5;#009BA5;#ddd" keyTimes="0;0.45;0.5;0.95;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="490" y="330" text-anchor="middle" font-size="9" fill="#666" font-family="Helvetica,Arial,sans-serif">LED</text>
  <rect x="409" y="272" width="30" height="12" rx="2" fill="#999"/>
  <rect x="412" y="258" width="24" height="16" rx="3" fill="#FFE500" stroke="#222" stroke-width="1.5"/>
  <text x="424" y="300" text-anchor="middle" font-size="9" fill="#666" font-family="Helvetica,Arial,sans-serif">USER 1</text>
  <rect x="445" y="272" width="30" height="12" rx="2" fill="#999"/>
  <rect x="448" y="258" width="24" height="16" rx="3" fill="#FFE500" stroke="#222" stroke-width="1.5"/>
  <text x="460" y="300" text-anchor="middle" font-size="9" fill="#666" font-family="Helvetica,Arial,sans-serif">USER 2</text>
</symbol>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#009BA5"/></marker>
</defs></svg>"""

css_extra = r'''
/* ---------- part 2 ---------- */
.reveal .cols.four{grid-template-columns:repeat(4,1fr);gap:16px}
.reveal .big3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:22px}
.reveal .big3 > div{border-top:4px solid var(--teal);padding-top:10px}
.reveal .big3 b{display:block;font-size:46px;color:var(--teal);line-height:1.05;letter-spacing:-.02em}
.reveal .big3 span{display:block;font-size:18px;color:var(--grey);margin-top:6px;line-height:1.3}
.reveal .plain{font-size:24px;line-height:1.4}
.reveal .plain li{margin-bottom:.5em}
.reveal .lead{font-size:26px;line-height:1.4}
/* section dividers */
.reveal .slides section.divider{display:flex !important;flex-direction:column;justify-content:center;padding-left:96px}
.reveal .divider .bigno{font-size:150px;font-weight:700;color:var(--teal);line-height:.9;letter-spacing:-.04em}
.reveal .divider h1{font-size:68px;margin-top:10px}
.reveal .divider p{font-size:28px;color:var(--grey);margin-top:14px}
/* emulator vs board */
.reveal .vs{display:grid;grid-template-columns:1fr 70px 1fr;align-items:stretch;margin-top:18px}
.reveal .vs .side{background:var(--teal-tint);padding:16px 22px}
.reveal .vs .side.board{background:#e9f0f1;border:2px solid var(--teal)}
.reveal .vs h3{font-size:26px;margin:0 0 2px;color:var(--ink)}
.reveal .vs h3 small{font-size:18px;color:var(--teal);font-weight:700;margin-left:8px}
.reveal .vs ul{font-size:20px;margin-top:10px}
.reveal .vs .mid{display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--grey);font-size:14px;text-align:center}
.reveal .vs .mid b{font-size:36px;color:var(--teal);font-weight:400}
/* steps: who does what */
.reveal .steps{list-style:none;padding:0;margin:14px 0 0;counter-reset:st}
.reveal .steps li{display:grid;grid-template-columns:34px 86px 1fr;gap:12px;align-items:center;padding:7px 0;margin:0;border-bottom:1px solid #e4eeef;font-size:20px}
.reveal .steps li::marker{content:none}
.reveal .steps li::before{counter-increment:st;content:counter(st);font-weight:700;color:var(--teal);font-size:22px;text-align:right}
.reveal .steps code{font-size:15px;color:var(--grey);margin-left:8px}
.reveal .who{display:inline-block;text-align:center;font-size:14px;font-weight:700;padding:3px 0;border-radius:12px}
.reveal .who.you{background:var(--yellow);color:var(--ink)}
.reveal .who.ag{background:var(--teal);color:#fff}
.reveal .who.bd{background:#0d5f63;color:#fff}
/* the afternoon in four steps */
.reveal .flow{display:grid;grid-template-columns:1fr 36px 1fr 36px 1fr 36px 1fr;align-items:stretch;margin-top:34px}
.reveal .flow .st{background:var(--teal-tint);padding:18px 18px}
.reveal .flow .st .n{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:var(--teal);color:#fff;font-weight:700;font-size:20px}
.reveal .flow .st h3{font-size:24px;color:var(--ink);margin:12px 0 8px}
.reveal .flow .st p{font-size:19px;color:var(--grey);margin:0}
.reveal .flow .ar{display:flex;align-items:center;justify-content:center;color:var(--teal);font-size:30px}
/* tasks */
.reveal .tasks3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:16px}
.reveal .task{background:var(--teal-tint);padding:18px 20px 16px;font-size:20px;line-height:1.35;display:flex;flex-direction:column;min-height:400px;box-sizing:border-box}
.reveal .task h3{font-size:25px;margin:0 0 8px;color:var(--ink)}
.reveal .task h3 .n{color:var(--teal);margin-right:8px}
.reveal .task p{margin:0 0 10px}
.reveal .task .done{margin-top:auto;padding-top:10px;border-top:1px solid #b9dfe2;font-size:18.5px}
.reveal .task .done b{color:var(--teal)}
.reveal .tags{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.reveal .tag{font-size:14px;font-weight:700;padding:2px 9px;border-radius:10px;background:#fff;border:1px solid var(--teal);color:var(--teal)}
.reveal .tag.sim{border-color:#999;color:#666}
.reveal .tag.warm{background:var(--yellow);border-color:var(--yellow);color:var(--ink)}
/* ways in, rules, screenshot, status */
.reveal .way{background:var(--teal-tint);padding:18px 20px;font-size:20px;line-height:1.34;min-height:250px;box-sizing:border-box}
.reveal .way h3{font-size:24px;margin:0 0 8px}
.reveal .way p{margin:0 0 8px}
.reveal .way .img{font-size:15.5px;color:var(--grey);font-family:var(--mono)}
.reveal pre.cmd{font-family:var(--mono);font-size:19px;line-height:1.5;background:#1d1f22;color:#e8e8e8;padding:12px 16px;border-radius:6px;margin:0;white-space:pre-wrap;box-shadow:none;width:auto}
.reveal pre.cmd .c{color:#8fc9cd}
.reveal .rule3{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:40px}
.reveal .rule3 > div{border-top:4px solid var(--teal);padding-top:12px}
.reveal .rule3 h3{font-size:27px;line-height:1.2;color:var(--ink);margin:0 0 12px}
.reveal .rule3 p{font-size:21px;line-height:1.4;color:var(--grey)}
.reveal .shot{border:1px solid #ddd;display:block;width:100%}
.reveal .legend{list-style:none;padding:0;margin:0;font-size:19px}
.reveal .legend li{display:grid;grid-template-columns:34px 1fr;gap:10px;margin:0 0 18px;padding:0}
.reveal .legend li::marker{content:none}
.reveal .legend .k{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:var(--teal);color:#fff;font-weight:700;font-size:16px}
.reveal .status{list-style:none;padding:0;margin:22px 0 0;font-size:22px}
.reveal .status li{display:grid;grid-template-columns:40px 1fr 110px;gap:10px;align-items:baseline;padding:11px 0;margin:0;border-bottom:1px solid #e4eeef}
.reveal .status li::marker{content:none}
.reveal .status .ok{color:var(--teal);font-weight:700;font-size:24px}
.reveal .status .no{color:var(--coral);font-weight:700;font-size:24px}
.reveal .status .d{color:var(--grey);font-size:17px;text-align:right}
.reveal .status li.open{background:var(--coral-tint);padding-left:10px;padding-right:10px}
'''
style = style + css_extra

NAV = '<div class="demo-nav"><button data-go="reboot" title="reboot the demo (D)">↻</button><button data-go="prev" title="previous slide (←)">‹</button><button data-go="next" title="next slide (→)">›</button></div>'
T, slides = [], []
def slide(html, t): T.append(t); slides.append(html)
def divider(no, title, sub, note):
    slide(f'''<section class="divider" data-timing="{{t}}">
  <div class="bigno">{no}</div><h1>{title}</h1><p>{sub}</p>
  <aside class="notes">{{ts}}. {note}</aside>
</section>''', 5)

# 1 title -----------------------------------------------------------------
slide('''<!-- ============ Title ============ -->
<section class="title" data-timing="{t}">
  <div style="margin-top:110px;max-width:760px">
    <h1>Hardware in the<br>agentic loop <span class="teal">2</span></h1>
    <p style="font-size:34px;color:var(--grey);margin:30px 0 40px">Two emulators, one dock, one afternoon</p>
    <p style="font-size:22px"><strong>esp32sim</strong><span class="teal"> &nbsp;·&nbsp; </span><strong>Cooja-NG</strong><span class="teal"> &nbsp;·&nbsp; </span><strong>DeviceDock</strong><span class="teal"> &nbsp;·&nbsp; </span><strong>the hackathon</strong></p>
    <p class="small grey">Joakim Eriksson, RISE — November 2026</p>
  </div>
  <svg viewBox="0 0 240 120" width="460" height="230" style="position:absolute;right:64px;bottom:90px" role="img" aria-label="An IoT board with two user buttons"><use href="#devboard" width="240" height="120"/></svg>
  <aside class="notes">{ts}. Part two. Part one was why the hardware has to be in a coding agent's loop. Today, in three parts: the two emulators we use as a fast stand-in for the board, the dock that gets an agent to a real board without handing it your laptop, and then your afternoon. Fifteen minutes.</aside>
</section>''', 20)

# 2 the problem ------------------------------------------------------------
slide('''<!-- ============ The problem ============ -->
<section data-timing="{t}">
  <h2>A coding agent grades its own homework</h2>
  <div class="cols two" style="margin-top:34px;grid-template-columns:1fr 520px">
    <ul class="plain">
      <li>It writes the firmware, writes the tests, runs them, and fixes until everything is <strong>green</strong>.</li>
      <li>But the code, the tests and the expected output all come from <strong>the same model</strong>. They share its blind spots.</li>
      <li><strong class="teal">Green is not the same as correct.</strong> Nobody touched a board.</li>
    </ul>
    <div>''' + selfloop + '''</div>
  </div>
  <aside class="notes">{ts}. The problem from part one, in one slide. An agent is very good at closing a loop it can observe. Left alone, the loop it observes is its own: its code, its tests, its idea of what the output should be. Those share its mistakes. All green, and nobody touched a board.</aside>
</section>''', 40)

# 3 put the board in the loop -------------------------------------------------
slide('''<!-- ============ The board in the loop ============ -->
<section data-timing="{t}">
  <h2>So put a real board in the loop</h2>
  <svg viewBox="0 0 1150 330" width="1150" height="330" style="margin-top:16px" role="img" aria-label="Agent, firmware and a real board in a loop">
    <rect class="node" x="20" y="70" width="230" height="84" rx="14"/>
    <text x="135" y="120" text-anchor="middle" font-size="26" font-weight="700">Agent</text>
    <rect class="node" x="340" y="70" width="230" height="84" rx="14"/>
    <text x="455" y="110" text-anchor="middle" font-size="24" font-weight="700">Firmware</text>
    <text x="455" y="136" text-anchor="middle" font-size="16" fill="#666">it wrote</text>
    <use href="#devboard" x="640" y="4" width="418" height="190"/>
    <rect x="648" y="0" width="170" height="28" rx="14" fill="#FFE500"/>
    <text x="733" y="19" text-anchor="middle" font-size="15" font-weight="700">a human plugs it in</text>
    <path class="arrow" style="marker-end:url(#ar)" d="M252 112 L336 112"/>
    <path class="arrow" style="marker-end:url(#ar)" d="M572 112 L645 112"/>
    <path class="arrow" style="marker-end:url(#ar)" d="M813 160 L813 262 L135 262 L135 160"/>
    <text x="480" y="296" text-anchor="middle" font-size="20"><tspan font-weight="700" fill="#009BA5">what the board really does: </tspan><tspan fill="#666">what it prints · its LEDs · its screen · its radio</tspan></text>
    <circle class="dot" r="9"><animateMotion dur="6s" repeatCount="indefinite" path="M135 112 L455 112 L813 112 L813 262 L135 262 Z"/></circle>
  </svg>
  <p class="lead" style="margin-top:14px">The board does not share the model's blind spots. <strong class="teal">It has the last word.</strong> <span class="grey">In part one we called it the oracle.</span></p>
  <aside class="notes">{ts}. The fix: the loop has to go through something the model did not write. A real board. The agent writes firmware, the board runs it, and what the board actually prints comes back to the agent. Someone still has to plug it in; that is the yellow chip, and later today the human part gets smaller.</aside>
</section>''', 40)

# 4 emulator vs board ----------------------------------------------------------
slide('''<!-- ============ Emulator and board ============ -->
<section data-timing="{t}">
  <h2>Boards are slow and scarce, so add an emulator</h2>
  <div class="vs">
    <div class="side">
      <svg viewBox="0 0 240 120" width="270" height="122" style="opacity:.45;outline:2px dashed #9ab;outline-offset:2px"><use href="#devboard" width="240" height="120"/></svg>
      <h3>Emulator <small>the fast stand-in</small></h3>
      <ul>
        <li>The same firmware file, run in software</li>
        <li>Hundreds of times faster than real time</li>
        <li>As many copies as you like</li>
        <li>Same seed, same run, every time</li>
        <li><strong>Can be wrong: it is software too</strong></li>
      </ul>
    </div>
    <div class="mid"><b>⇄</b>compared<br>with each<br>other</div>
    <div class="side board">
      <svg viewBox="0 0 240 120" width="270" height="122"><use href="#devboard" width="240" height="120"/></svg>
      <h3>Real board <small>the last word</small></h3>
      <ul>
        <li>The real chip, radio and timing</li>
        <li>Real time, and flashing takes a minute</li>
        <li>One per desk, one user at a time</li>
        <li>Noise, temperature, a cable that wiggles</li>
        <li><strong>Is what ships</strong></li>
      </ul>
    </div>
  </div>
  <p class="small grey" style="margin-top:16px">Go fast on the emulator, let the board decide. When the two disagree, one of them just taught you something; timings measured on the board go back into the emulator.</p>
  <aside class="notes">{ts}. Why two things. The board is the truth but slow: flashing takes a minute, there is one of it, it is shared. The emulator runs the same firmware file, hundreds of times faster, as many as you want, deterministic. But it is software, it can be wrong. So you compare them. Part one's three words: board is the oracle, emulator is the proxy, and board measurements calibrate the emulator.</aside>
</section>''', 45)

# 5 divider: emulators -------------------------------------------------------
divider('1', 'Two emulators', 'a fast stand-in for the board: one for single boards, one for whole networks',
        'Part one of three: the two emulators.')

# 6 esp32sim -------------------------------------------------------------------
slide('''<!-- ============ esp32sim ============ -->
<section data-timing="{t}">
  <h2>esp32sim: an ESP32 board, in software</h2>
  <ul class="plain" style="margin-top:26px">
    <li>Runs the board's <strong>real firmware file</strong>, the same binary you would flash, starting from the chip's own boot code.</li>
    <li>ESP32-S3, C3 and C6, with screens, LEDs, buttons and the low-power radio.</li>
    <li>On your laptop, in a browser tab, or as a <em>simulated board</em> in DeviceDock.</li>
  </ul>
  <p style="margin-top:30px;font-size:22px"><strong>How do we know it is right?</strong> <span class="grey">Compared with things the model did not write:</span></p>
  <div class="big3">
    <div><b>0 mismatches</b><span>in 1.26 million instructions, compared with the standard disassembler</span></div>
    <div><b>never diverged</b><span>11 000 steps run side by side with the real chip, over a debug cable</span></div>
    <div><b>205 of 208</b><span>boot lines identical to a real ESP32-C3's (C6: 203 of 204)</span></div>
  </div>
  <aside class="notes">{ts}. The first emulator, for single boards. esp32sim runs the real binary from the chip's boot ROM. It is trusted because it was checked against three references the agent did not write: the disassembler, the real chip stepped alongside over JTAG, and real boot logs. In DeviceDock a simulated ESP32 shows up as a device like any other.</aside>
</section>''', 40)

# 7 esp32sim demo ---------------------------------------------------------------
slide('''<!-- ============ esp32sim live ============ -->
<!-- data-demo picks the emulator, data-demo-q its query: the script turns them into data-background-iframe. -->
<section>
<section data-demo="esp32sim" data-demo-q="?wasm&fw=atech" data-background-interactive class="demo-slide" data-timing="{t}">
  <div class="demo-cap"><strong>Live:</strong> esp32sim in the browser, booting a real board's firmware: display, LEDs, buttons, synth. <span class="grey"><span class="kbd">↓</span> one more</span></div>
  ''' + NAV + '''
  <aside class="notes">{ts} (60 s). The Atech pocket synth's real firmware: boot ROM, bootloader, app. Point at the console and the display; enable audio if the room allows. The sub-slide below is an extra: skip it if late.</aside>
</section>
<section data-demo="esp32sim" data-demo-q="?wasm&fw=c6-rpl-net" data-background-interactive class="demo-slide" data-timing="0">
  <div class="demo-cap"><strong>Extra:</strong> two emulated ESP32-C6 boards running Contiki-NG: one is the network root, the other joins and sends a UDP request every 10 s.</div>
  ''' + NAV + '''
  <aside class="notes">Extra. RPL root and client, 6LoWPAN and CSMA end to end over the emulated 802.15.4 radio.</aside>
</section>
</section>''', 60)

# 8 Cooja-NG ---------------------------------------------------------------------
slide('''<!-- ============ Cooja-NG ============ -->
<section data-timing="{t}">
  <h2>Cooja-NG: a whole wireless network, in software</h2>
  <ul class="plain" style="margin-top:26px">
    <li>Every node runs its <strong>real firmware file</strong>: Contiki-NG, and also Zephyr, RIOT and OpenThread.</li>
    <li>A simulated radio connects them: hundreds of nodes on one laptop.</li>
    <li>Same seed, same run: a bug that shows up once shows up every time.</li>
  </ul>
  <div class="big3" style="margin-top:30px">
    <div><b>~1600×</b><span>faster than real time: two nodes on Apple Silicon (300–700× on the ARM boards)</span></div>
    <div><b>93 / 93</b><span>of Contiki-NG's own simulation tests pass</span></div>
    <div><b>14 of 15</b><span>a four-year-old "flaky" test, turned into a number an agent could fix</span></div>
  </div>
  <p style="margin-top:24px;font-size:21px">In DeviceDock it is the command <code>cngsim</code>: <span class="grey">try the image before you flash it. On hello-world it prints exactly what the real LaunchPad prints.</span></p>
  <aside class="notes">{ts}. The second emulator, for networks. Contiki-NG's simulator rewritten in C, fast and deterministic. Numbers from its README. Determinism is what an agent needs: "flaky" is not a work item, "14 of 15" is. Inside DeviceDock it is the cngsim command, checked against a real LaunchPad.</aside>
</section>''', 40)

# 9 Cooja-NG demo -------------------------------------------------------------------
slide('''<!-- ============ Cooja-NG live ============ -->
<section>
<section data-demo="cooja" data-demo-q="?wasm=grid100" data-background-interactive class="demo-slide" data-timing="{t}">
  <div class="demo-cap"><strong>Live:</strong> Cooja-NG in the browser: 100 nodes, each running real Contiki-NG firmware, forming a network. <span class="grey"><span class="kbd">↓</span> one more</span></div>
  ''' + NAV + '''
  <aside class="notes">{ts} (60 s). One hundred MSP430 nodes, each running the real firmware instruction by instruction, forming an RPL network in a browser tab with no server. Point at the network forming. The sub-slide below is an extra: skip it if late.</aside>
</section>
<section data-demo="cooja" data-demo-q="?wasm=mixed" data-background-interactive class="demo-slide" data-timing="0">
  <div class="demo-cap"><strong>Extra:</strong> three different chips in one network: Sky (MSP430), CC2538 and nRF52840 (ARM), each with its own Contiki-NG build.</div>
  ''' + NAV + '''
  <aside class="notes">Extra. Mixed platforms on one radio medium, one shared event queue.</aside>
</section>
</section>''', 60)

# 10 divider: DeviceDock --------------------------------------------------------------
divider('2', 'DeviceDock', 'getting the agent to a real board, safely', 'Part two of three: the dock.')

# 11 the sandbox problem ---------------------------------------------------------------
slide('''<!-- ============ The sandbox problem ============ -->
<section data-timing="{t}">
  <h2>The agent belongs in a box. The board is on your USB.</h2>
  <svg viewBox="0 0 1150 300" width="1150" height="300" style="margin-top:12px" role="img" aria-label="A board plugged into a laptop; the agent's sandbox inside the laptop has no USB">
    <use href="#devboard" x="10" y="104" width="260" height="118"/>
    <path d="M266 220 C 300 222, 320 224, 352 224" stroke="#666" stroke-width="4.6" fill="none" stroke-linecap="round"/>
    <rect x="350" y="10" width="620" height="250" rx="16" fill="#fafafa" stroke="#333" stroke-width="3"/>
    <path d="M318 260 H1002 L1036 292 H284 Z" fill="#d9dde1" stroke="#333" stroke-width="2"/>
    <text x="660" y="284" text-anchor="middle" font-size="15" fill="#666">your laptop</text>
    <rect x="378" y="38" width="260" height="196" rx="10" fill="#FFF8CC" stroke="#e0c400" stroke-width="2"/>
    <text x="508" y="76" text-anchor="middle" font-size="21" font-weight="700">Everything else</text>
    <text x="508" y="110" text-anchor="middle" font-size="17" fill="#555">your files · SSH keys</text>
    <text x="508" y="134" text-anchor="middle" font-size="17" fill="#555">logins · other projects</text>
    <text x="508" y="158" text-anchor="middle" font-size="17" fill="#555">the USB ports</text>
    <rect x="664" y="38" width="280" height="196" rx="10" fill="#E6F4F5" stroke="#009BA5" stroke-width="2.5"/>
    <text x="804" y="76" text-anchor="middle" font-size="21" font-weight="700">Sandbox (Docker)</text>
    <text x="804" y="110" text-anchor="middle" font-size="17" fill="#555">the agent, compilers,</text>
    <text x="804" y="134" text-anchor="middle" font-size="17" fill="#555">flashing tools</text>
    <rect x="726" y="170" width="156" height="34" rx="17" fill="#FBEBEA" stroke="#D9534F" stroke-width="1.5"/>
    <text x="804" y="193" text-anchor="middle" font-size="17" font-weight="700" fill="#D9534F">✕ no USB port</text>
  </svg>
  <ul class="plain" style="margin-top:10px;font-size:22px">
    <li>An agent runs shell commands for you. Keep it in a sandbox, away from your files and keys.</li>
    <li>But then it cannot reach the board, and you don't want to hand it every USB port you have.</li>
  </ul>
  <aside class="notes">{ts}. The practical problem. A coding agent runs commands; you want it in a sandbox, not loose on your laptop with your keys. A Docker sandbox has no USB. And you don't want to give it all your ports, just the one board you chose.</aside>
</section>''', 40)

# 12 DeviceDock diagram ------------------------------------------------------------------
slide('''<!-- ============ DeviceDock ============ -->
<section data-timing="{t}">
  <h2>DeviceDock: your browser lends the agent one board</h2>
  <svg viewBox="0 0 1150 210" width="1150" height="210" style="margin-top:14px" role="img" aria-label="Board, DeviceDock page, backend and sandbox in a chain">
    <use href="#devboard" x="0" y="34" width="210" height="105"/>
    <text x="105" y="160" text-anchor="middle" font-size="18" font-weight="700">Your board</text>
    <rect class="node em" x="262" y="40" width="262" height="104" rx="14"/>
    <text x="393" y="80" text-anchor="middle" font-size="20" font-weight="700">DeviceDock page</text>
    <text x="393" y="104" text-anchor="middle" font-size="14" fill="#666">in Chrome: you share one board</text>
    <text x="393" y="122" text-anchor="middle" font-size="14" fill="#666">and you approve</text>
    <rect x="353" y="10" width="80" height="24" rx="12" fill="#FFE500"/>
    <text x="393" y="27" text-anchor="middle" font-size="13" font-weight="700">you</text>
    <rect class="node" x="592" y="40" width="230" height="104" rx="14"/>
    <text x="707" y="80" text-anchor="middle" font-size="20" font-weight="700">Backend</text>
    <text x="707" y="104" text-anchor="middle" font-size="14" fill="#666">on your laptop:</text>
    <text x="707" y="122" text-anchor="middle" font-size="14" fill="#666">who may use what, when</text>
    <rect class="node si" x="890" y="40" width="256" height="104" rx="14"/>
    <text x="1018" y="74" text-anchor="middle" font-size="20" font-weight="700" fill="#fff">Sandbox</text>
    <text x="1018" y="98" text-anchor="middle" font-size="14" fill="#fff">Claude Code · Codex · OpenCode</text>
    <text x="1018" y="118" text-anchor="middle" font-size="14" fill="#fff">gcc · OpenOCD · esptool · cngsim</text>
    <path class="arrow" style="marker-start:url(#ar);marker-end:url(#ar)" d="M214 92 L258 92"/>
    <path class="arrow" style="marker-start:url(#ar);marker-end:url(#ar)" d="M528 92 L588 92"/>
    <path class="arrow" style="marker-start:url(#ar);marker-end:url(#ar)" d="M826 92 L886 92"/>
    <text x="558" y="174" text-anchor="middle" font-size="14" fill="#666">USB stays with the browser</text>
    <text x="1018" y="174" text-anchor="middle" font-size="14" fill="#666">reaches the board only through the dock</text>
  </svg>
  <div class="cols two" style="margin-top:10px;gap:30px">
    <div>
      <h3>What the agent gets</h3>
      <ul class="small" style="font-size:20px">
        <li>A serial port address that <strong>esptool, idf.py and pyserial</strong> use unchanged, reset into the bootloader included</li>
        <li>A tunnel so <strong>OpenOCD</strong> can flash a LaunchPad through its debug probe</li>
        <li><code>device list</code>, <code>send</code>, <code>monitor</code>, also as MCP tools</li>
      </ul>
    </div>
    <div>
      <h3>What it does not get</h3>
      <ul class="small" style="font-size:20px">
        <li>No USB device, no access to your laptop, no Docker socket</li>
        <li>Boards you did not share</li>
        <li>Your logins: agents log in inside the sandbox</li>
      </ul>
    </div>
  </div>
  <aside class="notes">{ts}. DeviceDock's idea: the browser owns the USB port, through Web Serial and WebUSB. You share one board from a page; a small backend decides who may use it and when; the sandbox reaches it only through that. To the agent's tools it looks normal: esptool and pyserial get a serial URL, OpenOCD gets a debug-probe tunnel.</aside>
</section>''', 50)

# 13 one request step by step --------------------------------------------------------------
slide('''<!-- ============ One request, step by step ============ -->
<section data-timing="{t}">
  <h2>One request, step by step</h2>
  <p class="sub">A TI LaunchPad running Contiki-NG, from DeviceDock's quick start</p>
  <ol class="steps">
    <li><span class="who you">you</span><span>Ask: <em>"Make hello-world print a counter, flash it to the LaunchPad and show me the output."</em></span></li>
    <li><span class="who ag">agent</span><span>Edits <code style="margin:0">hello-world.c</code> and builds it <code>make TARGET=simplelink BOARD=launchpad/cc1352r1</code></span></li>
    <li><span class="who ag">agent</span><span>Tries it on the simulator first <code>cngsim run hello.cc1352r1-launchpad -t 25s</code></span></li>
    <li><span class="who you">you</span><span>Click <strong>Approve</strong> in the page when it opens the debug probe <code>device probe-open &lt;id&gt;</code></span></li>
    <li><span class="who ag">agent</span><span>Flashes through the browser with OpenOCD: about a minute</span></li>
    <li><span class="who bd">board</span><span>Runs it and prints what it really does <code>device monitor &lt;id&gt; --seconds 20</code></span></li>
    <li><span class="who ag">agent</span><span>Reports what ran where: "on the simulator" and "on the board" are separate claims</span></li>
  </ol>
  <p class="small grey" style="margin-top:14px">With <em>Autonomous</em> switched on for the board, step 4 needs no click and the agent can go round again by itself.</p>
  <aside class="notes">{ts}. What one round trip looks like. You ask; the agent edits and builds; it tries the image in cngsim; you approve the debug session; OpenOCD flashes through the browser in about a minute; the board prints; the agent reports, keeping simulator and board results apart. Commands are from the DeviceDock quick start.</aside>
</section>''', 60)

# 14 screenshot ------------------------------------------------------------------------------
slide('''<!-- ============ What it looks like ============ -->
<section data-timing="{t}">
  <h2>What it looks like</h2>
  <div style="display:grid;grid-template-columns:770px 1fr;gap:30px;margin-top:12px;align-items:start">
    <img class="shot" src="assets/devicedock.jpg" alt="The DeviceDock page: terminals on the left, devices and a serial monitor on the right">
    <ol class="legend">
      <li><span class="k">1</span><span><strong>Terminals</strong> into the sandbox: a shell, and the agent</span></li>
      <li><span class="k">2</span><span><strong>Devices</strong> you shared: serial ports, debug probes, simulated ESP32 boards</span></li>
      <li><span class="k">3</span><span><strong>Per device</strong>: take it back, or let the agent work alone for 15 or 60 minutes</span></li>
      <li><span class="k">4</span><span><strong>Serial monitor</strong>: every byte in and out</span></li>
    </ol>
  </div>
  <p class="foot small grey">One command starts it all: <code>./devicedock.sh</code></p>
  <aside class="notes">{ts}. The page itself. Terminals into the sandbox on the left; on the right the devices you shared, each with its own controls, and a monitor of every byte.</aside>
</section>''', 30)

# 15 approvals ---------------------------------------------------------------------------------
slide('''<!-- ============ Approvals ============ -->
<section data-timing="{t}">
  <h2>You approve each write, or let it run for a while</h2>
  <div class="cols two" style="margin-top:28px">
    <div class="card" style="font-size:22px">
      <h3 style="font-size:26px">Default: you click</h3>
      <ul>
        <li>Every time the agent writes to a <strong>real</strong> board, the page asks you first.</li>
        <li>Opening a debug probe needs one approval.</li>
        <li>Simulated boards need none: nothing can break.</li>
      </ul>
    </div>
    <div class="card" style="font-size:22px">
      <h3 style="font-size:26px">Autonomous: 15 or 60 minutes</h3>
      <ul>
        <li>You switch it on for one board. At most 2 hours.</li>
        <li>It ends by itself, or when you unplug, take the board back or close the tab.</li>
        <li>Meanwhile the agent builds, flashes and reads on its own.</li>
      </ul>
    </div>
  </div>
  <p style="margin-top:26px;font-size:20px" class="grey">Always: one user per board at a time, and no automatic retries of a write that may already have happened.</p>
  <aside class="notes">{ts}. The safety model in two cards. By default every physical write waits for your click. For the hackathon loop you can let one board run autonomously for 15 or 60 minutes; it switches itself off. Underneath, one client per device and no automatic retries.</aside>
</section>''', 40)

# 16 status -------------------------------------------------------------------------------------
slide('''<!-- ============ Status ============ -->
<section data-timing="{t}">
  <h2>What works today, and what is still open</h2>
  <ul class="status">
    <li><span class="ok">✓</span><span><strong>ESP32:</strong> esptool talks to a real board through the browser: into the bootloader, reads the chip</span><span class="d">7 Nov</span></li>
    <li><span class="ok">✓</span><span><strong>TI LaunchPad:</strong> flashed and verified through its debug probe; its output reaches the agent</span><span class="d">9 Nov</span></li>
    <li><span class="ok">✓</span><span><strong>cngsim:</strong> hello-world prints the same as on the real LaunchPad</span><span class="d"></span></li>
    <li><span class="ok">✓</span><span><strong>Simulated ESP32 boards</strong> in the page: console, REPL, reset</span><span class="d"></span></li>
    <li class="open"><span class="no">○</span><span><strong>Still open:</strong> writing flash on a real ESP32 · MicroPython's mpremote · flashing a simulated ESP32 through the dock · cngsim nodes as devices · an agent doing the whole loop alone</span><span class="d">today?</span></li>
  </ul>
  <p class="foot teal" style="font-size:22px"><strong>The open row is a task list.</strong></p>
  <aside class="notes">{ts}. Honest status, from DeviceDock's own notes. Verified on real hardware: an ESP32 entering its bootloader through the bridge, a LaunchPad flashed and verified through its probe. Open: real ESP32 flash writes, mpremote, flashing a simulated ESP32 through the dock, cngsim nodes as devices, and an agent running the full loop on its own. Those are hackathon tasks.</aside>
</section>''', 35)

# 17 divider: afternoon ---------------------------------------------------------------------------
divider('3', 'Your afternoon', 'half a day, a board or a simulator, and a coding agent', 'Part three: over to you.')

# 18 the afternoon in four steps ----------------------------------------------------------------------
slide('''<!-- ============ The afternoon ============ -->
<section data-timing="{t}">
  <h2>The afternoon in four steps</h2>
  <div class="flow">
    <div class="st"><span class="n">1</span><h3>Pick a setup</h3><p>An ESP32, a LaunchPad, your own board, or just a simulator.</p></div>
    <div class="ar">→</div>
    <div class="st"><span class="n">2</span><h3>Pick a task</h3><p>From the next slides, or your own idea, as long as it has a "done when".</p></div>
    <div class="ar">→</div>
    <div class="st"><span class="n">3</span><h3>Let the agent loop</h3><p>It builds, flashes and reads. You watch, approve and steer.</p></div>
    <div class="ar">→</div>
    <div class="st"><span class="n">4</span><h3>Show the evidence</h3><p>Two minutes at the end: what the board said, not what the agent said.</p></div>
  </div>
  <aside class="notes">{ts}. The whole afternoon in one line: pick a setup, pick a task, let the agent loop while you supervise, and show the evidence at the end.</aside>
</section>''', 35)

# 19 four ways in -----------------------------------------------------------------------------------
slide('''<!-- ============ Four ways in ============ -->
<section data-timing="{t}">
  <h2>Step 1: four ways in</h2>
  <p class="sub">Everyone runs the same DeviceDock. Pick what is on your desk.</p>
  <div class="cols four">
    <div class="way"><h3>ESP32 board</h3><p class="img">image: esp32 or full</p><p>Share its serial port. Flash with <code>idf.py -p &lt;address from device list&gt; flash monitor</code>.</p></div>
    <div class="way"><h3>TI LaunchPad</h3><p class="img">image: contiki</p><p>Share the serial port <em>and</em> the debug probe. The quick start's hello-world is the worked example.</p></div>
    <div class="way"><h3>Simulator only</h3><p class="img">any image</p><p><em>＋ Simulated esp32s3 / c3 / c6</em> in the page, or <code>cngsim</code> for Contiki-NG boards and networks.</p></div>
    <div class="way"><h3>Your own board</h3><p class="img">any image</p><p>Any serial console works, and CMSIS-DAP debug probes. esptool, OpenOCD and mpremote are installed.</p></div>
  </div>
  <pre class="cmd" style="margin-top:26px"><span class="c"># the sandbox image is 3–12 GB: start this now if you have not</span>
export DEVICEDOCK_VARIANT=full        <span class="c"># or base · contiki · esp32</span>
./devicedock.sh                       <span class="c"># then in its console: o (page link) · login claude · sh</span>
cd /workspace &amp;&amp; claude               <span class="c"># the agent reads /workspace/AGENTS.md</span></pre>
  <aside class="notes">{ts}. Four ways in, same tool. ESP32s flash with ESP-IDF through the serial address from device list. LaunchPads flash with OpenOCD through the probe tunnel; the quick start walks through it. No board: simulated ESP32s in the page or cngsim. Your own board works if it has a serial console or a CMSIS-DAP probe. Start the image download now: up to 12 GB.</aside>
</section>''', 50)

# 20 rules ---------------------------------------------------------------------------------------------
slide('''<!-- ============ Rules ============ -->
<section data-timing="{t}">
  <h2>Three rules for the afternoon</h2>
  <div class="rule3">
    <div><h3><span class="teal">1</span> Done means evidence the model did not write</h3><p>The board's own output, a diff against a real boot, "N of M" runs. Green tests the agent wrote itself do not count.</p></div>
    <div><h3><span class="teal">2</span> Say where it ran</h3><p>"On the simulator" is not "on the board". When they differ, decide: emulator bug, or a fact about the board? Write it down.</p></div>
    <div><h3><span class="teal">3</span> Keep the receipts</h3><p>The command, the log, the commit, and where the agent was wrong. If it fails the same way three times, it stops and you decide.</p></div>
  </div>
  <div class="quote warn" style="font-style:normal;font-size:21px;margin-top:56px;display:grid;grid-template-columns:120px 1fr;gap:18px;align-items:center">
    <strong class="coral">Before you flash</strong>
    <span>Back up the factory firmware of a board you care about (quick start §4). Autonomous mode is per board, opt-in, and switches itself off.</span>
  </div>
  <aside class="notes">{ts}. Three rules, all from part one. Evidence from outside the model. Be explicit about simulator versus board. Keep receipts, including the agent's mistakes; DeviceDock's agent instructions already tell it to stop after the same failure three times. And back up firmware before you overwrite it.</aside>
</section>''', 35)

# 21-22 tasks -------------------------------------------------------------------------------------------
def task(n, title, tags, body, done):
    tg = ''.join(f'<span class="tag{(" "+c) if c else ""}">{t}</span>' for t, c in tags)
    return f'''    <div class="task"><h3><span class="n">{n}</span>{title}</h3>
      <div class="tags">{tg}</div>
      <p>{body}</p>
      <p class="done"><b>Done when</b> {done}</p></div>'''
slide('''<!-- ============ Tasks: start here ============ -->
<section data-timing="{t}">
  <h2>Step 2: suggested tasks — start here</h2>
  <div class="tasks3">
''' + '\n'.join([
    task(1, 'First loop', [('warm-up','warm'),('ESP32',''),('LaunchPad','')],
         'Ask the agent to make hello-world print a counter, build it, flash it and show you the output. Then switch on Autonomous and let it make the next change alone.',
         "the board's own serial output shows the change."),
    task(2, 'Sim first, then silicon', [('ESP32',''),('esp32sim','sim')],
         'Run one image on a simulated ESP32 and on a real one. Let the agent compare the two boot logs and sort every difference: emulator bug, or a fact about the board?',
         'every line of the difference is explained. Bonus: an esp32sim issue with the log.'),
    task(3, 'Make a flaky test a number', [('cngsim','sim'),('no board needed','sim')],
         'Pick a Contiki-NG test or example, run it in cngsim with many different seeds, and let the agent hunt whatever fails.',
         'you have "N of M" before and after, and the seed that reproduces it.'),
]) + '''
  </div>
  <aside class="notes">{ts}. Three to start with. One is the warm-up everyone can do: the step-by-step slide, on your board. Two is the sim-versus-silicon comparison. Three needs no board at all. Point at the "done when" lines: each names evidence the model cannot produce by itself.</aside>
</section>''', 60)
slide('''<!-- ============ Tasks: go further ============ -->
<section data-timing="{t}">
  <h2>Step 2: suggested tasks — go further</h2>
  <div class="tasks3">
''' + '\n'.join([
    task(4, 'Give the agent eyes', [('any board',''),('your own','')],
         'Write a self-test firmware whose output a program can check: pins, LEDs, buttons, sensors. Let the agent work out how your board is wired from what it reports.',
         'the pin map comes from the board, not from a photo or a guess from the datasheet.'),
    task(5, 'Two nodes, one radio', [('2 × LaunchPad',''),('cngsim','sim')],
         "Build Contiki-NG's rpl-udp example, prove it in cngsim with two nodes, then flash a server and a client onto two real boards.",
         'both real boards agree, and you can say what differed from the simulation.'),
    task(6, 'Close an open row', [('your own',''),('DeviceDock','')],
         'Verify what the dock has not yet: writing flash on a real ESP32, mpremote, a new debug probe. Or make a cngsim node show up in <code>device list</code>.',
         'a verification note with the log is in a pull request.'),
]) + '''
  </div>
  <aside class="notes">{ts}. Three more. Four is the one-LED lesson from part one: let the board tell you its wiring. Five is a real radio link, simulated first. Six improves the dock itself, from its open row. Your own idea is welcome, as long as it has a "done when".</aside>
</section>''', 60)

# 23 show and tell ------------------------------------------------------------------------------------------
slide('''<!-- ============ Show and tell ============ -->
<section data-timing="{t}">
  <h2>Step 4: two minutes, one receipt</h2>
  <div class="cols three" style="margin-top:30px">
    <div class="card" style="font-size:21px"><p><span class="num">1</span><strong>What you asked for</strong></p><p class="small grey">The task, the board, the prompt that got it going.</p></div>
    <div class="card" style="font-size:21px"><p><span class="num">2</span><strong>The evidence</strong></p><p class="small grey">The board's output, the diff, the number. Say where it ran.</p></div>
    <div class="card" style="font-size:21px"><p><span class="num">3</span><strong>Where the agent was wrong</strong></p><p class="small grey">And what caught it: the board, the simulator, or you.</p></div>
  </div>
  <p style="margin-top:34px;font-size:23px">Found a bug in esp32sim, Cooja-NG or DeviceDock? <strong class="teal">An issue with the log is the best receipt of the day.</strong></p>
  <aside class="notes">{ts}. How we close: two minutes per team, three things. Number three matters most: where the agent was confidently wrong, and what in the loop caught it.</aside>
</section>''', 30)

# 24 over to you -----------------------------------------------------------------------------------------------
slide('''<!-- ============ Over to you ============ -->
<section data-timing="{t}">
  <div class="cols two" style="grid-template-columns:1fr 1.1fr;align-items:center;margin-top:40px">
    <div>
      <h1 style="font-size:64px">Over to you</h1>
      <p class="grey" style="font-size:22px;margin-top:26px">Joakim Eriksson, RISE</p>
      <p class="small grey" style="line-height:1.6">github.com/joakimeriksson/devicedock<br>mikroverk.github.io/esp32sim<br>mikroverk.github.io/cooja-ng<br>part one: joakimeriksson.github.io/pres/agentic-hw/</p>
    </div>
    <div>
      ''' + arm + '''
    </div>
  </div>
  <aside class="notes">{ts}. Links: DeviceDock with its quick start, the two emulators, and part one. The arm is still pressing the buttons that were left for the human. This afternoon the agent presses them, and you check. Happy hacking.</aside>
</section>''', 15)

total = sum(T)
assert total == 900, total
out, cum = [], 0
for html, t in zip(slides, T):
    out.append(html.replace('{t}', str(t)).replace('{ts}', f"{cum//60}:{cum%60:02d}"))
    cum += t

script = r'''
<script src="vendor/reveal.js"></script>
<script src="vendor/notes.js"></script>
<script>
// Demo slides: data-demo picks the emulator, data-demo-q its query string. Set before Reveal reads the backgrounds.
// esp32sim: the local symlink (demos/esp32sim -> ~/work/esp32sim/web) on localhost, the hosted build on GitHub Pages.
// Cooja-NG: always the hosted WebAssembly build.
const onPages = /\.github\.io$/.test(location.hostname);
const DEMO = {
  esp32sim: onPages ? 'https://mikroverk.github.io/esp32sim/' : 'demos/esp32sim/index.html',
  cooja: 'https://mikroverk.github.io/cooja-ng/player.html',
};
document.querySelectorAll('section[data-demo]').forEach(sec => {
  sec.setAttribute('data-background-iframe', DEMO[sec.dataset.demo] + (sec.dataset.demoQ || ''));
});

Reveal.initialize({
  width: 1280, height: 720, margin: 0.04,
  center: false, hash: true, progress: true, controls: false,
  slideNumber: slide => [Reveal.getIndices(slide).h + 1, '/', Reveal.getHorizontalSlides().length],   // talk slides only, not the demo extras
  transition: 'fade', transitionSpeed: 'fast', backgroundTransition: 'none',
  defaultTiming: 40,
  totalTime: ''' + str(total) + ''',
  preloadIframes: false,       // demos boot when their slide appears, so the audience sees the boot
  plugins: [ RevealNotes ]
});

// Demo slides: a click inside an emulator takes keyboard focus. The ↻ ‹ › buttons always work; arrow keys are
// forwarded only when the emulator is same-origin (esp32sim served locally).
function rebootDemo(){
  const f = Reveal.getSlideBackground(Reveal.getCurrentSlide())?.querySelector('iframe');
  if (f) f.src = f.src;
}
document.querySelectorAll('.demo-nav button').forEach(b => b.addEventListener('click', e => {
  e.stopPropagation();
  const go = b.dataset.go;
  go === 'reboot' ? rebootDemo() : go === 'next' ? Reveal.right() : Reveal.left();
  window.focus();
}));
const NAV_KEYS = { ArrowRight: () => Reveal.right(), ArrowLeft: () => Reveal.left(), ArrowDown: () => Reveal.down(), ArrowUp: () => Reveal.up(),
                   PageDown: () => Reveal.next(), PageUp: () => Reveal.prev(), Escape: () => Reveal.toggleOverview() };
function hookDemoKeys(slide){
  const f = Reveal.getSlideBackground(slide)?.querySelector('iframe');
  if (!f) return;
  const attach = () => {
    try {
      const doc = f.contentDocument;
      if (!doc || doc.__deckKeys) return;
      doc.__deckKeys = true;
      doc.addEventListener('keydown', e => {
        const t = e.target, typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
        const go = NAV_KEYS[e.key];
        if (!go || typing) return;
        e.preventDefault(); go(); window.focus();
      });
    } catch (err) { /* cross-origin: the buttons still work */ }
  };
  attach();
  f.addEventListener('load', attach);
}
const onDemo = e => { if (e.currentSlide.classList.contains('demo-slide')) setTimeout(() => hookDemoKeys(e.currentSlide), 300); };
Reveal.on('slidechanged', onDemo);
Reveal.on('ready', onDemo);
Reveal.addKeyBinding({ keyCode: 68, key: 'D', description: 'Reboot demo' }, rebootDemo);
</script>
</body>
</html>
'''

html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<title>Hardware in the agentic loop 2 — Joakim Eriksson, RISE</title>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<link rel="stylesheet" href="vendor/reset.css">\n<link rel="stylesheet" href="vendor/reveal.css">\n'
        '<style>' + style + '</style>\n</head>\n<body>\n' + BOARD_DEFS + '\n<div class="reveal">\n<div class="slides">\n\n'
        + '\n\n'.join(out) + '\n\n</div>\n</div>\n' + script)
open('agentic-hw-2/index.html', 'w').write(html)
print('slides', len(T), 'total', total, 'bytes', len(html))
