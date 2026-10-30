// Render the RIFTLIFE mark into the site's icon files. Run from the repo root: node source/scripts/make_icons.js
// (needs Playwright's Chromium; favicon.ico is then packed by make_icons.py)
const { chromium } = require('playwright');
const fs = require('fs');
const MARK = 'M14.3 2.4a2.4 2.4 0 0 1 3.4 0l11.9 11.9a2.4 2.4 0 0 1 0 3.4L17.7 29.6a2.4 2.4 0 0 1-3.4 0L2.4 17.7a2.4 2.4 0 0 1 0-3.4Z';
const RIFT = 'M18.6 4.5 12.4 15.2h6.1L13.2 27.5';
// small sizes get a thicker cut so the rift survives at 16px; tiles get a dark square behind the mark
const svg = (size, { fill, cut, bg, pad = 0 }) => `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="${-pad} ${-pad} ${32 + pad * 2} ${32 + pad * 2}">
  ${bg ? `<rect x="${-pad}" y="${-pad}" width="${32 + pad * 2}" height="${32 + pad * 2}" fill="${bg}"/>` : ''}
  <defs><mask id="c" maskUnits="userSpaceOnUse" x="-1" y="-1" width="34" height="34"><rect x="-1" y="-1" width="34" height="34" fill="#fff"/><path d="${RIFT}" fill="none" stroke="#000" stroke-width="${cut}" stroke-linecap="round" stroke-linejoin="round"/></mask></defs>
  <path d="${MARK}" fill="${fill}" mask="url(#c)"/></svg>`;
const jobs = [
  ['source/icons/png-16.png', 16, { fill: '#B98328', cut: 3.6 }],
  ['source/icons/png-32.png', 32, { fill: '#B98328', cut: 3.2 }],
  ['source/icons/png-48.png', 48, { fill: '#B98328', cut: 3 }],
  ['apple-touch-icon.png', 180, { fill: '#D8A84F', cut: 2.7, bg: '#0D141B', pad: 7 }],
  ['icon-192.png', 192, { fill: '#D8A84F', cut: 2.7, bg: '#0D141B', pad: 9 }],
  ['icon-512.png', 512, { fill: '#D8A84F', cut: 2.7, bg: '#0D141B', pad: 9 }],
];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 1 });
  for (const [out, size, o] of jobs) {
    await p.setViewportSize({ width: size, height: size });
    await p.setContent(`<html><body style="margin:0;background:transparent">${svg(size, o)}</body></html>`);
    await p.screenshot({ path: out, omitBackground: !o.bg, clip: { x: 0, y: 0, width: size, height: size } });
    console.log('wrote', out);
  }
  await b.close();
})();
