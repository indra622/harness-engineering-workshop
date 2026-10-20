// Browser check, render and print for the full v02 deck (42 slides).
//
// Usage (from the project root, after build_v02.py):
//   PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js \
//     node slides/src/v02/check_v02.mjs
//
// Renders every slide at 1920 x 1080 to slides/render/v02/ (git-ignored),
// prints slides/harness-engineering-workshop-v02.pdf from a non-first slide,
// and writes slides/v02-check-evidence.json. Checks:
//   - manifest and data attributes: 42 slides, 120 minutes, 25 v10 terms in
//     order, five cases, one three-minute CEO Agent slide, a ten-minute break;
//   - notes: every term and case slide carries its full v10 block;
//   - every visible text run: inside the 40 px safe margin, at least 24 px on
//     the canvas, no overlap with another run, no clipped HTML box;
//   - diagram labels: an SVG label must stay inside the box it sits in, and no
//     connector may run through a label;
//   - keyboard, buttons, notes, deep links, full screen, narrow viewports,
//     the no-JavaScript fallback, the single file opened from an empty folder,
//     console errors and network requests.

import { createRequire } from "node:module";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..", "..");
const slidesDir = path.join(root, "slides");
const file = path.join(slidesDir, "harness-engineering-workshop-v02.html");
const pdfPath = path.join(slidesDir, "harness-engineering-workshop-v02.pdf");
const outDir = path.join(slidesDir, "render", "v02");
const url = pathToFileURL(file).href;
const rel = (p) => path.relative(root, p).split(path.sep).join("/");
mkdirSync(outDir, { recursive: true });

const V10_TERMS = ["모델", "에이전트", "런타임", "하네스", "오케스트레이션", "도구", "스킬", "플러그인", "커넥터", "MCP",
  "프롬프트", "컨텍스트", "토큰", "컨텍스트 창", "메모리", "세션", "워커", "서브에이전트", "워크플로우", "자동화",
  "완료 보고", "검증", "로컬 실행", "클라우드 실행", "리모트 컨트롤"];
const problems = [];
const fail = (m) => problems.push(m);
const consoleErrors = [];
const external = [];
const watch = (p) => {
  p.on("console", (m) => { if (m.type() === "error") consoleErrors.push(m.text()); });
  p.on("pageerror", (e) => consoleErrors.push(String(e)));
  p.on("request", (r) => { if (!r.url().startsWith("file:") && !r.url().startsWith("data:")) external.push(r.url()); });
};

