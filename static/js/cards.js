/**
 * cards.js — load ONCE at the bottom of the page, after all card partials.
 *
 * Replaces the per-card <script> IIFE that was previously embedded in the
 * Jinja partial. All colour math and event wiring runs in a single pass
 * over document.querySelectorAll('.card'), eliminating:
 *   • N repeated style-recalculations (getComputedStyle per card)
 *   • N individual JS parses / IIFEs
 *   • N individual mousemove listeners
 */
(function () {
  'use strict';

  /* ── Colour helpers ─────────────────────────────────────────────────── */

  function hexToRgb(hex) {
    hex = hex.trim().replace('#', '');
    if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
    hex = hex.padStart(6, '0');
    const n = parseInt(hex, 16);
    return [n >> 16 & 255, n >> 8 & 255, n & 255];
  }

  function rgbToHex(r, g, b) {
    return '#' + [r, g, b]
      .map(c => Math.round(Math.max(0, Math.min(255, c))).toString(16).padStart(2, '0'))
      .join('');
  }

  function luminance(r, g, b) {
    return [r, g, b].map(c => {
      c /= 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    }).reduce((acc, c, i) => acc + c * [0.2126, 0.7152, 0.0722][i], 0);
  }

  function ensureVisible(hex, minLum = 0.08) {
    const rgb = hexToRgb(hex);
    if (luminance(...rgb) >= minLum) return hex;
    const target = [138, 128, 112];
    let result = rgb;
    for (let t = 0.05; t <= 1; t += 0.05) {
      result = rgb.map((c, i) => c + (target[i] - c) * t);
      if (luminance(...result) >= minLum) break;
    }
    return rgbToHex(...result);
  }

  function contrastText(hex) {
    const [r, g, b] = hexToRgb(hex);
    return luminance(r, g, b) > 0.179 ? '#07090e' : '#e8dfc8';
  }

  function blendHex(hex1, hex2, t = 0.5) {
    const a = hexToRgb(hex1), b = hexToRgb(hex2);
    return rgbToHex(...a.map((c, i) => c + (b[i] - c) * t));
  }

  /* ── Tilt handler (shared, bound per card) ──────────────────────────── */

  function onMouseMove(card, e) {
    const r = card.getBoundingClientRect();
    const dx = (e.clientX - (r.left + r.width  / 2)) / (r.width  / 2);
    const dy = (e.clientY - (r.top  + r.height / 2)) / (r.height / 2);
    card.style.transform = `rotateY(${dx * 7}deg) rotateX(${-dy * 7}deg)`;
  }

  /* ── Main init — one pass over all cards ────────────────────────────── */

  const GOLD = '#d4a843';

  document.querySelectorAll('.card').forEach(card => {
    /* Read colours from data attributes — zero reflow cost vs getComputedStyle */
    const p1raw = card.dataset.p1 || '#4a6fa5';
    const p3raw = card.dataset.p3 || '#c9a84c';

    const p1vis      = ensureVisible(p1raw);
    const p3vis      = ensureVisible(p3raw);
    const blendedVis = ensureVisible(blendHex(p1raw, p3raw));

    card.querySelectorAll('.ability').forEach(ab => {
      const target = ab.dataset.target;
      const visCol  = target === 'self' ? p1vis : target === 'other' ? p3vis : blendedVis;

      const bubble = ab.querySelector('.ability-cost');
      if (bubble) {
        bubble.style.background = visCol;
        bubble.style.color = contrastText(visCol);
      }

      const badge = ab.querySelector('.target-badge');
      if (badge) {
        const badgeFill = target === 'multi' ? GOLD : visCol;
        badge.style.background  = `color-mix(in srgb, ${badgeFill} 18%, transparent)`;
        badge.style.borderColor = `color-mix(in srgb, ${badgeFill} 55%, transparent)`;
        badge.style.color       = ensureVisible(badgeFill, 0.12);
      }
    });

    /* Tilt — passive listeners avoid blocking the scroll thread */
    card.addEventListener('mousemove',  e  => onMouseMove(card, e), { passive: true });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; }, { passive: true });
  });

})();
