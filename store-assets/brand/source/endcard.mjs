// Brand-only end card for vertical clips (1080x1920 PNG with transparency).
// usage: node endcard.mjs OUT.png "<Game name>" ICON.png social|store
// social: game icon + name + "Free to play" + a search prompt; store: game icon + name + the Devonicus mark only.
// No store or platform names, no prices on the store variant (Apple and Google rules, and the owner's no-trademarks rule).
const pw = await import(process.env.PW || '/opt/npm-tools/node_modules/playwright/index.js');
const chromium = pw.chromium || pw.default.chromium;
import { readFileSync } from 'fs';
const [out, name, icon, kind] = process.argv.slice(2);
const b64 = f => readFileSync(f).toString('base64');
const font = b64(process.env.FONT || '/home/claude/brand/fredoka-700.ttf');
const mark = readFileSync(process.env.MARK || '/home/claude/brand/flat/devonicus-mark-mono-cream.svg', 'utf8')
  .replace(/width="\d+" height="\d+"/, 'width="96" height="96"');
const social = kind !== 'store';
const html = `<html><head><style>
@font-face { font-family: F; src: url(data:font/ttf;base64,${font}); }
html,body { margin:0; width:1080px; height:1920px; background:radial-gradient(ellipse 620px 760px at 50% 46%, rgba(8,16,20,.62) 0%, rgba(8,16,20,.38) 55%, rgba(8,16,20,0) 100%); font-family:F; color:#fffdf6; }
.wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; }
.icon { width:300px; height:300px; border-radius:68px; box-shadow:0 26px 60px rgba(0,0,0,.45), 0 0 0 6px rgba(255,253,246,.14); }
h1 { margin:6px 0 0; font-size:112px; line-height:1.02; text-align:center; max-width:900px; text-shadow:0 6px 24px rgba(0,0,0,.5); }
.free { font-size:62px; color:#f2b33d; text-shadow:0 4px 16px rgba(0,0,0,.5); }
.search { font-size:44px; color:#e8dfcb; opacity:.92; }
.brand { position:absolute; bottom:300px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:18px; font-size:44px; letter-spacing:.04em; opacity:.92; }
</style></head><body><div class="wrap">
<img class="icon" src="data:image/png;base64,${b64(icon)}">
<h1>${name}</h1>
${social ? `<div class="free">Free to play</div><div class="search">Search “${name}”</div>` : ''}
</div><div class="brand">${mark}<span>Devonicus</span></div></body></html>`;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.setContent(html); await page.waitForTimeout(200);
await page.screenshot({ path: out, omitBackground: true });
await browser.close();
