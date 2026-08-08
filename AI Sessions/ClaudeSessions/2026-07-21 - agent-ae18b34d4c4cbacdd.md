# Session agent-ae18b34d4c4cbacdd
**Date:** 2026-07-21 | **Session ID:** `agent-ae18b34d4c4cbacdd`

---

## 👤 User *(20:00:47)*

Você audita a QUALIDADE VISUAL de uma legenda do MCORCH (overlay 9:16 queimado sobre vídeo).

Estilo: "Neon" (slug caption-neon-glow-9x16).

LEIA (Read):
1. O template: /home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/templates/caption-neon-glow-9x16.html — foque no CSS + em applyProps/applyFrame.
2. A prévia renderizada (imagem): /home/gcrUX/htdocs/constellation-orchestra/public/caption-previews/caption-neon-glow-9x16.png — OLHE de fato.
3. O BENCHMARK aprovado pelo Sovereign (compare contra ele): /home/gcrUX/htdocs/constellation-orchestra/public/caption-previews/motion-graphics-hero-9x16.png + /home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/templates/motion-graphics-hero-9x16.html.

Julgue: legibilidade (contraste, tamanho, safe-area), polimento do movimento, hierarquia tipográfica, sofisticação (o benchmark é "card/kicker flutuante", NÃO rodapé karaoke). Se o estilo é motion-graphics-hero-9x16, marque keep_as_is=true (é a referência).

Proponha melhorias SEGURAS (só CSS/timing) que NÃO quebrem: (a) o contrato applyProps({beats,fps,durationSec})/applyFrame(i,total), (b) o layout px em 1080x1920, (c) a transparência do fundo (é overlay). Nada de reescrever a estrutura. Se já está ótimo, diga keep_as_is=true e deixe safe_improvements vazio. Retorne o objeto estruturado.

## 🤖 Claude *(20:00:56)*

<details>
<summary>💭 Thinking Process</summary>

I need to load the template file, preview image, and benchmark files to understand what I'm working with.

</details>


