// Browser check and render for the v02 redesign proof (six screens).
//
// Usage (from the project root, after build_proof.py):
//   PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js \
//     node slides/src/v02/check_proof.mjs
//
// Renders each screen at exactly 1920 x 1080 to slides/previews/redesign-v02/,
// prints slides/previews/redesign-v02.pdf, and checks every visible text run:
// inside the 40 px safe margin, no font below 24 px on the canvas, no text run
// overlapping another, no clipped HTML boxes. Also checks keyboard, buttons,
// notes, deep links, console errors and network requests.

import { createRequire } from "node:module";
import { mkdirSync, writeFileSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..", "..");
const file = path.join(root, "slides", "previews", "redesign-v02.html");
const outDir = path.join(root, "slides", "previews", "redesign-v02");
const url = pathToFileURL(file).href;
const rel = (p) => path.relative(root, p).split(path.sep).join("/");
mkdirSync(outDir, { recursive: true });

const NAMES = ["P1-cover", "P2-chapter-1", "P3-term-runtime", "P4-case-omh", "P5-case-ceo", "P6-closing"];
const problems = [];
const fail = (m) => problems.push(m);
const consoleErrors = [];
const external = [];
const watch = (p) => {
  p.on("console", (m) => { if (m.type() === "error") consoleErrors.push(m.text()); });
  p.on("pageerror", (e) => consoleErrors.push(String(e)));
  p.on("request", (r) => { if (!r.url().startsWith("file:")) external.push(r.url()); });
};

const browser = await pw.chromium.launch({ headless: true, channel: "chrome" });
const evidence = { browser: `Chrome ${browser.version()} (headless)`, file: rel(file), screens: [] };
try {
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  watch(page);
  await page.goto(url + "?shot=1#P1");
  await page.waitForSelector(".slide.active");
  await page.evaluate(() => document.fonts.ready);
  const fontOk = await page.evaluate(() => {
    const c = document.createElement("canvas").getContext("2d");
    const s = "하네스 엔지니어링 런타임";
    c.font = '40px "Nanum Gothic"'; const a = c.measureText(s).width;
    c.font = "40px monospace"; const b = c.measureText(s).width;
    return a !== b;
  });
  evidence.nanum_gothic_available = fontOk;
  if (!fontOk) fail("Nanum Gothic not available in the browser");

  for (let i = 0; i < NAMES.length; i++) {
    await page.evaluate((h) => { location.hash = h; }, `#P${i + 1}`);
    await page.waitForFunction((id) => document.querySelector(".slide.active")?.id === id, `P${i + 1}`);
    await page.waitForTimeout(80);
    const r = await page.evaluate(() => {
      const slide = document.querySelector(".slide.active");
      const canvas = slide.querySelector(".canvas");
      const cr = canvas.getBoundingClientRect();
      const scale = cr.width / 1920;
      const skip = (el) => el.closest("[aria-hidden='true']");
      const runs = [];
      const walker = document.createTreeWalker(canvas, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        if (!n.textContent.trim()) continue;
        const el = n.parentElement;
        if (skip(el)) continue;
        const range = document.createRange();
        range.selectNodeContents(n);
        const rects = Array.from(range.getClientRects()).filter((q) => q.width > 0 && q.height > 0);
        const fs = parseFloat(getComputedStyle(el).fontSize);
        rects.forEach((q) => runs.push({
          text: n.textContent.trim().slice(0, 24), el, fs,
          x: (q.left - cr.left) / scale, y: (q.top - cr.top) / scale,
          w: q.width / scale, h: q.height / scale }));
      }
      const out = { runs: runs.length, minFont: Math.min(...runs.map((q) => q.fs)),
        small: [], outside: [], overlaps: [], clipped: [] };
      runs.forEach((q) => {
        if (q.fs < 24) out.small.push(`${q.text} (${q.fs}px)`);
        if (q.x < 40 || q.y < 40 || q.x + q.w > 1880 || q.y + q.h > 1040) {
          out.outside.push(`${q.text} at ${q.x.toFixed(0)},${q.y.toFixed(0)} ${q.w.toFixed(0)}x${q.h.toFixed(0)}`);
        }
      });
      for (let a = 0; a < runs.length; a++) {
        for (let b = a + 1; b < runs.length; b++) {
          const A = runs[a], B = runs[b];
          if (A.el === B.el) continue;
          const ox = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x);
          const oy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
          if (ox > 2 && oy > 4) out.overlaps.push(`"${A.text}" x "${B.text}"`);
        }
      }
      canvas.querySelectorAll("*").forEach((el) => {
        if (el instanceof SVGElement) return;
        if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== "visible") {
          out.clipped.push(el.className || el.tagName);
        }
      });
      return out;
    });
    const name = NAMES[i];
    r.small.forEach((m) => fail(`${name}: font below 24px: ${m}`));
    r.outside.forEach((m) => fail(`${name}: text outside safe area: ${m}`));
    r.overlaps.forEach((m) => fail(`${name}: text overlap: ${m}`));
    r.clipped.forEach((m) => fail(`${name}: clipped box: ${m}`));
    const png = path.join(outDir, `${name}.png`);
    await page.screenshot({ path: png });
    evidence.screens.push({ id: `P${i + 1}`, name, text_runs: r.runs, min_font_px: r.minFont, png: rel(png) });
  }

  const p2 = await ctx.newPage();
  watch(p2);
  await p2.goto(url + "#P1");
  await p2.waitForSelector(".slide.active");
  const at = () => p2.evaluate(() => document.querySelector(".slide.active").id);
  const ix = {};
  await p2.keyboard.press("ArrowRight"); ix.arrowRight = await at();
  await p2.keyboard.press("End"); ix.end = await at();
  await p2.keyboard.press("Home"); ix.home = await at();
  await p2.click("#next"); ix.next = await at();
  await p2.keyboard.press("n");
  ix.notes = await p2.evaluate(() => ({ open: !document.getElementById("notes-panel").hidden,
    chars: document.getElementById("notes-body").textContent.trim().length }));
  await p2.screenshot({ path: path.join(outDir, "interaction-notes.png") });
  const want = { arrowRight: "P2", end: "P6", home: "P1", next: "P2" };
  for (const [k, v] of Object.entries(want)) if (ix[k] !== v) fail(`interaction ${k}: ${ix[k]}`);
  if (!ix.notes.open || ix.notes.chars < 100) fail("notes did not open with content");
  await p2.goto(url + "?notes=1#P5");
  await p2.waitForSelector(".slide.active");
  ix.deepLink = await p2.evaluate(() => ({ id: document.querySelector(".slide.active").id,
    canonical: document.getElementById("notes-body").textContent.includes("CEO Agent: 조사한 페르소나를 상황에 맞게 적용하기") }));
  if (ix.deepLink.id !== "P5" || !ix.deepLink.canonical) fail(`deep link P5: ${JSON.stringify(ix.deepLink)}`);
  evidence.interactions = ix;

  for (const [w, h] of [[1280, 720], [390, 844]]) {
    const c = await browser.newContext({ viewport: { width: w, height: h } });
    const p = await c.newPage();
    watch(p);
    await p.goto(url + "#P3");
    await p.waitForSelector(".slide.active");
    const fitOk = await p.evaluate(() => {
      const st = document.querySelector(".slide.active .stage").getBoundingClientRect();
      const cv = document.querySelector(".slide.active .canvas").getBoundingClientRect();
      return Math.abs(cv.width - st.width) < 1.5 && st.right <= innerWidth + 0.5 &&
        document.documentElement.scrollWidth <= innerWidth;
    });
    if (!fitOk) fail(`viewport ${w}x${h}: canvas does not fit the stage`);
    await p.screenshot({ path: path.join(outDir, `viewport-${w}x${h}.png`) });
    await c.close();
  }

  const pp = await ctx.newPage();
  await pp.goto(url + "#P1");
  await pp.waitForSelector(".slide.active");
  await pp.emulateMedia({ media: "print" });
  const pdf = path.join(root, "slides", "previews", "redesign-v02.pdf");
  await pp.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  const raw = readFileSync(pdf).toString("latin1");
  const pages = (raw.match(/\/Type\s*\/Page(?![a-zA-Z])/g) || []).length;
  evidence.pdf = { file: rel(pdf), pages };
  if (pages !== 6) fail(`proof PDF has ${pages} pages, expected 6`);
  await ctx.close();
} finally {
  await browser.close();
}
evidence.console_errors = consoleErrors;
evidence.external_requests = external;
if (consoleErrors.length) fail(`console errors: ${consoleErrors.join(" | ")}`);
if (external.length) fail(`network requests: ${external.join(" | ")}`);
evidence.problems = problems;
evidence.passed = !problems.length;
writeFileSync(path.join(outDir, "check-evidence.json"), JSON.stringify(evidence, null, 2) + "\n");
problems.forEach((p) => console.log("FAIL", p));
console.log(problems.length ? `${problems.length} problem(s)` : "ok");
process.exit(problems.length ? 1 : 0);
