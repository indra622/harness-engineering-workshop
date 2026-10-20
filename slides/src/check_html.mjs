// Browser check for the HTML deck with real headless Chrome.
//
// Usage (from the project root, after build_html.py):
//   PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js \
//     node slides/src/check_html.mjs
//
// Uses an existing Playwright install (no download): set PLAYWRIGHT_MODULE to
// its index.js, or have `playwright` resolvable from this folder. Chrome is
// launched through Playwright's "chrome" channel.
//
// Writes slide PNGs, interaction and viewport screenshots to slides/render/
// (git-ignored), the print PDF to slides/harness-engineering-workshop.pdf, and
// slides/html-check-evidence.json. Exit code 1 if any check fails.

import { createRequire } from "node:module";
import { mkdirSync, writeFileSync, rmSync, readFileSync, copyFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..");
const slidesDir = path.join(root, "slides");
const renderDir = path.join(slidesDir, "render");
const indexUrl = pathToFileURL(path.join(slidesDir, "index.html")).href;
const rel = (p) => path.relative(root, p).split(path.sep).join("/");
const standalonePath = path.join(slidesDir, "harness-engineering-workshop-v01.html");

// count page objects in a PDF and read the first page size, without extra tools
function pdfInfo(file) {
  const raw = readFileSync(file).toString("latin1");
  const pages = (raw.match(/\/Type\s*\/Page(?![a-zA-Z])/g) || []).length;
  const box = raw.match(/\/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]/);
  return { pages, width_pt: box ? Number(box[1]) : null, height_pt: box ? Number(box[2]) : null };
}

rmSync(renderDir, { recursive: true, force: true });
mkdirSync(renderDir, { recursive: true });

const problems = [];
const fail = (msg) => problems.push(msg);
const consoleErrors = [];
const externalRequests = [];

function watch(page) {
  page.on("console", (m) => { if (m.type() === "error") consoleErrors.push(m.text()); });
  page.on("pageerror", (e) => consoleErrors.push(String(e)));
  page.on("request", (r) => { if (!r.url().startsWith("file:")) externalRequests.push(r.url()); });
}

const browser = await pw.chromium.launch({ headless: true, channel: "chrome" });
const version = browser.version();
const evidence = { browser: `Chrome ${version} (headless, Playwright chrome channel)` };