// v10 blocks, normalised the way the notes are compared
const plan = readFileSync(path.join(root, "docs", "plans", "slide-content-plan-v10.md"), "utf8");
const squash = (s) => s.replace(/\s+/g, "");
function v10Block(sid) {
  const m = plan.match(new RegExp(`^### S${sid}\\. [\\s\\S]*?(?=^### S\\d+\\. |^## )`, "m"));
  if (!m) return null;
  return squash(m[0].split("\n").filter((l) => !l.trim().startsWith("```"))
    .map((l) => l.replace(/\*\*/g, "").replace(/^### /, "").trim().replace(/^- /, "")).join(""));
}

const browser = await pw.chromium.launch({ headless: true, channel: "chrome" });
const evidence = { browser: `Chrome ${browser.version()} (headless)`, file: rel(file), slides: [] };
try {
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  watch(page);
  await page.goto(url + "?shot=1#s1");
  await page.waitForSelector(".slide.active");
  await page.evaluate(() => document.fonts.ready);
  evidence.nanum_gothic_available = await page.evaluate(() => document.fonts.check('40px "Nanum Gothic"', "가"));

  // ---------------------------------------------------------------- manifest
  const meta = await page.evaluate(() => {
    const man = JSON.parse(document.getElementById("deck-manifest").textContent);
    const attrs = [...document.querySelectorAll(".slide")].map((s) => ({ ...s.dataset, id: s.id }));
    const notes = [...document.querySelectorAll(".slide")].map((s) => s.querySelector(".notes")?.textContent || "");
    return { man, attrs, notes };
  });
  const items = meta.man.items;
  const m = {
    slides: items.length, minutes: items.reduce((a, b) => a + b.minutes, 0),
    terms: items.filter((i) => i.kind === "term").map((i) => i.term),
    cases: items.filter((i) => i.kind === "case").map((i) => `${i.case} (${i.minutes}분)`),
    chapters: items.filter((i) => i.kind === "chapter").length,
    break_minutes: items.filter((i) => i.kind === "break").map((i) => i.minutes),
    ceo: items.filter((i) => i.case === "CEO Agent").map((i) => ({ physical: i.physical, minutes: i.minutes })),
    layouts: [...new Set(items.filter((i) => i.kind === "term").map((i) => i.layout))],
  };
  evidence.manifest = m;
  if (m.slides !== 42 || meta.attrs.length !== 42) fail(`slide count ${m.slides}/${meta.attrs.length} != 42`);
  if (m.minutes !== 120) fail(`minutes ${m.minutes} != 120`);
  if (JSON.stringify(m.terms) !== JSON.stringify(V10_TERMS)) fail("terms do not match the 25 v10 terms in order");
  if (m.cases.length !== 5) fail(`cases: ${m.cases.length}`);
  if (m.ceo.length !== 1 || m.ceo[0].minutes !== 3) fail(`CEO Agent: ${JSON.stringify(m.ceo)}`);
  if (JSON.stringify(m.break_minutes) !== "[10]") fail(`break: ${m.break_minutes}`);
  if (m.layouts.length < 3) fail(`only ${m.layouts.length} term layout families`);
  items.forEach((it, i) => {
    const a = meta.attrs[i];
    if (Number(a.physical) !== it.physical || a.kind !== it.kind || Number(a.minutes) !== it.minutes ||
        (it.term || "") !== (a.term || "") || (it.v10 || []).join(" ") !== (a.v10 || "")) {
      fail(`slide ${i + 1}: data attributes differ from the manifest`);
    }
    const nt = squash(meta.notes[i]);
    if ([9, 23, 29, 30].includes(i + 1)) {
      const fix = nt.indexOf(squash("v02 정정 (아래 v10 원문보다 우선)"));
      const src = nt.indexOf(squash("v10 원문 S"));
      if (fix < 0 || src < 0 || fix > src) fail(`slide ${i + 1}: v02 correction must come before the v10 source block`);
    }
    if (nt.length < 80) fail(`slide ${i + 1}: notes are too short`);
    for (const sid of it.v10 || []) {
      const b = v10Block(Number(sid.slice(1)));
      if (!b || !nt.includes(b)) fail(`slide ${i + 1}: notes do not carry the full v10 block ${sid}`);
    }
  });

  // ---------------------------------------------------------------- per-slide layout
  for (let i = 0; i < items.length; i++) {
    const id = `s${i + 1}`;
    await page.evaluate((h) => { location.hash = h; }, `#${id}`);
    await page.waitForFunction((x) => document.querySelector(".slide.active")?.id === x, id);
    await page.waitForTimeout(40);
    const r = await page.evaluate(() => {
      const slide = document.querySelector(".slide.active");
      const canvas = slide.querySelector(".canvas");
      const cr = canvas.getBoundingClientRect();
      const k = cr.width / 1920;
      const box = (q) => ({ x: (q.left - cr.left) / k, y: (q.top - cr.top) / k, w: q.width / k, h: q.height / k });
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
        const fs = parseFloat(getComputedStyle(el).fontSize);
        [...range.getClientRects()].filter((q) => q.width > 0 && q.height > 0)
          .forEach((q) => runs.push({ text: n.textContent.trim().slice(0, 28), el, fs, ...box(q) }));
      }
      const out = { runs: runs.length, minFont: Math.min(...runs.map((q) => q.fs)), small: [], outside: [], overlaps: [],
        clipped: [], spills: [], crossings: [] };
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
          out.clipped.push(String(el.className || el.tagName));
        }
      });
      // diagram labels: inside their box, not crossed by a connector
      canvas.querySelectorAll("svg").forEach((svg) => {
        const shapes = [...svg.querySelectorAll("rect, polygon, path")].filter((s) => !s.closest("marker, defs"))
          .map((s) => ({ s, b: box(s.getBoundingClientRect()) })).filter((o) => o.b.w > 30 && o.b.h > 30);
        const texts = [...svg.querySelectorAll("text")].map((t) => ({ t: t.textContent.slice(0, 24), b: box(t.getBoundingClientRect()) }));
        texts.forEach((t) => {
          const cx = t.b.x + t.b.w / 2, cy = t.b.y + t.b.h / 2;
          const holders = shapes.filter((o) => cx > o.b.x && cx < o.b.x + o.b.w && cy > o.b.y && cy < o.b.y + o.b.h)
            .sort((p, q) => p.b.w * p.b.h - q.b.w * q.b.h);
          const h = holders[0];
          if (h && (t.b.x < h.b.x - 1 || t.b.x + t.b.w > h.b.x + h.b.w + 1 || t.b.y < h.b.y - 2 || t.b.y + t.b.h > h.b.y + h.b.h + 2)) {
            out.spills.push(`"${t.t}" spills out of its ${h.s.tagName}`);
          }
        });
        // a connector drawn under an opaque box does not cross the box's label
        const covers = (t, lineEl) => shapes.some((o) => {
          const f = o.s.getAttribute("fill");
          return f && f !== "none" && (lineEl.compareDocumentPosition(o.s) & Node.DOCUMENT_POSITION_FOLLOWING) &&
            t.b.x >= o.b.x - 1 && t.b.x + t.b.w <= o.b.x + o.b.w + 1 && t.b.y >= o.b.y - 2 && t.b.y + t.b.h <= o.b.y + o.b.h + 2;
        });
        const segs = [];
        svg.querySelectorAll("polyline, line").forEach((el) => {
          const ctm = el.getScreenCTM();
          let pts;
          if (el.tagName === "line") {
            pts = [[el.x1.baseVal.value, el.y1.baseVal.value], [el.x2.baseVal.value, el.y2.baseVal.value]];
          } else {
            pts = [...el.points].map((q) => [q.x, q.y]);
          }
          pts = pts.map(([x, y]) => { const q = new DOMPoint(x, y).matrixTransform(ctm); return [(q.x - cr.left) / k, (q.y - cr.top) / k]; });
          for (let j = 1; j < pts.length; j++) segs.push([pts[j - 1], pts[j], el]);
        });
        texts.forEach((t) => {
          const x0 = t.b.x + 3, x1 = t.b.x + t.b.w - 3, y0 = t.b.y + 4, y1 = t.b.y + t.b.h - 4;
          for (const [[ax, ay], [bx, by], el] of segs) {
            if (covers(t, el)) continue;
            const steps = Math.max(2, Math.ceil(Math.hypot(bx - ax, by - ay) / 4));
            let hit = false;
            for (let s = 0; s <= steps && !hit; s++) {
              const x = ax + (bx - ax) * s / steps, y = ay + (by - ay) * s / steps;
              if (x > x0 && x < x1 && y > y0 && y < y1) hit = true;
            }
            if (hit) { out.crossings.push(`connector through "${t.t}"`); break; }
          }
        });
      });
      return out;
    });
    const tag = `slide ${i + 1}`;
    r.small.forEach((x) => fail(`${tag}: font below 24px: ${x}`));
    r.outside.forEach((x) => fail(`${tag}: text outside safe area: ${x}`));
    r.overlaps.forEach((x) => fail(`${tag}: text overlap: ${x}`));
    r.clipped.forEach((x) => fail(`${tag}: clipped box: ${x}`));
    r.spills.forEach((x) => fail(`${tag}: label: ${x}`));
    r.crossings.forEach((x) => fail(`${tag}: ${x}`));
    const png = path.join(outDir, `s${String(i + 1).padStart(2, "0")}.png`);
    await page.screenshot({ path: png });
    evidence.slides.push({ physical: i + 1, kind: items[i].kind, layout: items[i].layout, text_runs: r.runs,
      min_font_px: r.minFont, png: rel(png) });
  }

  // ---------------------------------------------------------------- interactions
  const p2 = await ctx.newPage();
  watch(p2);
  await p2.goto(url + "#s1");
  await p2.waitForSelector(".slide.active");
  const at = () => p2.evaluate(() => document.querySelector(".slide.active").id);
  const ix = {};
  await p2.keyboard.press("ArrowRight"); ix.arrowRight = await at();
  await p2.keyboard.press("PageDown"); ix.pageDown = await at();
  await p2.keyboard.press("ArrowLeft"); ix.arrowLeft = await at();
  await p2.keyboard.press("End"); ix.end = await at();
  await p2.keyboard.press("Home"); ix.home = await at();
  await p2.click("#next"); ix.nextButton = await at();
  await p2.click("#prev"); ix.prevButton = await at();
  ix.prevDisabledOnFirst = await p2.evaluate(() => document.getElementById("prev").disabled);
  await p2.keyboard.press("n");
  ix.notes = await p2.evaluate(() => ({ open: !document.getElementById("notes-panel").hidden,
    chars: document.getElementById("notes-body").textContent.trim().length }));
  await p2.click("#notes-close");
  ix.notesClosed = await p2.evaluate(() => document.getElementById("notes-panel").hidden);
  await p2.keyboard.press("f");
  await p2.waitForTimeout(300);
  ix.fullscreenOn = await p2.evaluate(() => !!document.fullscreenElement);
  await p2.keyboard.press("f");
  await p2.waitForTimeout(300);
  ix.fullscreenOff = await p2.evaluate(() => !document.fullscreenElement);
  const want = { arrowRight: "s2", pageDown: "s3", arrowLeft: "s2", end: "s42", home: "s1", nextButton: "s2", prevButton: "s1" };
  for (const [kk, v] of Object.entries(want)) if (ix[kk] !== v) fail(`interaction ${kk}: ${ix[kk]}`);
  if (!ix.prevDisabledOnFirst) fail("previous button is enabled on the first slide");
  if (!ix.notes.open || ix.notes.chars < 100 || !ix.notesClosed) fail("notes did not open and close");
  if (!ix.fullscreenOn || !ix.fullscreenOff) fail(`full screen toggle: ${ix.fullscreenOn}/${ix.fullscreenOff}`);
  await p2.goto(url + "?notes=1#s31");
  await p2.waitForSelector(".slide.active");
  ix.deepLinkCeo = await p2.evaluate(() => ({ id: document.querySelector(".slide.active").id,
    notesOpen: !document.getElementById("notes-panel").hidden,
    canonical: document.getElementById("notes-body").textContent.includes("CEO Agent: 조사한 페르소나를 상황에 맞게 적용하기"),
    counter: document.getElementById("counter").textContent }));
  if (ix.deepLinkCeo.id !== "s31" || !ix.deepLinkCeo.canonical || !ix.deepLinkCeo.notesOpen || ix.deepLinkCeo.counter !== "31 / 42") {
    fail(`deep link s31: ${JSON.stringify(ix.deepLinkCeo)}`);
  }
  await p2.goto(url + "#7");
  await p2.waitForSelector(".slide.active");
  ix.deepLinkNumber = await at();
  if (ix.deepLinkNumber !== "s7") fail(`deep link #7: ${ix.deepLinkNumber}`);
  await p2.screenshot({ path: path.join(outDir, "interaction-s7.png") });
  evidence.interactions = ix;

  // ---------------------------------------------------------------- viewports
  evidence.viewports = [];
  for (const [w, h, notes] of [[1280, 720, false], [1920, 1080, true], [390, 844, false], [390, 844, true]]) {
    const c = await browser.newContext({ viewport: { width: w, height: h } });
    const pv = await c.newPage();
    watch(pv);
    await pv.goto(url + (notes ? "?notes=1" : "") + "#s21");
    await pv.waitForSelector(".slide.active");
    const fit = await pv.evaluate(() => {
      const st = document.querySelector(".slide.active .stage").getBoundingClientRect();
      const cv = document.querySelector(".slide.active .canvas").getBoundingClientRect();
      const ctl = document.querySelector(".controls").getBoundingClientRect();
      return { stageW: Math.round(st.width), fits: Math.abs(cv.width - st.width) < 1.5 && st.right <= innerWidth + 0.5 &&
        st.bottom <= innerHeight + 0.5 && document.documentElement.scrollWidth <= innerWidth,
        controlsVisible: ctl.height > 0 && ctl.bottom <= innerHeight + 0.5 };
    });
    evidence.viewports.push({ size: `${w}x${h}`, notes, ...fit });
    if (!fit.fits || !fit.controlsVisible) fail(`viewport ${w}x${h}${notes ? " with notes" : ""}: ${JSON.stringify(fit)}`);
    await pv.screenshot({ path: path.join(outDir, `viewport-${w}x${h}${notes ? "-notes" : ""}.png`) });
    await c.close();
  }

  // ---------------------------------------------------------------- no JavaScript
  const nj = await browser.newContext({ viewport: { width: 1280, height: 900 }, javaScriptEnabled: false });
  const pn = await nj.newPage();
  await pn.goto(url);
  const visibleNoJs = await pn.evaluate(() => [...document.querySelectorAll(".slide")].filter((s) => s.getBoundingClientRect().height > 100).length);
  evidence.no_javascript_visible_slides = visibleNoJs;
  if (visibleNoJs !== 42) fail(`without JavaScript only ${visibleNoJs} slides are visible`);
  await pn.screenshot({ path: path.join(outDir, "no-javascript.png") });
  await nj.close();

  // ---------------------------------------------------------------- single file from an empty folder
  const tmp = mkdtempSync(path.join(os.tmpdir(), "deck-v02-"));
  const copy = path.join(tmp, "harness-engineering-workshop-v02.html");
  copyFileSync(file, copy);
  const sc = await browser.newContext({ viewport: { width: 1600, height: 900 } });
  const ps = await sc.newPage();
  watch(ps);
  await ps.goto(pathToFileURL(copy).href + "#s14");
  await ps.waitForSelector(".slide.active");
  await ps.keyboard.press("ArrowRight");
  const solo = await ps.evaluate(() => ({ count: document.querySelectorAll(".slide").length,
    active: document.querySelector(".slide.active").id,
    styled: getComputedStyle(document.querySelector(".controls")).display === "flex",
    stageW: document.querySelector(".slide.active .stage").getBoundingClientRect().width }));
  evidence.standalone_copy = { folder: "fresh temporary folder, no other files", ...solo };
  if (solo.count !== 42 || solo.active !== "s15" || !solo.styled || solo.stageW < 800) fail(`standalone copy: ${JSON.stringify(solo)}`);
  await sc.close();

  // ---------------------------------------------------------------- print from a non-first slide
  const pp = await ctx.newPage();
  await pp.goto(url + "#s20");
  await pp.waitForSelector(".slide.active");
  const activeBeforePrint = await pp.evaluate(() => document.querySelector(".slide.active").id);
  await pp.emulateMedia({ media: "print" });
  await pp.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true });
  const raw = readFileSync(pdfPath).toString("latin1");
  const pages = (raw.match(/\/Type\s*\/Page(?![a-zA-Z])/g) || []).length;
  const box = raw.match(/\/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]/);
  const ratio = box ? Number(box[1]) / Number(box[2]) : 0;
  evidence.pdf = { file: rel(pdfPath), printed_from: activeBeforePrint, pages, media_box: box ? [Number(box[1]), Number(box[2])] : null,
    ratio: Number(ratio.toFixed(4)) };
  if (pages !== 42) fail(`PDF has ${pages} pages, expected 42`);
  if (Math.abs(ratio - 16 / 9) > 0.01) fail(`PDF page ratio ${ratio}`);
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
writeFileSync(path.join(slidesDir, "v02-check-evidence.json"), JSON.stringify(evidence, null, 2) + "\n");
problems.forEach((x) => console.log("FAIL", x));
console.log(problems.length ? `${problems.length} problem(s)` : "ok");
process.exit(problems.length ? 1 : 0);
