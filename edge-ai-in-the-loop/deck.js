// Demo slides: pick the emulator source before Reveal reads the backgrounds.
// Local: the symlink demos/esp32sim -> ~/work/esp32sim/web. On GitHub Pages: the hosted build under the
// mikroverk organisation, a different origin from the deck (see the key forwarding and 'D' below).
const demoBase = /\.github\.io$/.test(location.hostname) ? 'https://mikroverk.github.io/esp32sim/' : 'demos/esp32sim/index.html';
document.querySelectorAll('section[data-demo-fw]').forEach(sec => {
  sec.setAttribute('data-background-iframe', `${demoBase}?wasm&fw=${sec.dataset.demoFw}`);
});

Reveal.initialize({
  width: 1280, height: 720, margin: 0.04,
  center: false, hash: true, progress: true, controls: false,
  // count the talk's horizontal slides only: the demo extras (vertical) and backup slides (uncounted) show "+"
  slideNumber: slide => {
    if (!slide) return [''];
    const counted = [...document.querySelectorAll('.reveal .slides > section')]
      .filter(s => s.dataset.visibility !== 'uncounted');
    const top = slide.parentElement.closest('section') || slide;
    const i = counted.indexOf(top);
    return i < 0 || top !== slide && Reveal.getIndices(slide).v > 0 ? ['+'] : [i + 1, '/', counted.length];
  },
  transition: 'fade', transitionSpeed: 'fast', backgroundTransition: 'none',
  defaultTiming: 60,
  totalTime: 1550,   // the sum of data-timing; the CandyTron demo comes after
  preloadIframes: true,
  plugins: [ RevealNotes ]
});

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Count-up stats when a slide becomes visible
function countUp(section){
  section.querySelectorAll('.count[data-to]').forEach(el => {
    const to = +el.dataset.to;
    const fmt = n => n >= 1000 ? n.toLocaleString('en').replace(/,/g, ' ') : String(n);
    if (reduce) { el.textContent = fmt(to); return; }
    const t0 = performance.now(), dur = 900;
    (function tick(now){
      const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(to * e));
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  });
}

// Frame player (the FPGA slide): steps through the Verilator frame sprite while the slide is showing
const player = document.getElementById('player');
let playerTimer = null;
function runPlayer(on){
  clearInterval(playerTimer); playerTimer = null;
  if (!player) return;
  const n = +player.dataset.frames, fno = player.querySelector('.fno');
  let i = 0;
  const show = () => { player.style.backgroundPosition = `${i / (n - 1) * 100}% 0`; fno.textContent = 'frame ' + String(i).padStart(3, '0'); };
  show();
  if (!on || reduce) { i = n - 1; show(); return; }
  playerTimer = setInterval(() => { i = (i + 1) % (n + 4); if (i < n) show(); }, 250);   // 4 fps; hold the last frame a second
}

// LED grids (the two-stories slide): light chain LED 0..8 on both modules, through their measured maps
const grids = document.getElementById('grids');
let gridTimer = null;
function runGrids(on){
  clearInterval(gridTimer); gridTimer = null;
  if (!grids) return;
  const maps = { p7: grids.dataset.p7.split(',').map(Number), p11: grids.dataset.p11.split(',').map(Number) };
  grids.querySelectorAll('.grid').forEach(g => { if (!g.children.length) for (let c = 0; c < 9; c++) g.appendChild(document.createElement('b')); });
  let k = 0;
  const show = () => {
    grids.querySelectorAll('.grid').forEach(g => {
      const cell = maps[g.dataset.grid][k];
      [...g.children].forEach((b, c) => { b.classList.toggle('lit', c === cell); b.textContent = c === cell ? k : ''; });
    });
    document.getElementById('chainno').textContent = k;
  };
  show();
  if (!on || reduce) return;
  gridTimer = setInterval(() => { k = (k + 1) % 9; show(); }, 600);
}

// Memory column (the 500 KB slide): the stack eats the RAM and then the code, counting re-entries
let memTimer = null;
function runMem(on){
  cancelAnimationFrame(memTimer);
  const st = document.getElementById('memstack'), cnt = document.getElementById('memcnt'), boom = document.getElementById('memboom');
  if (!st) return;
  st.style.height = '0px'; cnt.textContent = ''; boom.classList.remove('on');
  if (!on) return;
  const total = 3867, full = 400, dur = reduce ? 0 : 3200, t0 = performance.now();
  (function tick(now){
    const p = Math.min(1, (now - t0) / dur);
    st.style.height = Math.round(full * p) + 'px';
    cnt.textContent = Math.round(total * p).toLocaleString('en').replace(/,/g, '\u2009') + ' re-entries';
    if (p < 1) memTimer = requestAnimationFrame(tick); else boom.classList.add('on');
  })(t0);
}

function onSlide(e){
  runMem(!!e.currentSlide.querySelector('#mem'));
  countUp(e.currentSlide);
  runPlayer(!!e.currentSlide.querySelector('#player'));
  runGrids(!!e.currentSlide.querySelector('#grids'));
  if (e.currentSlide.classList.contains('demo-slide')) setTimeout(() => hookDemoKeys(e.currentSlide), 300);
}
Reveal.on('ready', onSlide);
Reveal.on('slidechanged', onSlide);

// Demo slides: the emulator page takes keyboard focus once you click in it, so the deck would stop hearing
// the arrow keys. Two ways back: the ↻ ‹ › buttons in the caption bar, and forwarding of the navigation keys
// from inside the emulator page. Forwarding needs the emulator to be same-origin, which holds locally; on
// GitHub Pages it is not, and the buttons are the way back.
function rebootDemo(){
  const slide = Reveal.getCurrentSlide();
  const f = slide.querySelector('iframe') || Reveal.getSlideBackground(slide)?.querySelector('iframe');
  if (f) f.src = f.src;          // works across origins, unlike contentWindow.location.reload()
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
  const bg = Reveal.getSlideBackground(slide), f = bg && bg.querySelector('iframe');
  if (!f) return;
  const attach = () => {
    try {
      const doc = f.contentDocument;
      if (!doc || doc.__deckKeys) return;
      doc.__deckKeys = true;
      doc.addEventListener('keydown', e => {
        const t = e.target, typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable);
        const go = NAV_KEYS[e.key];
        if (!go || typing) return;
        e.preventDefault();
        go();
        window.focus();
      });
    } catch (err) { /* cross-origin page: buttons still work */ }
  };
  attach();
  f.addEventListener('load', attach);
}

// 'D' reboots the demo on the current slide
Reveal.addKeyBinding({ keyCode: 68, key: 'D', description: 'Reboot demo' }, rebootDemo);