try {
  // ------------------------------------------------------------ structure and fonts
  const ctx = await browser.newContext({ viewport: { width: 1600, height: 984 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  watch(page);
  await page.goto(indexUrl + "#s1");
  await page.waitForSelector(".slide.active");
  await page.evaluate(() => document.fonts.ready);

  const fontInfo = await page.evaluate(() => {
    const c = document.createElement("canvas").getContext("2d");
    const sample = "회의 준비 컨텍스트 검증 OpenClaw";
    const w = (f) => { c.font = f; return c.measureText(sample).width; };
    return {
      nanum: w('20px "Nanum Gothic"'), monospace: w("20px monospace"), serif: w("20px serif"),
      check: document.fonts.check('20px "Nanum Gothic"'),
    };
  });
  const nanumAvailable = fontInfo.nanum !== fontInfo.monospace && fontInfo.nanum !== fontInfo.serif;
  if (!nanumAvailable) fail("Nanum Gothic not available to the browser; a fallback font was used");
  evidence.font = { family: "Nanum Gothic", available_in_browser: nanumAvailable, probe: fontInfo };

  const meta = await page.evaluate(() => Array.from(document.querySelectorAll(".slide")).map((s) => ({
    id: s.id, sid: Number(s.dataset.sid), title: s.dataset.title, canonical: s.dataset.canonicalTitle,
    minutes: Number(s.dataset.minutes),
    notesChars: (s.querySelector(".notes")?.textContent || "").trim().length,
    notesHasCanonical: (s.querySelector(".notes")?.textContent || "").includes(s.dataset.canonicalTitle),
    images: s.querySelectorAll("img, image").length,
    svgTexts: s.querySelectorAll("svg text").length,
  })));
  if (meta.length !== 35) fail(`slide count ${meta.length} != 35`);
  meta.forEach((m, i) => {
    if (m.sid !== i + 1 || m.id !== `s${i + 1}`) fail(`slide order: position ${i + 1} is ${m.id}`);
    if (!m.notesChars) fail(`${m.id}: empty notes`);
    if (!m.notesHasCanonical) fail(`${m.id}: notes lack canonical title`);
    if (m.images) fail(`${m.id}: raster image found`);
  });
  const totalMinutes = meta.reduce((a, m) => a + m.minutes, 0);
  if (totalMinutes !== 120) fail(`minutes total ${totalMinutes} != 120`);

  // ------------------------------------------------------------ every slide: geometry + screenshot
  const perSlide = [];
  for (const m of meta) {
    await page.evaluate((h) => { window.location.hash = h; }, `#s${m.sid}`);
    await page.waitForFunction((id) => document.querySelector(".slide.active")?.id === id, m.id);
    const geo = await page.evaluate(() => {
      const s = document.querySelector(".slide.active");
      const svg = s.querySelector("svg");
      const out = { overflow: [], outside: [], groups: 0 };
      const tol = 0.03;
      for (const g of svg.querySelectorAll("g.tx")) {
        out.groups++;
        const [x, y, w, h] = g.dataset.box.split(" ").map(Number);
        const [il, ir] = g.dataset.inset.split(" ").map(Number);
        const b = g.getBBox();
        if (b.width === 0) continue;
        if (b.x < x + il - tol || b.x + b.width > x + w - ir + tol ||
            b.y < y - tol || b.y + b.height > y + h + tol) {
          out.overflow.push(`${g.dataset.name}: text ${b.x.toFixed(2)},${b.y.toFixed(2)} ` +
            `${b.width.toFixed(2)}x${b.height.toFixed(2)} vs box ${x},${y} ${w}x${h}`);
        }
      }
      const all = svg.getBBox();
      if (all.x < -0.001 || all.y < -0.001 || all.x + all.width > 13.334 || all.y + all.height > 7.501) {
        out.outside.push(`content ${all.x.toFixed(2)},${all.y.toFixed(2)} ${all.width.toFixed(2)}x${all.height.toFixed(2)}`);
      }
      const st = s.querySelector(".stage").getBoundingClientRect();
      out.stage = { w: Math.round(st.width), h: Math.round(st.height) };
      out.inViewport = st.left >= 0 && st.top >= 0 && st.right <= innerWidth + 0.5 && st.bottom <= innerHeight + 0.5;
      out.counter = document.getElementById("counter").textContent;
      return out;
    });
    geo.overflow.forEach((o) => fail(`${m.id}: rendered text overflow ${o}`));
    geo.outside.forEach((o) => fail(`${m.id}: content outside slide ${o}`));
    if (!geo.inViewport) fail(`${m.id}: stage not inside viewport`);
    const file = path.join(renderDir, `s${String(m.sid).padStart(2, "0")}.png`);
    await page.locator(".slide.active .stage").screenshot({ path: file });
    perSlide.push({ id: m.id, title: m.title, canonical_title: m.canonical, minutes: m.minutes,
      text_groups: geo.groups, svg_text_elements: m.svgTexts, notes_chars: m.notesChars,
      counter: geo.counter, png: rel(file) });
  }
  evidence.slides = perSlide;

  // ------------------------------------------------------------ interactions
  const ix = {};
  const p2 = await ctx.newPage();
  watch(p2);
  await p2.goto(indexUrl + "#s1");
  await p2.waitForSelector(".slide.active");
  const active = () => p2.evaluate(() => ({ id: document.querySelector(".slide.active").id, hash: location.hash }));
  await p2.keyboard.press("ArrowRight"); ix.arrowRight = await active();
  await p2.keyboard.press("PageDown"); ix.pageDown = await active();
  await p2.keyboard.press("ArrowLeft"); ix.arrowLeft = await active();
  await p2.keyboard.press("End"); ix.end = await active();
  await p2.keyboard.press("Home"); ix.home = await active();
  await p2.click("#next"); ix.nextButton = await active();
  await p2.click("#prev"); ix.prevButton = await active();
  ix.prevDisabledAtStart = await p2.$eval("#prev", (b) => b.disabled);
  const expect = { arrowRight: "s2", pageDown: "s3", arrowLeft: "s2", end: "s35", home: "s1",
    nextButton: "s2", prevButton: "s1" };
  for (const [k, id] of Object.entries(expect)) {
    if (ix[k].id !== id || ix[k].hash !== `#${id}`) fail(`interaction ${k}: got ${ix[k].id} ${ix[k].hash}`);
  }
  if (!ix.prevDisabledAtStart) fail("prev button not disabled on first slide");

  await p2.keyboard.press("n");
  const notesOpen = await p2.evaluate(() => {
    const p = document.getElementById("notes-panel");
    return { visible: !p.hidden && p.getBoundingClientRect().width > 200,
      text: document.getElementById("notes-body").textContent.slice(0, 80),
      pressed: document.getElementById("notes-toggle").getAttribute("aria-pressed") };
  });
  ix.notesKey = notesOpen;
  if (!notesOpen.visible || notesOpen.pressed !== "true") fail("N key did not open notes");
  await p2.screenshot({ path: path.join(renderDir, "interaction-notes-open.png") });
  await p2.click("#notes-close");
  ix.notesClosed = await p2.evaluate(() => document.getElementById("notes-panel").hidden);
  if (!ix.notesClosed) fail("notes close button did not hide notes");

  const p3 = await ctx.newPage();
  watch(p3);
  await p3.goto(indexUrl + "?notes=1#s26");
  await p3.waitForSelector(".slide.active");
  ix.deepLink = await p3.evaluate(() => ({
    id: document.querySelector(".slide.active").id,
    screenTitle: document.querySelector(".slide.active").dataset.title,
    notesVisible: !document.getElementById("notes-panel").hidden,
    notesHasCanonical: document.getElementById("notes-body").textContent
      .includes(document.querySelector(".slide.active").dataset.canonicalTitle),
  }));
  if (ix.deepLink.id !== "s26" || !ix.deepLink.notesVisible || !ix.deepLink.notesHasCanonical) {
    fail(`deep link #s26 with notes failed: ${JSON.stringify(ix.deepLink)}`);
  }
  await p3.screenshot({ path: path.join(renderDir, "interaction-deeplink-s26-notes.png") });
  evidence.interactions = ix;

  // ------------------------------------------------------------ responsive viewports
  const views = [[1920, 1080], [1280, 720], [1024, 768], [390, 844]];
  evidence.viewports = [];
  for (const [w, h] of views) {
    const c = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const p = await c.newPage();
    watch(p);
    await p.goto(indexUrl + "#s11");
    await p.waitForSelector(".slide.active");
    const r = await p.evaluate(() => {
      const st = document.querySelector(".slide.active .stage").getBoundingClientRect();
      return { stageW: st.width, stageH: st.height, left: st.left, top: st.top, right: st.right,
        bottom: st.bottom, scrollW: document.documentElement.scrollWidth, innerW: innerWidth,
        innerH: innerHeight };
    });
    const ratio = r.stageW / r.stageH;
    const ok = Math.abs(ratio - 16 / 9) < 0.02 && r.left >= 0 && r.top >= 0 && r.right <= r.innerW + 0.5 &&
      r.bottom <= r.innerH + 0.5 && r.scrollW <= r.innerW;
    if (!ok) fail(`viewport ${w}x${h}: stage ${JSON.stringify(r)}`);
    const shot = path.join(renderDir, `viewport-${w}x${h}.png`);
    await p.screenshot({ path: shot });
    evidence.viewports.push({ viewport: `${w}x${h}`, stage: `${Math.round(r.stageW)}x${Math.round(r.stageH)}`,
      ratio: Number(ratio.toFixed(3)), no_horizontal_scroll: r.scrollW <= r.innerW, ok, png: rel(shot) });
    await c.close();
  }

  // ------------------------------------------------------------ no-JavaScript fallback
  const nojs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 800 } });
  const pn = await nojs.newPage();
  await pn.goto(indexUrl);
  const visibleNoJs = await pn.evaluate(() =>
    Array.from(document.querySelectorAll(".slide")).filter((s) => s.getBoundingClientRect().height > 0).length);
  evidence.no_javascript_visible_slides = visibleNoJs;
  if (visibleNoJs !== 35) fail(`without JavaScript only ${visibleNoJs} slides are visible`);
  await nojs.close();

  // ------------------------------------------------------------ print to PDF
  const pp = await ctx.newPage();
  await pp.goto(indexUrl + "#s1");
  await pp.waitForSelector(".slide.active");
  await pp.emulateMedia({ media: "print" });
  const pdfPath = path.join(slidesDir, "harness-engineering-workshop-v01.pdf");
  await pp.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true });
  const pinfo = pdfInfo(pdfPath);
  evidence.print_pdf = { file: rel(pdfPath), ...pinfo };
  if (pinfo.pages !== 35) fail(`print PDF has ${pinfo.pages} pages, expected 35`);
  if (pinfo.width_pt && Math.abs(pinfo.width_pt / pinfo.height_pt - 16 / 9) > 0.01) {
    fail(`print page is not 16:9: ${pinfo.width_pt}x${pinfo.height_pt}`);
  }

  // ------------------------------------------------------------ standalone single file
  const soloDir = path.join(renderDir, "standalone-alone");
  mkdirSync(soloDir, { recursive: true });
  const soloFile = path.join(soloDir, path.basename(standalonePath));
  copyFileSync(standalonePath, soloFile);          // no assets folder next to it
  const sctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const sp = await sctx.newPage();
  watch(sp);
  await sp.goto(pathToFileURL(soloFile).href + "#s7");
  await sp.waitForSelector(".slide.active");
  const solo1 = await sp.evaluate(() => ({ count: document.querySelectorAll(".slide").length,
    active: document.querySelector(".slide.active").id,
    styled: getComputedStyle(document.querySelector(".controls")).display === "flex",
    stageW: document.querySelector(".slide.active .stage").getBoundingClientRect().width }));
  await sp.keyboard.press("ArrowRight");
  const solo2 = await sp.evaluate(() => document.querySelector(".slide.active").id);
  await sp.screenshot({ path: path.join(renderDir, "standalone-s8.png") });
  await sp.emulateMedia({ media: "print" });
  const soloPdf = path.join(renderDir, "standalone-print.pdf");
  await sp.pdf({ path: soloPdf, preferCSSPageSize: true, printBackground: true });
  const sinfo = pdfInfo(soloPdf);
  evidence.standalone = { file: rel(standalonePath), bytes: readFileSync(standalonePath).length,
    loaded_without_assets: solo1, after_arrow_right: solo2, print_pages: sinfo.pages };
  if (solo1.count !== 35 || solo1.active !== "s7" || !solo1.styled || solo1.stageW < 600) {
    fail(`standalone file did not load correctly: ${JSON.stringify(solo1)}`);
  }
  if (solo2 !== "s8") fail(`standalone navigation failed: ${solo2}`);
  if (sinfo.pages !== 35) fail(`standalone print has ${sinfo.pages} pages, expected 35`);
  await sctx.close();

  evidence.console_errors = consoleErrors;
  evidence.external_requests = externalRequests;
  if (consoleErrors.length) fail(`console errors: ${consoleErrors.slice(0, 3).join(" | ")}`);
  if (externalRequests.length) fail(`network requests: ${externalRequests.slice(0, 3).join(" | ")}`);
  await ctx.close();
} finally {
  await browser.close();
}

evidence.problems = problems;
evidence.passed = problems.length === 0;
writeFileSync(path.join(slidesDir, "html-check-evidence.json"), JSON.stringify(evidence, null, 2) + "\n");
console.log(`slides checked: ${evidence.slides ? evidence.slides.length : 0}`);
problems.forEach((p) => console.log("FAIL", p));
console.log(problems.length ? `${problems.length} problem(s)` : "ok");
process.exit(problems.length ? 1 : 0);
