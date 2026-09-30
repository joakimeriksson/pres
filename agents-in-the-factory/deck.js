// Demo slides: the testbed viewer as the slide background. demos/viewer is a copy of the testbed's viewer and
// demos/runs holds the recordings, so the deck is self-contained: no testbed and no network needed.
document.querySelectorAll('section[data-demo-src]').forEach(sec => {
  sec.setAttribute('data-background-iframe', 'demos/' + sec.dataset.demoSrc);
});

Reveal.initialize({
  width: 1280, height: 720, margin: 0.04,
  center: false, hash: true, progress: true, controls: false,
  // count the talk's slides only; backup slides (data-visibility="uncounted") show "+"
  slideNumber: slide => {
    const counted = [...document.querySelectorAll('.reveal .slides > section')]
      .filter(s => s.dataset.visibility !== 'uncounted');
    const i = counted.indexOf(slide);
    return i < 0 ? ['+'] : [i + 1, '/', counted.length];
  },
  transition: 'fade', transitionSpeed: 'fast', backgroundTransition: 'none',
  defaultTiming: 60,
  totalTime: 1800,
  preloadIframes: true,
  plugins: [ RevealNotes ]
});

// Count-up stats when a slide becomes visible (respects reduced motion)
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
function countUp(section){
  section.querySelectorAll('.count[data-to]').forEach(el => {
    const to = +el.dataset.to;
    const fmt = n => n >= 1000 ? n.toLocaleString('en').replace(/,/g, ' ') : String(n);
    if (reduce) { el.textContent = fmt(to); return; }
    const t0 = performance.now(), dur = 900;
    (function tick(now){
      const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(to * e));
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  });
}
Reveal.on('ready', e => countUp(e.currentSlide));
Reveal.on('slidechanged', e => countUp(e.currentSlide));

// Demo slides: the viewer takes keyboard focus once you click in it, so the deck would stop hearing the
// arrow keys. Two ways back: the ‹ › buttons in the caption bar, and forwarding of the navigation keys
// from inside the (same-origin) viewer page to the deck.
document.querySelectorAll('.demo-nav button').forEach(b => b.addEventListener('click', e => {
  e.stopPropagation();
  b.dataset.go === 'next' ? Reveal.right() : Reveal.left();
  window.focus();
}));
const NAV_KEYS = { ArrowRight: () => Reveal.right(), ArrowLeft: () => Reveal.left(),
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
Reveal.on('slidechanged', e => { if (e.currentSlide.classList.contains('demo-slide')) setTimeout(() => hookDemoKeys(e.currentSlide), 300); });
Reveal.on('ready', e => { if (e.currentSlide.classList.contains('demo-slide')) setTimeout(() => hookDemoKeys(e.currentSlide), 300); });

// 'D' reloads the demo on the current slide
Reveal.addKeyBinding({ keyCode: 68, key: 'D', description: 'Reload demo' }, () => {
  const slide = Reveal.getCurrentSlide();
  const f = Reveal.getSlideBackground(slide)?.querySelector('iframe');
  if (f) f.contentWindow.location.reload();
});