## 🤖 Claude *(20:00:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/templates/caption-neon-glow-9x16.html"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	<!DOCTYPE html>
> 2	<!--
> 3	  caption-neon-glow-9x16 — MCORCH caption style "Neon" (video-repurpose FR-VR-017).
> 4	  TRANSPARENT background: rendered by render-core `renderAlphaFrames` (omitBackground:true) → RGBA PNG seq,
> 5	  composited OVER real reframed footage by segment-core (FFmpeg overlay=0:0).
> 6	  Look: stacked text-shadow halos (cyan + magenta) around a SOLID near-white core. The dark contact shadow and
> 7	  the dark stroke are painted first so the halo never dissolves the glyph over bright footage — the neon is a
> 8	  rim, never the body of the letter. Emphasis tints the phrase and ignites the active word in full accent.
> 9	  Deterministic: index-driven only (t = i/FPS); no wallclock, no random, no CSS animation, no network.
> 10	  Contract: applyProps({ beats:[{t_start,t_end,phrase,emphasis}], fps, durationSec }); applyFrame(i,total).
> 11	  emphasis ∈ {hook(magenta), punch(cyan), normal(white)}. All text via textContent → XSS-safe.
> 12	-->
> 13	<!-- lang is load-bearing: it is what lets `hyphens:auto` hyphenate a long PT-BR word instead of
> 14	     snapping it mid-syllable with overflow-wrap:anywhere. -->
> 15	<html lang="pt-BR">
> 16	<head><meta charset="utf-8"><style>
> 17	  /* Self-hosted OFL font, resolved relative to this file under file:// → offline + deterministic.
> 18	     NEVER swap for a CDN/Google Fonts link: it fails silently here and the text falls back. */
> 19	  @font-face{ font-family:'Montserrat'; src:url('fonts/Montserrat-variable.ttf') format('truetype');
> 20	    font-weight:100 900; font-style:normal; font-display:block; }
> 21	
> 22	  /* Transparent root is MANDATORY — any opaque background here becomes a solid rectangle that erases the video. */
> 23	  html,body{ margin:0; padding:0; width:1080px; height:1920px; background:transparent; overflow:hidden; }
> 24	
> 25	  /* Lower-third stage inside the hard safe area (y 1075..1575 ⊂ [230,1651]). */
> 26	  #stage{ position:absolute; left:0; right:0; top:56%; height:26%;
> 27	    display:flex; align-items:center; justify-content:center; }
> 28	
> 29	  /* 80% width → text box x ∈ [108,972]; even a ~30px halo stays inside the lateral safe area [76,1004]. */
> 30	  #beat{ position:relative; width:80%; text-align:center;
> 31	    font-family:'Montserrat','Liberation Sans',system-ui,sans-serif;
> 32	    font-weight:900; text-transform:uppercase; font-size:92px; line-height:1.12; letter-spacing:1px;
> 33	    overflow-wrap:anywhere; hyphens:auto; color:#FFFFFF;
> 34	    /* Outline painted BEHIND the fill so a thick stroke never eats the glyph at sharp joints (broken-accent artifact). */
> 35	    -webkit-text-stroke:2.5px rgba(3,5,12,0.95); paint-order:stroke fill; }
> 36	
> 37	  /* Local scrim — behind the text only. Opacity is driven per-frame; it must never cover the whole canvas. */
> 38	  /* Wide + long falloff so it reads as a soft darkening of the footage, not as a discrete gray blob
> 39	     sitting on top of it. Lower peak alpha; the dark stroke does the heavy lifting for legibility. */
> 40	  #scrim{ position:absolute; left:-10%; right:-10%; top:-20%; bottom:-22%; z-index:-1; opacity:0;
> 41	    background:radial-gradient(ellipse at center,
> 42	      rgba(4,5,12,0.52) 0%, rgba(4,5,12,0.34) 42%, rgba(4,5,12,0.14) 68%, rgba(4,5,12,0) 88%);
> 43	    filter:blur(22px); }
> 44	
> 45	  /* ── Neon stacks ───────────────────────────────────────────────────────────
> 46	     Shadow order matters: the FIRST entry paints closest to the glyph. Tight dark contact shadows go first
> 47	     (they hold the core solid over bright footage), colored halos widen out behind them. */
> 48	  /* The spans are inline-block with NO whitespace text node between them, so this margin IS the word gap.
> 49	     At weight 900 uppercase a small gap makes the line read as one run-on word — keep it generous. */
> 50	  #beat .w{ display:inline-block; margin:0 0.28em 0.05em 0; overflow-wrap:anywhere;
> 51	    opacity:0; transform:translateY(24px) scale(0.72); will-change:transform,opacity;
> 52	    text-shadow:
> 53	      0 0 3px rgba(3,5,12,0.95),
> 54	      0 4px 0 rgba(3,5,12,0.55),
> 55	      0 0 16px rgba(3,5,12,0.85),
> 56	      0 0 34px rgba(34,240,255,0.20),
> 57	      0 0 66px rgba(255,61,206,0.14); }
> 58	
> 59	  /* Active ("hot") word — the neon ignites: chromatic split + wide double halo, core still near-white. */
> 60	  #beat .w.hot{ color:#F2FEFF;
> 61	    text-shadow:
> 62	      0 0 3px rgba(3,5,12,0.95),
> 63	      0 4px 0 rgba(3,5,12,0.55),
> 64	      0 0 14px rgba(3,5,12,0.88),
> 65	      -3px 0 16px rgba(255,61,206,0.55),
> 66	      3px 0 16px rgba(34,240,255,0.55),
> 67	      0 0 40px rgba(34,240,255,0.60),
> 68	      0 0 78px rgba(255,61,206,0.42),
> 69	      0 0 120px rgba(34,240,255,0.26); }
> 70	
> 71	  /* hook → magenta neon */
> 72	  #beat.hook .w{ color:#FFE7F8;
> 73	    text-shadow:
> 74	      0 0 3px rgba(12,2,10,0.95),
> 75	      0 4px 0 rgba(12,2,10,0.55),
> 76	      0 0 16px rgba(12,2,10,0.85),
> 77	      0 0 36px rgba(255,61,206,0.26),
> 78	      0 0 70px rgba(255,61,206,0.16); }
> 79	  #beat.hook .w.hot{ color:#FF66DC;
> 80	    text-shadow:
> 81	      0 0 3px rgba(12,2,10,0.95),
> 82	      0 4px 0 rgba(12,2,10,0.60),
> 83	      0 0 14px rgba(12,2,10,0.90),
> 84	      -3px 0 16px rgba(255,61,206,0.60),
> 85	      3px 0 16px rgba(140,80,255,0.45),
> 86	      0 0 42px rgba(255,61,206,0.70),
> 87	      0 0 84px rgba(255,61,206,0.46),
> 88	      0 0 128px rgba(180,60,255,0.28); }
> 89	
> 90	  /* punch → cyan neon */
> 91	  #beat.punch .w{ color:#E4FDFF;
> 92	    text-shadow:
> 93	      0 0 3px rgba(0,10,14,0.95),
> 94	      0 4px 0 rgba(0,10,14,0.55),
> 95	      0 0 16px rgba(0,10,14,0.85),
> 96	      0 0 36px rgba(34,240,255,0.28),
> 97	      0 0 70px rgba(34,240,255,0.16); }
> 98	  #beat.punch .w.hot{ color:#4DF3FF;
> 99	    text-shadow:
> 100	      0 0 3px rgba(0,10,14,0.95),
> 101	      0 4px 0 rgba(0,10,14,0.60),
> 102	      0 0 14px rgba(0,10,14,0.90),
> 103	      -3px 0 16px rgba(34,240,255,0.60),
> 104	      3px 0 16px rgba(120,120,255,0.40),
> 105	      0 0 42px rgba(34,240,255,0.72),
> 106	      0 0 84px rgba(34,240,255,0.46),
> 107	      0 0 128px rgba(90,140,255,0.26); }
> 108	
> 109	  /* Neon tube underline — anchored to the TEXT BLOCK (child of #beat), never to the stage. */
> 110	  #tube{ position:absolute; left:50%; bottom:-40px; transform:translateX(-50%);
> 111	    height:9px; width:0; border-radius:9px; opacity:0;
> 112	    background:linear-gradient(90deg,#FF3DCE 0%,#B76BFF 50%,#22F0FF 100%);
> 113	    box-shadow:0 0 12px rgba(34,240,255,0.75), 0 0 30px rgba(255,61,206,0.55), 0 0 60px rgba(34,240,255,0.30); }
> 114	</style></head>
> 115	<body>
> 116	  <div id="stage">
> 117	    <div id="beat">
> 118	      <div id="scrim"></div>
> 119	      <div id="tube"></div>
> 120	    </div>
> 121	  </div>
> 122	<script>
> 123	// ── Pure helpers (no randomness, no clock) ─────────────────────────────────
> 124	function clamp(t){ return t < 0 ? 0 : t > 1 ? 1 : t; }
> 125	function easeOut(t){ t = clamp(t); return 1 - Math.pow(1 - t, 3); }
> 126	
> 127	var BEATS = [], FPS = 30, DUR = 6, CUR = -1;
> 128	
> 129	var MAX_FONT = 92;      // starting size
> 130	var MIN_FONT = 44;      // hard floor from the typography contract
> 131	var FONT_STEP = 2;
> 132	var MAX_TEXT_H = 452;   // px of text allowed inside the 500px stage (leaves room for the tube ornament)
> 133	
> 134	// ── Props (textContent ONLY → XSS-safe; every field coerced + validated) ───
> 135	window.applyProps = function (p) {
> 136	  p = p || {};
> 137	  FPS = Math.max(1, Math.min(60, Number(p.fps) || 30));
> 138	  DUR = Math.max(0.1, Number(p.durationSec) || 6);
> 139	  BEATS = Array.isArray(p.beats) ? p.beats.map(function (b) {
> 140	    b = b || {};
> 141	    return { t0: Number(b.t_start) || 0, t1: Number(b.t_end) || 0,
> 142	             phrase: String(b.phrase || ''), emphasis: String(b.emphasis || 'normal') };
> 143	    // Trim before the length test: a whitespace-only phrase ('   ') has length but yields ZERO word
> 144	    // spans, and a beat with no spans used to throw in applyFrame — which aborts the whole clip.
> 145	  }).filter(function (b) { return b.t1 > b.t0 && b.phrase.replace(/\s+/g, '').length; }) : [];
> 146	  CUR = -1;
> 147	  buildBeat(-1);
> 148	};
> 149	
> 150	// Write a word list into the beat element as spans (createTextNode → never innerHTML).
> 151	function setWords(beatEl, words, ellipsis) {
> 152	  var spans = beatEl.getElementsByClassName('w');
> 153	  while (spans.length) beatEl.removeChild(spans[0]);
> 154	  for (var i = 0; i < words.length; i++) {
> 155	    var s = document.createElement('span');
> 156	    s.className = 'w';
> 157	    var txt = words[i];
> 158	    if (ellipsis && i === words.length - 1) txt = txt + '…';
> 159	    s.appendChild(document.createTextNode(txt));
> 160	    beatEl.appendChild(s);
> 161	  }
> 162	}
> 163	
> 164	function overflows(beatEl) { return beatEl.scrollHeight > MAX_TEXT_H; }
> 165	
> 166	// Auto-fit: shrink to the floor, then truncate by whole words with a VISIBLE ellipsis.
> 167	// Truncation is the only mutilation allowed (verbatim rule) and it announces itself.
> 168	function fitBeat(beatEl, words) {
> 169	  var size = MAX_FONT;
> 170	  beatEl.style.fontSize = size + 'px';
> 171	  setWords(beatEl, words, false);
> 172	  while (size > MIN_FONT && overflows(beatEl)) {
> 173	    size -= FONT_STEP;
> 174	    beatEl.style.fontSize = size + 'px';
> 175	  }
> 176	  if (!overflows(beatEl)) return;
> 177	  var kept = words.slice();
> 178	  while (kept.length > 1) {
> 179	    kept.pop();
> 180	    setWords(beatEl, kept, true);
> 181	    if (!overflows(beatEl)) return;
> 182	  }
> 183	}
> 184	
> 185	// Rebuild spans only when the active beat changes → span identity is stable across frames.
> 186	function buildBeat(idx) {
> 187	  var beatEl = document.getElementById('beat');
> 188	  var spans = beatEl.getElementsByClassName('w');
> 189	  while (spans.length) beatEl.removeChild(spans[0]);
> 190	  beatEl.className = '';
> 191	  if (idx < 0 || idx >= BEATS.length) { CUR = idx; return; }
> 192	  var b = BEATS[idx];
> 193	  beatEl.className = (b.emphasis === 'hook' || b.emphasis === 'punch') ? b.emphasis : '';
> 194	  var words = b.phrase.split(/\s+/).filter(function (w) { return w.length; });
> 195	  if (words.length) fitBeat(beatEl, words);
> 196	  CUR = idx;
> 197	}
> 198	
> 199	function activeBeat(t) {
> 200	  for (var i = 0; i < BEATS.length; i++) { if (t >= BEATS[i].t0 && t < BEATS[i].t1) return i; }
> 201	  return -1;
> 202	}
> 203	
> 204	// ── Deterministic per-frame render. Every visual change is written imperatively here. ──
> 205	window.applyFrame = function (i, total) {
> 206	  var t = i / FPS;
> 207	  var idx = activeBeat(t);
> 208	  if (idx !== CUR) buildBeat(idx);
> 209	
> 210	  var beatEl = document.getElementById('beat');
> 211	  var scrim = document.getElementById('scrim');
> 212	  var tube = document.getElementById('tube');
> 213	
> 214	  if (idx < 0) {
> 215	    scrim.style.opacity = '0';
> 216	    tube.style.opacity = '0';
> 217	    tube.style.width = '0';
> 218	    return;
> 219	  }
> 220	
> 221	  var b = BEATS[idx];
> 222	  var localP = clamp((t - b.t0) / (b.t1 - b.t0));
> 223	  var fin = easeOut(localP / 0.09);
> 224	  var fout = localP > 0.88 ? 1 - clamp((localP - 0.88) / 0.12) : 1;
> 225	  var env = Math.min(fin, fout);
> 226	
> 227	  scrim.style.opacity = (0.95 * env).toFixed(3);
> 228	
> 229	  var spans = beatEl.getElementsByClassName('w');
> 230	  var W = spans.length;
> 231	  // Defensive: never index past the live HTMLCollection. A beat that produced no spans must render
> 232	  // nothing rather than throw — an exception here kills the entire clip, not just this frame.
> 233	  if (!W) { tube.style.opacity = '0'; tube.style.width = '0'; return; }
> 234	
> 235	  // Which word is currently igniting: the last one already past its reveal midpoint.
> 236	  var hot = -1;
> 237	  for (var h = 0; h < W; h++) { if (localP >= (h / W) * 0.46 + 0.05) hot = h; }
> 238	
> 239	  for (var k = 0; k < W; k++) {
> 240	    var wStart = (k / W) * 0.46;
> 241	    var wt = easeOut((localP - wStart) / 0.15);
> 242	    var op = wt * env;
> 243	    // Words already read dim slightly so the hot word owns the eye.
> 244	    if (k < hot) op *= 0.82;
> 245	    var pop = (k === hot) ? 0.07 * (1 - clamp((localP - wStart) / 0.13)) : 0;
> 246	    spans[k].className = (k === hot && wt > 0.35) ? 'w hot' : 'w';
> 247	    spans[k].style.opacity = op.toFixed(3);
> 248	    spans[k].style.transform =
> 249	      'translateY(' + ((1 - wt) * 24).toFixed(2) + 'px) scale(' + (0.72 + 0.28 * wt + pop).toFixed(3) + ')';
> 250	  }
> 251	
> 252	  // Neon tube draws in under the block as the words land, retracts with the fade-out.
> 253	  var tw = easeOut((localP - 0.10) / 0.52);
> 254	  tube.style.opacity = (env * (tw > 0 ? 1 : 0)).toFixed(3);
> 255	  tube.style.width = (tw * 58 * env).toFixed(1) + '%';
> 256	};
> 257	
> 258	// Standalone-open guard: render-core always calls applyProps/applyFrame explicitly, so this is only
> 259	// so the file shows something sane when opened by hand. Never a source of state for the render.
> 260	window.applyProps({ beats: [{ t_start: 0, t_end: 3, phrase: 'A PERCEPÇÃO CONSTRÓI A DECISÃO', emphasis: 'punch' }], fps: 30, durationSec: 3 });
> 261	window.applyFrame(0, 2);
> 262	</script>
> 263	</body>
> 264	</html>
> 265	
> ```

## 🤖 Claude *(20:00:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/public/caption-previews/caption-neon-glow-9x16.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDZFBC0IgmBTRNCCIAg2RQQtCIJgU0TQgiAINkUELQiCYFNE0IIgCDbl/wfdqrvYflgdQwAAAABJRU5ErkJggg==', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(20:00:57)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/templates/motion-graphics-hero-9x16.html"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	<!DOCTYPE html>
> 2	<!--
> 3	  motion-graphics-hero-9x16 — MCORCH motion-editorial "hero card" caption style (video-repurpose FR-VR-012 family).
> 4	  A caption_style ALONGSIDE the 7 karaoke overlays (it does NOT replace them): instead of a full transcript bar it
> 5	  shows a POSTER per beat — 1 small CONTEXT kicker (weight ~500) + 1 heavy HERO (weight ~880), anchored in a chosen
> 6	  ZONE of the negative space (not a centered lower-third), premium staggered reveal (mask-up + weight-in + focus-pull,
> 7	  decelerate easing, NO bounce), mono white + a SINGLE cyan accent reserved for the climax word.
> 8	
> 9	  ARCHITECTURE (repo fact): rendered by render-core `renderAlphaFrames` (omitBackground:true) → transparent RGBA PNG
> 10	  sequence → FFmpeg overlay over the reframed footage (segment-core). Shared caption contract:
> 11	    applyProps({ beats:[{ t_start, t_end, phrase, emphasis, zone?, context?, hero? }], fps, durationSec });
> 12	    applyFrame(i, total).
> 13	  Deterministic: index-driven, NO wallclock / Date.now / Math.random / performance.now / rAF / setTimeout / network.
> 14	  Self-hosted OFL variable font under file:// (a Google Fonts / CDN url() fails SILENTLY offline → system fallback).
> 15	  Every string enters via textContent → XSS-safe (third-party transcript text is never innerHTML).
> 16	
> 17	  emphasis (per-beat, from the detector) → card intensity:
> 18	    hook  → climax HERO: cyan #22D3EE hero + architectural [ ] brackets (the one accent MEANS something)
> 19	    punch → HERO: white hero, no graphic
> 20	    normal→ quiet: white hero only (context kicker suppressed)
> 21	
> 22	  zone (from the saliency picker — the calmest region by saliency; template only ANCHORS, default 'lower-left'):
> 23	    lower-left · lower-right · upper-left · upper-right · mid-left · mid-right   (+ 'center-stack' superset)
> 24	
> 25	  GEOMETRY CONTRACT (FR-VR-016 safe-area, 1080×1920): no text pixel leaves x ∈ [76,1004], y ∈ [230,1651] at ANY
> 26	  frame, in ANY zone. Enforced, in order:
> 27	    1. #stage is a HARD px box strictly inside the safe area (never a % that drifts). Its top is nudged down enough
> 28	       that the exit lift (-16px) on an upper-anchored card still clears y=230.
> 29	    2. Per-line auto-shrink ladders (hero 184→132, context 52→34) step the font down until the line fits its box.
> 30	    3. At the floor, geometry wins over one-line: the line WRAPS (overflow-wrap:anywhere) — a multi-word hero breaks
> 31	       between words, a single token wider than the box breaks inside itself. Nothing is ever clipped in silence.
> 32	  Silently losing a glyph is a caption engine's original sin: a wrap tells the truth, a clip lies.
> 33	-->
> 34	<html lang="pt-BR">
> 35	<head><meta charset="utf-8"><style>
> 36	  /* Self-hosted OFL variable font. The worker loads via file:// so this relative url() resolves next to the
> 37	     template. NEVER a network font here — under file:// it fails SILENTLY to a system fallback. */
> 38	  @font-face{ font-family:'Montserrat'; src:url('fonts/Montserrat-variable.ttf') format('truetype');
> 39	    font-weight:100 900; font-style:normal; font-display:block; }
> 40	
> 41	  html,body{ margin:0; padding:0; width:1080px; height:1920px; background:transparent; overflow:hidden; }
> 42	
> 43	  :root{ --ink:#FFFFFF; --accent:#22D3EE; }
> 44	
> 45	  /* HARD px box inside the safe area. left 88 (≥76) and right→88+900=988 (margin 92 ≥76) clear the lateral bound;
> 46	     top 248 + height 1348 = bottom 1596 (<1651). The 248 top leaves 18px of headroom above the 230 line so the
> 47	     -16px exit lift on an upper-anchored card still lands at y=232 ≥ 230. The card is anchored by zone INSIDE it. */
> 48	  #stage{ position:absolute; left:88px; top:248px; width:900px; height:1348px;
> 49	    display:flex; }
> 50	
> 51	  /* Zones: justify-content = horizontal, align-items = vertical (flex row). text-align rides along for wraps. */
> 52	  #stage.lower-left  { justify-content:flex-start; align-items:flex-end;    }
> 53	  #stage.lower-right { justify-content:flex-end;   align-items:flex-end;    }
> 54	  #stage.upper-left  { justify-content:flex-start; align-items:flex-start;  }
> 55	  #stage.upper-right { justify-content:flex-end;   align-items:flex-start;  }
> 56	  #stage.mid-left    { justify-content:flex-start; align-items:center;      }
> 57	  #stage.mid-right   { justify-content:flex-end;   align-items:center;      }
> 58	  #stage.center-stack{ justify-content:center;     align-items:center;      }
> 59	
> 60	  #card{ position:relative; display:flex; flex-direction:column; max-width:900px;
> 61	    font-family:'Montserrat','Liberation Sans',system-ui,sans-serif;
> 62	    align-items:flex-start; }               /* flush-left default; JS mirrors it for the -right zones */
> 63	  #stage.lower-right #card, #stage.upper-right #card, #stage.mid-right #card{ align-items:flex-end; text-align:right; }
> 64	  #stage.center-stack #card{ align-items:center; text-align:center; }
> 65	
> 66	  /* Soft dark scrim ONLY behind the card → sound-off legibility over bright footage (stays local; the rest is
> 67	     transparent). Sized imperatively per beat so it hugs the card in whatever zone it landed. */
> 68	  #scrim{ position:absolute; left:0; top:0; width:0; height:0; border-radius:60px;
> 69	    background:radial-gradient(ellipse at center, rgba(6,8,12,0.72) 0%, rgba(6,8,12,0.40) 52%, rgba(6,8,12,0) 78%);
> 70	    filter:blur(14px); opacity:0; z-index:0; pointer-events:none; }
> 71	
> 72	  #card > .context, #card > .hero-wrap{ position:relative; z-index:1; }
> 73	
> 74	  /* CONTEXT: small kicker, weight 500, open tracking (editorial "kicker" read). Mask-up reveal.
> 75	     overflow-wrap:anywhere is inert under white-space:nowrap and only bites when the fit falls back to wrap. */
> 76	  .context{ overflow:hidden; margin:0 0 22px 2px; max-width:900px; }
> 77	  .ctx-ink{ display:inline-block;
> 78	    font-size:52px; font-weight:500; font-variation-settings:'wght' 500;
> 79	    text-transform:uppercase; letter-spacing:0.17em; line-height:1.05;
> 80	    color:var(--ink); opacity:0.90; white-space:nowrap;
> 81	    overflow-wrap:anywhere; word-break:normal;
> 82	    /* paint-order stroke→fill: draw the outline BEHIND the fill so a thick stroke never eats the glyph at sharp
> 83	       joints — the notch/broken-accent artifact that mutilates Ã/Ç/É/Ê. Load-bearing for pt-BR. */
> 84	    -webkit-text-stroke:1.1px rgba(6,8,12,0.85); paint-order:stroke fill;
> 85	    text-shadow:0 2px 0 rgba(6,8,12,0.5), 0 0 18px rgba(6,8,12,0.7);
> 86	    transform:translateY(100%); }
> 87	
> 88	  /* HERO: big heavy word(s). .hero-line is the MASK (overflow hidden); .hero-ink rises from underneath. */
> 89	  /* gap 16 (mirrored by BRACKET_GAP in JS) keeps the [ ] hug tight inside a narrow zone cell (DEFECT 1). */
> 90	  .hero-wrap{ display:flex; align-items:stretch; gap:16px; max-width:900px; }
> 91	  .hero-line{ overflow:hidden; }
> 92	  .hero-ink{ display:inline-block;
> 93	    font-size:184px; font-variation-settings:'wght' 880; font-weight:880;
> 94	    text-transform:uppercase; letter-spacing:-0.015em; line-height:0.98;
> 95	    color:var(--ink); white-space:nowrap;
> 96	    overflow-wrap:anywhere; word-break:normal;
> 97	    -webkit-text-stroke:2px rgba(6,8,12,0.92); paint-order:stroke fill;
> 98	    text-shadow:0 4px 0 rgba(6,8,12,0.55), 0 0 30px rgba(6,8,12,0.7), 0 10px 44px rgba(6,8,12,0.55);
> 99	    transform:translateY(108%); will-change:transform,font-variation-settings,filter; }
> 100	  /* hook → the hero takes the ACCENT (the only non-white color in the system). */
> 101	  #card.hook .hero-ink{ color:var(--accent);
> 102	    -webkit-text-stroke-color:rgba(0,26,32,0.9);
> 103	    text-shadow:0 4px 0 rgba(0,20,26,0.55), 0 0 40px rgba(34,211,238,0.45), 0 10px 44px rgba(6,8,12,0.55); }
> 104	
> 105	  /* Architectural [ ] brackets (CSS borders, not glyphs) — hook ONLY. They scale up vertically after the hero lands.
> 106	     align-self:stretch → a bracket ALWAYS spans the hero-line's full height, so on a wrapped 2-line hero the pair
> 107	     ENVELOPS the whole block instead of splitting (DEFECT 2). flex-basis 18 mirrored by BRACKET_W in JS. */
> 108	  .bracket{ flex:0 0 18px; align-self:stretch; margin:6px 0 14px;
> 109	    transform:scaleY(0.25); transform-origin:center; opacity:0;
> 110	    box-shadow:0 0 22px rgba(34,211,238,0.35); }
> 111	  .bracket.bl{ border-left:7px solid var(--accent); border-top:7px solid var(--accent); border-bottom:7px solid var(--accent); }
> 112	  .bracket.br{ border-right:7px solid var(--accent); border-top:7px solid var(--accent); border-bottom:7px solid var(--accent); }
> 113	</style></head>
> 114	<body>
> 115	  <div id="stage">
> 116	    <div id="scrim"></div>
> 117	    <div id="card"></div>
> 118	  </div>
> 119	<script>
> 120	function clamp(t){ return t<0?0:t>1?1:t; }
> 121	function easeOutQuint(t){ t=clamp(t); return 1-Math.pow(1-t,5); }
> 122	function easeInCubic(t){ t=clamp(t); return t*t*t; }
> 123	
> 124	var BEATS=[], FPS=30, DUR=6, CUR=-1;
> 125	
> 126	// Auto-shrink ladders. First entry = design size; last = the FLOOR. The HERO ladder now runs deeper (down to 84)
> 127	// so a long word shrinks into BALANCED wrapped lines inside a NARROW zone cell instead of clipping or orphaning a
> 128	// glyph (see fitHero). The CONTEXT ladder is unchanged — a single kicker line, wrapping at its floor via fitInk.
> 129	var HERO_LADDER=[184,168,152,140,132,120,108,100,96,92,88,84];
> 130	var CTX_LADDER=[52,46,40,34];
> 131	
> 132	// ── Zone-cell geometry (DEFECT 1: card must stay on its own side of the frame, off the subject) ────────────────
> 133	// The safe box is x∈[SAFE_L,SAFE_R]. A LEFT-anchored card must never let its hero cross the frame centre toward
> 134	// the subject; a RIGHT-anchored one must never cross back. So the hero/context are fitted to their ZONE CELL — the
> 135	// half of the frame on the card's side, held CENTER_GUTTER off centre — NOT to the full 900px safe box. A left cell
> 136	// is [88 .. 512] (~0.37 of the frame width). center-stack keeps the full safe box (it has no subject side).
> 137	var SAFE_L=88, SAFE_R=988, FRAME_CENTER=540, CENTER_GUTTER=28;
> 138	// Bracket budget the hook's [ ] consumes (2 borders + 2 flex gaps). MUST mirror .bracket flex-basis + .hero-wrap gap.
> 139	var BRACKET_W=18, BRACKET_GAP=16;
> 140	// A single line is kept intact only down to this floor. Below it a BRACKETED (hook) hero WRAPS — its brackets
> 141	// envelop the block so the wrap reads as one unit; a bare hero (punch/normal) stays single-line longer (a mid-word
> 142	// break with no brackets to bind it is ambiguous), wrapping only when it cannot fit even this small size. The hook
> 143	// floor sits BELOW a 5-letter word's single-line size in the narrowest zone cell, so a short hook (SORTE) stays on
> 144	// one line in EVERY zone — a rung-boundary flip must never wrap it in one zone and keep it whole in another.
> 145	var HERO_SINGLE_FLOOR_HOOK=88, HERO_SINGLE_FLOOR_PLAIN=80;
> 146	// Invisible break opportunity (U+200B). A single over-long token is split at BALANCED offsets joined by ZWSP; under
> 147	// word-break:keep-all the browser breaks ONLY there → balanced lines, never an orphan glyph, no visible mark.
> 148	var ZWSP='​';
> 149	
> 150	// Card cell width for a zone: the on-side half held CENTER_GUTTER off the frame centre (center-stack = full box).
> 151	function zoneCellWidth(zone){
> 152	  if(zone==='center-stack') return SAFE_R-SAFE_L;
> 153	  if(/-right$/.test(zone))  return SAFE_R-(FRAME_CENTER+CENTER_GUTTER);   // right-anchored → [568 .. 988]
> 154	  return (FRAME_CENTER-CENTER_GUTTER)-SAFE_L;                             // left-anchored → [88 .. 512]  (default)
> 155	}
> 156	
> 157	// zone allowlist: the 6 the saliency picker emits, plus 'center-stack' as an honored superset. Unknown → default.
> 158	var ZONES={ 'lower-left':1,'lower-right':1,'upper-left':1,'upper-right':1,'mid-left':1,'mid-right':1,'center-stack':1 };
> 159	
> 160	// pt-BR stopwords to derive the hero when a beat brings no explicit context/hero (grammar §1.3).
> 161	var STOP_PTBR={a:1,o:1,os:1,as:1,um:1,uma:1,de:1,do:1,da:1,dos:1,das:1,e:1,ou:1,que:1,'é':1,em:1,no:1,na:1,por:1,'com':1,se:1,ao:1,'à':1};
> 162	
> 163	function el(id){ return document.getElementById(id); }
> 164	
> 165	// Derive {context, hero} from a phrase: hero = last CONTENT word; context = up to 3 words before it. Honest
> 166	// heuristic (§1.3): nails a terminal pt-BR punchline, misses a non-terminal payload — the superset authors the index.
> 167	function splitPhrase(phrase){
> 168	  var toks=String(phrase||'').split(/\s+/).filter(function(w){return w.length;});
> 169	  if(!toks.length) return { context:'', hero:'' };
> 170	  var heroIdx=-1;
> 171	  for(var i=toks.length-1;i>=0;i--){ if(!STOP_PTBR[toks[i].toLowerCase()]){ heroIdx=i; break; } }
> 172	  if(heroIdx<0) heroIdx=toks.length-1;
> 173	  var ctx=toks.slice(Math.max(0,heroIdx-3), heroIdx).join(' ');
> 174	  return { context:ctx, hero:toks[heroIdx] };
> 175	}
> 176	
> 177	// Fit one inline-block line into `availW`: step down `ladder` until it fits on ONE line (white-space:nowrap →
> 178	// offsetWidth is the true content width, so the measurement is honest). If the floor is reached and it still
> 179	// overflows, switch to WRAP (white-space:normal + maxWidth) so a multi-word line breaks between words and a
> 180	// single over-wide token breaks inside itself (overflow-wrap:anywhere). Geometry wins over one-line, but nothing
> 181	// is ever clipped in silence. Returns the chosen size (for callers that care).
> 182	function fitInk(inkEl, availW, ladder){
> 183	  inkEl.style.whiteSpace='nowrap'; inkEl.style.maxWidth='none';
> 184	  var size=ladder[ladder.length-1];
> 185	  for(var s=0;s<ladder.length;s++){
> 186	    size=ladder[s]; inkEl.style.fontSize=size+'px';
> 187	    if(inkEl.offsetWidth<=availW) return size;      // fits on one line → done
> 188	  }
> 189	  inkEl.style.whiteSpace='normal'; inkEl.style.maxWidth=availW+'px'; inkEl.style.fontSize=size+'px';
> 190	  return size;                                       // floor: wrapped within the safe box
> 191	}
> 192	
> 193	// Balanced char-split of a single token into `parts` chunks. Earlier chunks are never SHORTER than later ones, so
> 194	// the last line can never be an orphan glyph (e.g. 'INEVITÁVEL'→['INEVI','TÁVEL'], 'DECISÃO'→['DECI','SÃO']).
> 195	function balancedSplit(word, parts){
> 196	  var n=word.length, base=Math.floor(n/parts), rem=n%parts, out=[], i=0;
> 197	  for(var k=0;k<parts;k++){ var len=base+(k<rem?1:0); out.push(word.slice(i,i+len)); i+=len; }
> 198	  return out;
> 199	}
> 200	
> 201	// Fit the HERO into its zone cell (DEFECT 2). Priority, in order:
> 202	//   1. ONE intact line — the largest ladder rung that fits availW, down to `singleFloor` (SORTE, FOCO stay whole).
> 203	//   2. Else WRAP into the fewest BALANCED lines (2, then 3) at the LARGEST size whose chunks each fit availW. A
> 204	//      multi-word hero breaks at its own spaces; a single token breaks at ZWSP hints under word-break:keep-all, so
> 205	//      lines are balanced, no glyph is orphaned, and the [ ] brackets envelop the whole block (they never split).
> 206	//   3. Last resort — a token too wide even split three ways: overflow-wrap:anywhere at the floor. Geometry wins,
> 207	//      nothing is clipped in silence, and it STILL never overflows the cell (never crosses into the subject).
> 208	function fitHero(inkEl, availW, singleFloor){
> 209	  var word=inkEl.textContent, L=HERO_LADDER;
> 210	  // Phase 1 — intact single line (largest fitting rung ≥ singleFloor).
> 211	  inkEl.style.whiteSpace='nowrap'; inkEl.style.wordBreak='normal'; inkEl.style.overflowWrap='normal'; inkEl.style.maxWidth='none';
> 212	  for(var s=0;s<L.length;s++){
> 213	    if(L[s]<singleFloor) break;
> 214	    inkEl.style.fontSize=L[s]+'px';
> 215	    if(inkEl.offsetWidth<=availW) return;             // whole word on one line → done
> 216	  }
> 217	  // Phase 2 — balanced wrap. Fewest lines first; within a line count, largest size that fits every chunk.
> 218	  var multiWord=/\s/.test(word);
> 219	  for(var parts=2; parts<=3; parts++){
> 220	    inkEl.textContent = multiWord ? word : balancedSplit(word, parts).join(ZWSP);
> 221	    inkEl.style.whiteSpace='normal'; inkEl.style.maxWidth=availW+'px';
> 222	    inkEl.style.wordBreak='keep-all'; inkEl.style.overflowWrap='normal';   // break ONLY at spaces / ZWSP
> 223	    for(var s2=0;s2<L.length;s2++){
> 224	      inkEl.style.fontSize=L[s2]+'px';
> 225	      if(inkEl.scrollWidth<=availW+1) return;         // no chunk overflows at this (largest passing) size
> 226	    }
> 227	  }
> 228	  // Phase 3 — honest fallback: allow an in-token break at the floor (never clip, never exceed the cell).
> 229	  inkEl.textContent=word;
> 230	  inkEl.style.fontSize=L[L.length-1]+'px';
> 231	  inkEl.style.whiteSpace='normal'; inkEl.style.maxWidth=availW+'px'; inkEl.style.wordBreak='normal'; inkEl.style.overflowWrap='anywhere';
> 232	}
> 233	
> 234	// ── Props (textContent ONLY → XSS-safe) ──────────────────────────────────
> 235	window.applyProps=function(p){
> 236	  p=p||{};
> 237	  FPS=Math.max(1,Math.min(60, Number(p.fps)||30));
> 238	  DUR=Math.max(0.1, Number(p.durationSec)||6);
> 239	  BEATS=Array.isArray(p.beats)?p.beats.map(function(b){
> 240	    b=b||{};
> 241	    var emph=String(b.emphasis||'normal');
> 242	    // explicit context/hero (superset) OR derived from the phrase.
> 243	    var ctx=(b.context!=null)?String(b.context):'';
> 244	    var hero=(b.hero!=null)?String(b.hero):'';
> 245	    if(!hero){ var s=splitPhrase(b.phrase); ctx=(b.context!=null)?ctx:s.context; hero=s.hero; }
> 246	    if(emph==='normal') ctx='';                       // quiet line: context suppressed (preserve proto semantics)
> 247	    var zone=ZONES[String(b.zone||'')]?String(b.zone):'lower-left';
> 248	    return { t0:Number(b.t_start)||0, t1:Number(b.t_end)||0, emphasis:emph, zone:zone, context:ctx, hero:hero };
> 249	  }).filter(function(b){ return b.t1>b.t0 && b.hero.length; }) : [];
> 250	  CUR=-1;
> 251	  buildBeat(-1);
> 252	};
> 253	
> 254	// Rebuild the card only when the active beat changes → stable spans across frames (fit runs 1×/beat).
> 255	function buildBeat(idx){
> 256	  var stage=el('stage'), card=el('card'), scrim=el('scrim');
> 257	  card.textContent=''; card.className=''; stage.className='';
> 258	  CUR=idx;
> 259	  if(idx<0 || idx>=BEATS.length){ scrim.style.opacity='0'; return; }
> 260	
> 261	  var b=BEATS[idx];
> 262	  stage.className=b.zone;
> 263	  card.className=(b.emphasis==='hook'||b.emphasis==='punch')?b.emphasis:'';
> 264	
> 265	  // CONTEXT (mask + ink) — only when present.
> 266	  if(b.context){
> 267	    var ctxLine=document.createElement('div'); ctxLine.className='context';
> 268	    var ctxInk=document.createElement('span'); ctxInk.className='ctx-ink';
> 269	    ctxInk.appendChild(document.createTextNode(b.context));   // never innerHTML — third-party transcript
> 270	    ctxLine.appendChild(ctxInk); card.appendChild(ctxLine);
> 271	  }
> 272	
> 273	  // HERO (bracket? + mask + ink + bracket?)
> 274	  var wrap=document.createElement('div'); wrap.className='hero-wrap';
> 275	  var withBrackets=(b.emphasis==='hook');
> 276	  if(withBrackets){ var bl=document.createElement('div'); bl.className='bracket bl'; wrap.appendChild(bl); }
> 277	  var line=document.createElement('div'); line.className='hero-line';
> 278	  var ink=document.createElement('span'); ink.className='hero-ink';
> 279	  ink.appendChild(document.createTextNode(b.hero));
> 280	  line.appendChild(ink); wrap.appendChild(line);
> 281	  if(withBrackets){ var br=document.createElement('div'); br.className='bracket br'; wrap.appendChild(br); }
> 282	  card.appendChild(wrap);
> 283	
> 284	  // Fit both lines to the ZONE CELL (DEFECT 1) — not the full safe box — so a left card never crosses centre.
> 285	  // Context spans the cell; the hero also loses the bracket budget so [ HERO ] fits WITH its brackets in the cell.
> 286	  var cellW=zoneCellWidth(b.zone);
> 287	  card.style.maxWidth=cellW+'px';
> 288	  var ctxInkEl=card.querySelector('.ctx-ink');
> 289	  if(ctxInkEl) fitInk(ctxInkEl, cellW-4, CTX_LADDER);
> 290	  var bracketBudget=withBrackets?(2*BRACKET_W+2*BRACKET_GAP):0;
> 291	  fitHero(ink, cellW-bracketBudget-4, withBrackets?HERO_SINGLE_FLOOR_HOOK:HERO_SINGLE_FLOOR_PLAIN);
> 292	
> 293	  // Scrim sized to the card bounding box (hugs the text in whatever zone it landed), then clamped so even its soft
> 294	  // halo stays on the card's side of centre — it must not bleed onto the subject on the far side.
> 295	  var cr=card.getBoundingClientRect(), sr=stage.getBoundingClientRect();
> 296	  var padX=40, padTop=50, padBot=50;
> 297	  var sLeft=(cr.left-sr.left)-padX, sTop=(cr.top-sr.top)-padTop, sW=cr.width+2*padX, sH=cr.height+padTop+padBot;
> 298	  var stageCenter=FRAME_CENTER-SAFE_L;             // frame centre in stage-local px (stage starts at SAFE_L)
> 299	  if(/-left$/.test(b.zone)){ var maxR=stageCenter-8; if(sLeft+sW>maxR) sW=maxR-sLeft; }
> 300	  else if(/-right$/.test(b.zone)){ var minL=stageCenter+8; if(sLeft<minL){ sW-=(minL-sLeft); sLeft=minL; } }
> 301	  scrim.style.left=sLeft+'px';
> 302	  scrim.style.top=sTop+'px';
> 303	  scrim.style.width=Math.max(0,sW)+'px';
> 304	  scrim.style.height=sH+'px';
> 305	}
> 306	
> 307	function activeBeat(t){
> 308	  for(var i=0;i<BEATS.length;i++){ if(t>=BEATS[i].t0 && t<BEATS[i].t1) return i; }
> 309	  return -1;
> 310	}
> 311	
> 312	// ── Deterministic per-frame render (t = i/FPS). ──────────────────────────
> 313	window.applyFrame=function(i,total){
> 314	  var t=i/FPS;
> 315	  var idx=activeBeat(t);
> 316	  if(idx!==CUR) buildBeat(idx);
> 317	
> 318	  var card=el('card'), scrim=el('scrim');
> 319	  if(idx<0){ scrim.style.opacity='0'; card.style.opacity='0'; return; }
> 320	
> 321	  var b=BEATS[idx];
> 322	  var localP=clamp((t-b.t0)/(b.t1-b.t0));
> 323	
> 324	  // Exit (last 12%): the whole card lifts a touch and fades — emphasized ACCELERATE (easeIn), no mask.
> 325	  var xf=localP>0.88 ? (localP-0.88)/0.12 : 0;
> 326	  var exitY=-16*easeInCubic(xf);
> 327	  var cardOp=1-easeInCubic(xf);
> 328	  card.style.transform='translateY('+exitY.toFixed(2)+'px)';
> 329	  card.style.opacity=cardOp.toFixed(3);
> 330	  scrim.style.opacity=(0.85*cardOp).toFixed(3);
> 331	
> 332	  // CONTEXT enters first (window 0.00→0.14).
> 333	  var ctxInk=card.querySelector('.ctx-ink');
> 334	  if(ctxInk){
> 335	    var cp=easeOutQuint((localP-0.00)/0.14);
> 336	    ctxInk.style.transform='translateY('+((1-cp)*100).toFixed(2)+'%)';
> 337	    ctxInk.style.opacity=(0.90*cp).toFixed(3);
> 338	    var cLine=ctxInk.parentNode; cLine.style.overflow=(cp>=0.999)?'visible':'hidden';
> 339	  }
> 340	
> 341	  // HERO lands +200ms later (window 0.06→0.22) with WEIGHT-IN + a micro focus-pull (blur→0).
> 342	  var ink=card.querySelector('.hero-ink');
> 343	  if(ink){
> 344	    var hp=easeOutQuint((localP-0.06)/0.16);
> 345	    ink.style.transform='translateY('+((1-hp)*108).toFixed(2)+'%)';
> 346	    var wght=Math.round(300+580*hp);
> 347	    ink.style.fontVariationSettings="'wght' "+wght;
> 348	    ink.style.fontWeight=String(wght);
> 349	    ink.style.filter='blur('+((1-hp)*4).toFixed(2)+'px)';
> 350	    // tracking settle: 0.03em → -0.015em as it lands (the Black's editorial squeeze).
> 351	    ink.style.letterSpacing=((0.03-0.045*hp)).toFixed(4)+'em';
> 352	    var hLine=ink.parentNode; hLine.style.overflow=(hp>=0.999)?'visible':'hidden';
> 353	  }
> 354	
> 355	  // BRACKETS (hook only) draw AFTER the hero lands (window 0.22→0.34).
> 356	  var brs=card.getElementsByClassName('bracket');
> 357	  if(brs.length){
> 358	    var bp=easeOutQuint((localP-0.22)/0.12);
> 359	    for(var k=0;k<brs.length;k++){
> 360	      brs[k].style.transform='scaleY('+(0.25+0.75*bp).toFixed(3)+')';
> 361	      brs[k].style.opacity=bp.toFixed(3);
> 362	    }
> 363	  }
> 364	};
> 365	
> 366	// standalone-open guard (render-core always calls applyProps/applyFrame explicitly).
> 367	window.applyProps({ beats:[
> 368	  { t_start:0, t_end:3, phrase:'ISSO NÃO É SORTE', context:'ISSO NÃO É', hero:'SORTE', emphasis:'hook', zone:'lower-left' }
> 369	], fps:30, durationSec:3 });
> 370	window.applyFrame(0,2);
> 371	</script>
> 372	</body>
> 373	</html>
> 374	
> ```

