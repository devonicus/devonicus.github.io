// Render SVGs to PNG with headless Chromium. usage: node render.mjs file.svg:out.png:size ...
const pw = await import(process.env.PW || '/opt/npm-tools/node_modules/playwright/index.js'); const chromium = pw.chromium || pw.default.chromium;
import { readFileSync } from 'fs';
const browser = await chromium.launch();
const page = await browser.newPage();
for (const job of process.argv.slice(2)) {
  const [svg, out, size] = job.split(':'); const n = +size;
  await page.setViewportSize({ width: n, height: n });
  const markup = readFileSync(svg, 'utf8').replace(/width="\d+" height="\d+"/, `width="${n}" height="${n}"`);
  await page.setContent(`<html><body style="margin:0;background:transparent">${markup}</body></html>`);
  await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: n, height: n } });
}
await browser.close();