## 🤖 Claude *(20:00:57)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/public/caption-previews/motion-graphics-hero-9x16.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(20:02:09)*

<details>
<summary>💭 Thinking Process</summary>

I'm examining the "Neon" caption style against the benchmark motion-graphics template to assess visual quality. The benchmark uses a floating card design with a small "LEGENDAS QUE" kicker and large cyan "PREN DEM" hero text framed by architectural brackets, positioned in the lower-left with an editorial poster aesthetic.

The Neon style, by contrast, is a centered lower-third karaoke format—white "LEGENDAS QUE" stacked above magenta "PRENDEM" with a neon gradient tube underline. Since the slug is caption-neon-glow-9x16 (not motion-graphics-hero), keep_as_is should be false, and I can propose refinements while respecting its distinct identity as a footer-style caption rather than a floating card.

Now I'm evaluating the Neon's visual polish on its own terms, looking at the preview to assess the text sizing, glow effects, and overall execution quality. The karaoke reveal style inherently flattens the hierarchy since all words are the same size, which trades sophistication for the reveal mechanic. The neon underline tube feels a bit thin and the glow could be more luminous to match the intensity of the magenta "PRENDEM" accent. So the preview was generated with the hook emphasis mode, which explains why "PRENDEM" shows up in that bright magenta (#FF66DC) while "LEGENDAS QUE" appears in the softer near-white pink. Now I'm thinking through the legibility — the glow halos are fairly subtle at low alpha, which works fine against the dark preview background, but I'm concerned about how it'll hold up over bright footage where the dark stroke and scrim will need to do more of the heavy lifting.

The safe area positioning looks solid, with the stage occupying the middle portion of the frame and the tube extending slightly below without breaking bounds. The animation logic uses staggered word reveals with easing and a tube draw-in effect, which is reasonable though not quite as polished as the benchmark's weight-in combined with focus blur and mask transitions. I could suggest more sophisticated motion, but I need to be careful not to over-propose changes that might complicate the contract.

The main gap compared to the benchmark is in the visual hierarchy — the neon treatment feels a bit flat. The scrim's alpha could be bumped from 0.52 to around 0.60 for better legibility over bright footage, though the original comment suggests the dark stroke was doing the heavy lifting, so this is a medium-risk aesthetic call. The neon tube itself is fairly thin at its current max width, so I could increase its height or glow intensity for more visual punch. On letter-spacing, the current 1px feels a bit tight for uppercase glyphs at this weight and size, so adding a touch more tracking might help readability without breaking the design intent.

Looking at the animation timing, the reveal completes in the first 9% of the beat which is quite snappy, and the word stagger spreads across 46% of the beat—both feel appropriate. The scale pop on the hot word provides the hierarchy, which is sufficient for a karaoke-style reveal. Now I'm weighing what's actually a defect versus what's just a polish gap compared to the benchmark.

The core issue is that the benchmark is an asymmetric editorial poster with dramatic scale contrast, while the Neon is a centered symmetric lower-third karaoke—fundamentally different categories. The Neon isn't trying to be the Sovereign; it's a legitimate distinct style in the caption library. My role is to evaluate its quality and suggest safe CSS and timing refinements, not restructure it into something else. So I'll score it and propose targeted improvements.

Looking at the actual defects: the typography is too flat—"LEGENDAS QUE" and "PRENDEM" are both 92px, differing only in color and glow treatment. Compared to the benchmark's dramatic 52px-to-184px scale hierarchy, this lacks visual contrast and reads as generic centered karaoke rather than a poster. The symmetric centered composition in the lower-third is also less sophisticated than the card-based approach.

The neon tube underline is too thin and subtle—it reads as a gradient bar rather than a luminous neon signature. The scrim's low radial value (0.52) creates tight safety margins on bright footage, relying heavily on dark strokes for legibility. The animation is competent with its translate and scale reveal, but it's shallow compared to the benchmark's weight-in, focus-pull blur, and mask-up choreography.

I'm identifying three low-risk CSS improvements: increasing the scrim's radial peak from 0.52 to around 0.62 with stronger blur to reinforce legibility on bright footage while keeping it soft; thickening the neon tube from 9px to 12px and amplifying its glow shadow to make it read as an actual luminous element; and introducing subtle scale emphasis on key words to add more visual pop to the animation.

For the scale emphasis, I'm considering bumping the hot word's pop constant from +0.07 to around +0.12 to give the keyword more prominence without breaking the applyFrame contract or layout constraints — this is a medium-risk change since it involves timing adjustments, but tweaking numeric constants inside the function is safe enough.

I'm also increasing letter-spacing from 1px to 2px for the uppercase weight-900 text so the glyphs breathe better and improve readability, which is low-risk since the auto-fit mechanism handles any width overflow. For the reveal timing, stretching the easing curve slightly from 0.09 to 0.12 of the beat gives a smoother, more premium entrance without slowing down the overall read.

Since this is a karaoke model with single-phrase reveals rather than a two-tier hierarchy, the hot-word pop is the main mechanism for emphasis, so I'll focus on strengthening that effect. Now I'm identifying the specific lines to modify: the scrim gradient, letter-spacing, tube height, box-shadow, the fin easing variable, and the hot-pop animation parameters.

Generating structured output...

</details>


## 🤖 Claude *(20:02:11)*

I've read the template CSS, the render logic (applyProps/applyFrame), the Neon preview PNG, and the benchmark (motion-graphics-hero HTML + PNG). Here is my assessment.

**Verdict:** The slug is `caption-neon-glow-9x16`, not the benchmark — so `keep_as_is=false`. It is a legitimately distinct "Neon karaoke" style, competent and legible, but it sits in exactly the category the Sovereign contrasted against (centered lower-third + underline = "footer karaoke"), and its typographic hierarchy is flatter than the benchmark's kicker-vs-hero poster. I propose only safe CSS/timing polish that preserves the `applyProps/applyFrame` contract, the 1080×1920 px layout, and the transparent overlay.

## 🤖 Claude *(20:02:34)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "slug": "caption-neon-glow-9x16",
  "score": 7,
  "keep_as_is": false,
  "issues": [
    "Hierarquia tipografica plana: no PNG 'LEGENDAS QUE' e 'PRENDEM' tem o MESMO corpo (92px, weight 900) \u2014 o unico diferenciador e cor/glow. O benchmark cria drama com contraste de escala (kicker 52px vs hero 184px); aqui o bloco le como karaoke centralizado, nao como poster editorial.",
    "Composicao centralizada simetrica no lower-third (stage top:56%, justify-content:center): menos sofisticada que o card ancorado assimetrico (zone lower-left) do benchmark, e ocupa o eixo central podendo cair sobre o sujeito do video.",
    "O tubo neon (underline, #tube height:9px) e fino e o box-shadow modesto; no PNG le como uma barrinha de gradiente, nao como um tubo de neon luminoso \u2014 a assinatura visual do estilo 'Neon' fica subaproveitada.",
    "Scrim de pico baixo (radial-gradient peak rgba(4,5,12,0.52) linha 42): sobre footage CLARA a legibilidade depende quase toda do -webkit-text-stroke escuro; margem de seguranca apertada em cenas de alto brilho / sound-off.",
    "Movimento raso comparado ao benchmark: reveal por translateY(24px)+scale(0.72) e competente, mas o benchmark soma weight-in (300->880) + focus-pull (blur->0) + mask-up, leitura mais premium.",
    "Reveal muito rapido: fin = easeOut(localP/0.09) resolve a entrada em ~9% do beat \u2014 em beats curtos a palavra 'estala' quase instantanea, perdendo o refinamento do stagger."
  ],
  "safe_improvements": [
    {
      "change": "caption-neon-glow-9x16.html:111-113 \u2014 engrossar o tubo neon de height:9px para ~12px e reforcar o glow no box-shadow (aumentar raios/alpha, ex.: 0 0 16px rgba(34,240,255,0.85), 0 0 40px rgba(255,61,206,0.65), 0 0 80px rgba(34,240,255,0.38)). Faz o underline ler como tubo de neon luminoso, coerente com a identidade do estilo. Nao toca layout px nem contrato.",
      "why": "O tubo e a assinatura do estilo 'Neon' e hoje aparece subdimensionado no PNG; mais luminancia eleva o polimento sem risco.",
      "risk": "low"
    },
    {
      "change": "caption-neon-glow-9x16.html:42 \u2014 elevar o pico do scrim radial de rgba(4,5,12,0.52) para ~rgba(4,5,12,0.62) mantendo a queda longa (42%/68%/88% inalterados). Reforca legibilidade sound-off sobre footage clara sem virar bloco cinza discreto.",
      "why": "Aumenta a margem de seguranca de contraste em cenas brilhantes, que hoje repousa quase toda no stroke escuro.",
      "risk": "low"
    },
    {
      "change": "caption-neon-glow-9x16.html:32 \u2014 subir letter-spacing de 1px para ~2px no #beat (uppercase weight 900). O auto-fit (fitBeat) ja reduz o corpo se estourar, entao nao ha risco de overflow no layout px.",
      "why": "Da respiro aos glyphs uppercase colados, melhorando legibilidade e refinamento tipografico.",
      "risk": "low"
    },
    {
      "change": "caption-neon-glow-9x16.html:245 e :249 \u2014 reforcar o destaque da palavra 'hot': aumentar o pop de escala de 0.07 para ~0.12 (linha 245) e ampliar a amplitude de scale do reveal (o termo 0.28*wt na linha 249 para ~0.34*wt, ajustando o valor base). Cria contraste de escala para a palavra-chave sem introduzir segundo nivel estrutural de hierarquia.",
      "why": "Compensa a hierarquia plana dando enfase visual real a palavra ignitada, aproximando do impacto do hero do benchmark, apenas mexendo em constantes numericas dentro de applyFrame.",
      "risk": "medium"
    },
    {
      "change": "caption-neon-glow-9x16.html:223 \u2014 alongar levemente a janela de entrada: fin = easeOut(localP/0.09) -> easeOut(localP/0.13), deixando o reveal e o stagger de palavras respirarem mais antes do assentamento.",
      "why": "Entrada mais suave/premium sem atrasar a leitura, alinhando o ritmo ao decelerate do benchmark; nao altera assinatura de applyFrame.",
      "risk": "low"
    }
  ]
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-21 - agent-ae1505d94321d1e7f]]
> * **Próxima Sessão**: [[2026-07-21 - agent-af9b610d3f474d05d]]
%% --- TIMELINE END --- %%
