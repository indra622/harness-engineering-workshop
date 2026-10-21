// Browser check, render and print for the deck (42 slides, 44 from v07 with two reference slides, 45 from v16).
//
// Usage (from the project root, after build_v02.py):
//   PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js \
//     node slides/src/v02/check_v02.mjs
// DECK_VERSION selects the deck (default v03). Running it for v02 rewrites the
// delivered v02 PDF and evidence, so leave v02 alone unless that is intended.
//
// Renders every slide at 1920 x 1080 to slides/render/VER/ (git-ignored),
// prints slides/harness-engineering-workshop-VER.pdf from a non-first slide,
// and writes slides/VER-check-evidence.json. From v03 it also checks the
// physical page number on every slide, in the page and in the PDF text. Checks:
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
import { execFileSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..", "..");
const slidesDir = path.join(root, "slides");
// versions compare as strings: always two digits after "v" (v02 ... v16)
const VER = process.env.DECK_VERSION || "v16";
if (!/^v(0[2-9]|1[0-6])$/.test(VER)) throw new Error(`unknown DECK_VERSION ${VER}`);
const PAGENO = VER >= "v03";
// v07 adds two optional reference slides after the OMH case; v16 adds a third after the Grokbot case
const TOTAL = VER >= "v16" ? 45 : VER >= "v07" ? 44 : 42;
// v02 and v03 carry the 120-minute lecture schedule; v04 has no lecture timing at all
const TIMED = VER < "v04";
// lecture time on screen or in notes (tool and task times such as 09:12 or cron do not match)
const LECTURE_TIME = /\d+\s*분(?!기)|\d+\s*초(에서|이내|부터)|약\s*\d+\s*분|\d+\s*min\b/g;
const file = path.join(slidesDir, `harness-engineering-workshop-${VER}.html`);
const pdfPath = path.join(slidesDir, `harness-engineering-workshop-${VER}.pdf`);
const outDir = path.join(slidesDir, "render", VER);
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
// v04 keeps the teaching content of each v10 block: these labelled lines must be there in full
const KEY_FIELDS = ["장면과 질문", "한 문장 정의", "장면에 다시 적용", "강사용 보충 예시", "구체 예시", "헷갈리는 지점",
  "확인 질문과 모범 답안", "핵심 메시지", "전환 질문", "측정 상태"];
function v10KeyLines(sid) {
  const m = plan.match(new RegExp(`^### S${sid}\\. [\\s\\S]*?(?=^### S\\d+\\. |^## )`, "m"));
  if (!m) return null;
  return m[0].split("\n").filter((l) => KEY_FIELDS.some((k) => l.startsWith(`**${k}`)))
    .map((l) => squash(l.replace(/\*\*/g, "")));
}

const browser = await pw.chromium.launch({ headless: true, channel: "chrome" });
const evidence = { version: VER, browser: `Chrome ${browser.version()} (headless)`, file: rel(file), slides: [] };
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
    slides: items.length, ...(TIMED ? { minutes: items.reduce((a, b) => a + b.minutes, 0) } : {}),
    terms: items.filter((i) => i.kind === "term").map((i) => i.term),
    cases: items.filter((i) => i.kind === "case").map((i) => (TIMED ? `${i.case} (${i.minutes}분)` : i.case)),
    chapters: items.filter((i) => i.kind === "chapter").length,
    breaks: items.filter((i) => i.kind === "break").map((i) => (TIMED ? i.minutes : i.physical)),
    ceo: items.filter((i) => i.case === "CEO Agent").map((i) => ({ physical: i.physical, ...(TIMED ? { minutes: i.minutes } : {}) })),
    layouts: [...new Set(items.filter((i) => i.kind === "term").map((i) => i.layout))],
  };
  evidence.manifest = m;
  if (m.slides !== TOTAL || meta.attrs.length !== TOTAL) fail(`slide count ${m.slides}/${meta.attrs.length} != ${TOTAL}`);
  const refs = items.filter((it) => it.kind === "reference");
  if (refs.length !== TOTAL - 42) fail(`reference slides: ${refs.length}`);
  if (VER >= "v07") {
    // originals keep their v06 numbering; references sit right after original 14
    const origs = items.filter((it) => it.kind !== "reference").map((it) => it.original);
    if (JSON.stringify(origs) !== JSON.stringify([...Array(42).keys()].map((k) => k + 1))) fail("original numbering broken");
    const place = VER >= "v16" ? "15A,16B,21C" : "15A,16B";
    if (refs.map((r) => `${r.physical}${r.reference}`).join(",") !== place) fail(`reference placement: ${refs.map((r) => r.physical)}`);
    evidence.reference_slides = refs.map((r) => ({ physical: r.physical, reference: r.reference, label: r.label }));
  }
  if (TIMED && m.minutes !== 120) fail(`minutes ${m.minutes} != 120`);
  if (!TIMED) {
    const sched = items.filter((it) => "minutes" in it || "start" in it || "end" in it).map((it) => it.physical);
    if ("minutes" in meta.man || sched.length) fail(`v04 manifest still carries schedule fields: ${sched}`);
    const attrSched = meta.attrs.filter((a) => "minutes" in a || "start" in a).map((a) => a.physical);
    if (attrSched.length) fail(`v04 data attributes still carry schedule fields: ${attrSched}`);
  }
  if (JSON.stringify(m.terms) !== JSON.stringify(V10_TERMS)) fail("terms do not match the 25 v10 terms in order");
  if (m.cases.length !== 5) fail(`cases: ${m.cases.length}`);
  if (m.ceo.length !== 1 || (TIMED && m.ceo[0].minutes !== 3)) fail(`CEO Agent: ${JSON.stringify(m.ceo)}`);
  if (m.breaks.length !== 1 || (TIMED && m.breaks[0] !== 10)) fail(`break: ${m.breaks}`);
  if (m.layouts.length < 3) fail(`only ${m.layouts.length} term layout families`);
  items.forEach((it, i) => {
    const a = meta.attrs[i];
    if (Number(a.physical) !== it.physical || a.kind !== it.kind || (TIMED && Number(a.minutes) !== it.minutes) ||
        (it.term || "") !== (a.term || "") || (it.v10 || []).join(" ") !== (a.v10 || "")) {
      fail(`slide ${i + 1}: data attributes differ from the manifest`);
    }
    const nt = squash(meta.notes[i]);
    const fixes = { 9: "v02", 23: "v02", 29: "v02", 30: "v02", ...(VER >= "v03" ? { 2: "v03" } : {}),
      ...(VER >= "v06" ? { 18: "v06", 31: "v06" } : {}), ...(VER >= "v10" ? { 14: "v10" } : {}), ...(VER >= "v12" ? { 25: "v12" } : {}),
      ...(VER >= "v16" ? { 40: "v16" } : {}) };
    const orig = it.original || it.physical;  // corrections are keyed by the original slide
    if (it.kind !== "reference" && fixes[orig]) {
      const label = TIMED ? `${fixes[orig]} 정정 (아래 v10 원문보다 우선)` : "정정 (아래 v10 발췌보다 우선)";
      const fix = nt.indexOf(squash(label));
      const src = nt.indexOf(squash(TIMED ? "v10 원문 S" : "v10 발췌 S"));
      if (fix < 0 || src < 0 || fix > src) fail(`slide ${i + 1} (original ${orig}): correction must come before the v10 source block`);
    }
    if (nt.length < 80) fail(`slide ${i + 1}: notes are too short`);
    for (const sid of it.v10 || []) {
      const n = Number(sid.slice(1));
      if (TIMED) {
        const b = v10Block(n);
        if (!b || !nt.includes(b)) fail(`slide ${i + 1}: notes do not carry the full v10 block ${sid}`);
      } else {
        const label = VER >= "v06" ? "v06 편집" : "v04 편집";
        if (!nt.includes(squash(`v10 발췌 ${sid} (${label})`))) fail(`slide ${i + 1}: notes lack the labelled v10 excerpt ${sid}`);
        // v06 swaps outdated expressions in the excerpts; the manifest publishes the exact pairs, applied in order
        const swaps = (meta.man.excerpt_edits || []).map(([a, b]) => [squash(a), squash(b)]);
        const expect = (v10KeyLines(n) || []).map((l) => swaps.reduce((s, [a, b]) => s.split(a).join(b), l));
        const missing = expect.filter((l) => !nt.includes(l));
        if (missing.length) fail(`slide ${i + 1}: v10 ${sid} teaching lines missing from notes: ${missing.length}`);
      }
    }
    if (!TIMED) {
      const hits = meta.notes[i].match(LECTURE_TIME);
      if (hits) fail(`slide ${i + 1}: lecture time in notes: ${hits.join(", ")}`);
    }
  });

  if (!TIMED) {
    // nothing on screen, in labels or in the page head may give a lecture time
    const vis = await page.evaluate(() => ({
      head: document.title + " " + (document.querySelector('meta[name="description"]')?.content || ""),
      slides: [...document.querySelectorAll(".slide .canvas")].map((c) => c.textContent + " " +
        [...c.querySelectorAll("[aria-label]")].map((e) => e.getAttribute("aria-label")).join(" ")),
    }));
    const headHits = vis.head.match(LECTURE_TIME);
    if (headHits) fail(`lecture time in the page head: ${headHits}`);
    const slideHits = vis.slides.map((t, k) => [k + 1, t.match(LECTURE_TIME)]).filter(([, h]) => h);
    slideHits.forEach(([k, h]) => fail(`slide ${k}: lecture time on screen: ${h.join(", ")}`));
    evidence.lecture_time_references = { screen_and_labels: slideHits.length, page_head: headHits ? headHits.length : 0,
      notes: meta.notes.filter((t) => t.match(LECTURE_TIME)).length };
  }

  if (VER >= "v06") {
    // slide 9: one coordinator judges, delegates or handles directly, and checks the returned result
    const roles = await page.evaluate(() => {
      const all = [...document.querySelectorAll(".slide .canvas")].map((c) => c.textContent);
      const s9 = document.querySelector("#s9 .canvas").textContent;
      return { s9, parentOnScreen: all.map((t, k) => (t.includes("부모") ? k + 1 : 0)).filter(Boolean),
        toolRoute: all.map((t, k) => (t.includes("도구로 처리") ? k + 1 : 0)).filter(Boolean) };
    });
    const need = ["코디네이터", "직접 처리", "워커에게 위임", "결과 검증", "코디네이터가 확인", "같은 코디네이터", "작업 확인 화면"];
    const lacking = need.filter((w) => !roles.s9.includes(w));
    if (lacking.length) fail(`slide 9 lacks: ${lacking.join(", ")}`);
    if (roles.parentOnScreen.length) fail(`"부모" still on screen: ${roles.parentOnScreen}`);
    if (roles.toolRoute.length) fail(`"도구로 처리" on screen (route must be 직접 처리): ${roles.toolRoute}`);
    // slide 14: the same task before and after the OMH additions, with the evidence limit on screen
    const s14 = await page.evaluate(() => document.querySelector("#s14 .canvas").textContent);
    const need14 = VER >= "v14"
      ? ["요청", "표의 금액 빈칸만 0으로 채워 줘. 번호와 상품은 그대로", "빈칸만 채우랬는데, 번호까지 바뀌었다면?",
        "OpenCode 순정", "같은 일을 직접 꾸려 진행", "표를 고침", "금액 빈칸에 0을 채움", "원본과 비교", "비교 코드를 짜서 맞춰 봄",
        "기준에 따라 검토", "번호, 상품이 그대로인지", "필요하면 다시 맡김", "고칠 것을 되돌림", "OMH 통합 구성", "OMO 역할 협업",
        "총괄", "작업 담당", "검토 담당", "맡김", "고친 표", "다시 고침", "원본과 결과", "검토 결과", "검토 통과 뒤 보고",
        "금액 빈칸 → 0", "요청한 변경", "상품 A 번호 0 → 3", "요청 밖 변경", "준비된 비교 도구", "data_compare", "쓰는 이유",
        ...(VER >= "v15" ? ["반복할수록, 복잡할수록 커지는 하네스의 효용",
          "분업, 비교, 재검토 절차를 재사용해 복잡한 반복 작업의 준비와 확인 부담을 줄이기"]
          : ["OpenCode 순정도 네 단계를 할 수 있지만"])]
      : VER === "v13"
      ? ["요청", "표의 금액 빈칸만 0으로 채워 줘. 번호와 상품은 그대로", "빈칸만 채우랬는데, 번호까지 바뀌었다면?",
        "OpenCode 순정", "전용 도구가 없으면", "직접 준비할 것", "OMH 통합 구성", "OMO 역할 협업", "총괄", "작업 담당",
        "검토 담당", "맡김", "고친 표", "다시 고침", "원본과 결과", "검토 결과", "검토 통과 뒤 보고", "금액 빈칸 → 0", "요청한 변경", "상품 A 번호 0 → 3", "요청 밖 변경",
        "준비된 비교 도구", "data_compare", "쓰는 이유", "설명용", "실제로 실행한 결과"]
      : VER >= "v12"
      ? ["요청", "행 수는 그대로, 빠진 ID까지 찾아내기", "OpenCode 순정", "전용 도구가 없으면 직접 준비할 것", "OMH 통합 구성",
        "OMO: 역할 분담, 검토", "data_inspect, data_compare", "omh-rigorous", "첫 결과", "행 3 → 3", "빈 값 1 → 0",
        "id 기준 비교", "left_only 1", "right_only 1", "검토 기준", "추가, 삭제 0건", "완료 보고 전에 되돌림", "수정 결과",
        "left_only 0", "right_only 0", "자동 병합 없음", "행 값 없이", "쓰는 이유", "실제 실행한 개수", "설명용"]
      : VER >= "v10"
      ? ["같은 일", "OpenCode 순정", "범용 코딩 에이전트", "OMH 통합 구성", "OMO + 업무 도구 + 작업 절차",
        "OMO의 역할 구성까지 묶은 OMH", "OMO", "data_inspect", "data_compare", "자동 병합 없음", "행 값 없이",
        "omh-rigorous", "달라진 것", "사람이 결정", "사내 모델의 품질 비교는 하지 않음"]
      : ["같은 일", "추가 전", "OpenCode + OMO", "추가 후", "data_inspect", "data_compare", "자동 병합 없음",
        "달라진 것", "omh-rigorous", "사내 모델의 품질 비교는 하지 않음"];
    const lack14 = need14.filter((w) => !s14.includes(w));
    if (lack14.length) fail(`slide 14 lacks: ${lack14.join(", ")}`);
    evidence.omh_before_after = { has: need14.filter((w) => s14.includes(w)) };
    if (VER >= "v12") {
      // the scene: first result, keyed comparison, review criterion, fixed result, left to right;
      // the counts on screen are the ones the real tool run recorded for the synthetic fixture
      const sum = JSON.parse(readFileSync(path.join(root, "examples", "omh-v12", "evidence", "summary.json"), "utf8"));
      const steps = await page.evaluate(() => [...document.querySelectorAll("#s14 [data-step]")]
        .map((r) => [r.getAttribute("data-step"), parseFloat(r.getAttribute("x"))]));
      const order = steps.map((x) => x[0]).join(",");
      if (VER === "v12" && (order !== "first,compare,review,fixed" || !steps.every((x, k) => !k || x[1] > steps[k - 1][1]))) {
        fail(`slide 14 scene order: ${JSON.stringify(steps)}`);
      }
      const f1 = sum.first, f2 = sum.fixed;
      const agrees = f1.rows_before === 3 && f1.rows_after === 3 && sum.amount_blanks_before === 1 && f1.amount_blanks_after === 0 &&
        f1.left_only === 1 && f1.right_only === 1 && f1.scope === "full" && !f1.values_returned && f1.meets_criterion === false &&
        f2.left_only === 0 && f2.right_only === 0 && f2.scope === "full" && JSON.stringify(f2.changed_fields) === '["amount"]' &&
        f2.value_changed === 1 && f2.meets_criterion === true;
      if (!agrees) fail(`slide 14 counts do not match the recorded tool run: ${JSON.stringify(sum)}`);
      if (/%|항상|보장|자동으로 막|일마다|매번/.test(s14)) fail("slide 14 makes an absolute or speed claim on screen");
      evidence.omh_v12_scene = { order, first: f1, fixed: f2, engine_version: sum.engine_version };
    }
    if (VER >= "v13") {
      // slide 14 as a role handoff: plain request, roles inside OMO, every arrow between the right roles in order,
      // the correction back through the same 총괄, the report only after the re-check
      if (/CSV|amount|left_only|right_only|value_changed/.test(s14)) fail("slide 14 shows technical field names on screen");
      const r = await page.evaluate(() => {
        const box = (el) => {
          const [x, y, w, h] = ["x", "y", "width", "height"].map((a) => parseFloat(el.getAttribute(a)));
          return [x, y, x + w, y + h];
        };
        const roles = Object.fromEntries([...document.querySelectorAll("#s14 [data-role]")]
          .map((el) => [el.getAttribute("data-role"), box(el)]));
        const flows = [...document.querySelectorAll("#s14 polyline[data-kind]")].map((el) => ({
          from: el.getAttribute("data-from"), to: el.getAttribute("data-to"),
          kind: el.getAttribute("data-kind"), dashed: el.hasAttribute("stroke-dasharray"),
          pts: el.getAttribute("points").split(" ").map((p) => p.split(",").map(Number)) }));
        const omo = document.querySelector('#s14 [data-box="omo"]');
        return { roles, flows, omo: omo && box(omo) };
      });
      const inside = (a, b) => a && b && a[0] >= b[0] && a[1] >= b[1] && a[2] <= b[2] && a[3] <= b[3];
      if (!["lead", "worker", "reviewer"].every((k) => inside(r.roles[k], r.omo))) fail(`slide 14 roles must sit inside OMO: ${JSON.stringify(r)}`);
      // one arrow per role pair and direction, few enough to read at a glance
      const seq = r.flows.map((x) => `${x.from}>${x.to}:${x.kind}`).join(" ");
      const want = "lead>worker:assign worker>lead:result lead>worker:return lead>reviewer:assign reviewer>lead:evidence " +
        "lead>requester:report";
      if (seq !== want) fail(`slide 14 handoffs: ${seq}`);
      // each arrow starts at its sender's edge and ends at its receiver's edge (within a marker's length)
      const near = (v, w) => Math.abs(v - w) <= 8;
      const ends = r.flows.filter((x) => x.to !== "requester").every((x) => {
        const [[x1, y1], [x2, y2]] = x.pts;
        const a = r.roles[x.from], b = r.roles[x.to];
        const right = a[0] < b[0];
        return y1 === y2 && y1 > a[1] && y1 < a[3] && y1 > b[1] && y1 < b[3] &&
          near(x1, right ? a[2] : a[0]) && near(x2, right ? b[0] : b[2]);
      });
      if (!ends) fail("slide 14 handoff arrows do not join their roles");
      const report = r.flows.find((x) => x.kind === "report");
      const lead = r.roles.lead;
      if (!report || !(report.pts[0][0] > lead[0] && report.pts[0][0] < lead[2] && near(report.pts[0][1], lead[1]) && report.pts[1][1] < 80)) {
        fail(`slide 14 report must leave 총괄 for the request strip: ${JSON.stringify(report)}`);
      }
      if (!r.flows.find((x) => x.kind === "return").dashed) fail("slide 14 correction arrow must be dashed");
      if (r.flows.some((x) => (x.from === "worker" && x.to === "reviewer") || (x.from === "reviewer" && x.to === "requester"))) {
        fail("slide 14 has a handoff that bypasses 총괄");
      }
      // the change strip follows the real comparison: one number gone, one new; the fixed result passes
      const sum = JSON.parse(readFileSync(path.join(root, "examples", "omh-v12", "evidence", "summary.json"), "utf8"));
      if (!(sum.first.left_only === 1 && sum.first.right_only === 1 && sum.fixed.left_only === 0 && sum.fixed.right_only === 0)) {
        fail("slide 14 change strip no longer matches the recorded tool run");
      }
      evidence.omh_v13_roles = { handoffs: seq, roles_inside_omo: true, arrows_join_roles: ends };
    }
    if (VER >= "v14") {
      // slide 14 left panel: four process steps in order, every line inside the OpenCode box;
      // no on-screen footnote, and the summary strip sits lower than in v13 yet clear of the page number
      await page.evaluate(() => { location.hash = "#s14"; });
      await page.waitForFunction(() => document.querySelector(".slide.active")?.id === "s14");
      await page.waitForTimeout(80);
      const v = await page.evaluate(() => {
        const s = document.querySelector("#s14");
        const canvas = s.querySelector(".canvas").getBoundingClientRect();
        const k = canvas.width / 1920;
        const rel = (q) => ({ top: (q.top - canvas.top) / k, bottom: (q.bottom - canvas.top) / k,
          left: (q.left - canvas.left) / k, right: (q.right - canvas.left) / k });
        const oc = rel(s.querySelector('[data-box="opencode"]').getBoundingClientRect());
        const steps = [...s.querySelectorAll("g[data-step]")].map((g) => ({ n: g.getAttribute("data-step"),
          texts: [...g.querySelectorAll("text")].map((tx) => ({ t: tx.textContent, ...rel(tx.getBoundingClientRect()) })) }));
        const loop = s.querySelector('[data-box="opencode"] ~ polyline[stroke-dasharray]');
        return { oc, steps, foot: !!s.querySelector(".foot"),
          summary: rel(s.querySelector('[data-box="summary"]').getBoundingClientRect()),
          pageno: rel(s.querySelector(".pageno").getBoundingClientRect()), loop: !!loop };
      });
      if (v.steps.map((x) => x.n).join(",") !== "1,2,3,4") fail(`slide 14 left steps: ${v.steps.map((x) => x.n)}`);
      const want = ["표를 고침", "원본과 비교", "기준에 따라 검토", "필요하면 다시 맡김"];
      if (JSON.stringify(v.steps.map((x) => x.texts[1]?.t)) !== JSON.stringify(want)) fail(`slide 14 step order: ${JSON.stringify(v.steps)}`);
      const tops = v.steps.map((x) => x.texts[0].top);
      if (!tops.every((y, i) => !i || y > tops[i - 1])) fail("slide 14 steps must run top to bottom");
      const out = v.steps.flatMap((x) => x.texts).filter((r) => r.left < v.oc.left || r.right > v.oc.right || r.top < v.oc.top || r.bottom > v.oc.bottom);
      if (out.length) fail(`slide 14 step text outside the OpenCode box: ${JSON.stringify(out)}`);
      if (!v.loop) fail("slide 14 lacks the dashed return from step 4");
      if (v.foot) fail("slide 14 still shows a footnote");
      if (!(v.summary.top >= 890)) fail(`slide 14 summary must sit lower than v13 (top ${v.summary.top})`);
      if (!(v.summary.bottom <= v.pageno.top - 4)) fail(`slide 14 summary overlaps the page number: ${JSON.stringify(v)}`);
      evidence.omh_v14_process = { steps: want, summary_top: Math.round(v.summary.top), summary_bottom: Math.round(v.summary.bottom),
        pageno_top: Math.round(v.pageno.top), footnote: v.foot };
    }
    if (VER >= "v10") {
      // OMO must sit inside the OMH boundary, and bare OpenCode outside it
      const geo = await page.evaluate(() => {
        const g = (k) => {
          const r = document.querySelector(`#s14 [data-box="${k}"]`);
          if (!r) return null;
          const [x, y, w, h] = ["x", "y", "width", "height"].map((a) => parseFloat(r.getAttribute(a)));
          return [x, y, x + w, y + h];
        };
        return { omh: g("omh"), omo: g("omo"), tools: g("tools"), procedure: g("procedure"), opencode: g("opencode") };
      });
      const inside = (a, b) => a && b && a[0] >= b[0] && a[1] >= b[1] && a[2] <= b[2] && a[3] <= b[3];
      const apart = (a, b) => a && b && (a[2] <= b[0] || b[2] <= a[0]);
      // from v13 the procedure is named in the OMH header rather than drawn as its own box
      const nested = (VER >= "v13" ? ["omo", "tools"] : ["omo", "tools", "procedure"]).every((k) => inside(geo[k], geo.omh));
      if (!nested) fail(`slide 14: OMO, tools and procedure must sit inside OMH: ${JSON.stringify(geo)}`);
      if (!apart(geo.opencode, geo.omh)) fail("slide 14: OpenCode 순정 must sit outside OMH");
      if (/추가 전|OpenCode \+ OMO/.test(s14)) fail("slide 14 still shows the old OpenCode + OMO baseline");
      evidence.omh_v10_structure = { omo_tools_procedure_inside_omh: nested, opencode_outside_omh: apart(geo.opencode, geo.omh) };
    }
    evidence.role_wording = { slide9_has: need.filter((w) => roles.s9.includes(w)),
      parent_on_screen: roles.parentOnScreen, tool_route_label: roles.toolRoute };
  }

  if (VER >= "v07") {
    // reference slides: content, provenance on screen, pinned sources in notes
    const ref = await page.evaluate(() => ["#s15", "#s16"].map((id) => {
      const s = document.querySelector(id);
      return { text: s.querySelector(".canvas").textContent, notes: s.querySelector(".notes").innerHTML,
        skip: s.querySelector(".canvas a.ref-skip")?.getAttribute("href") };
    }));
    const needA = VER >= "v12"
      ? ["참고 A", "기본기는 모델에, 업무 기준과 위임은 하네스에", "Superpowers", "pstack", "먼저, 실행 기본기", "다음 초점",
        "그 위에서, 이 일에 맞게", "잘 만든 기본 절차,", "계속 다듬어지는 습관", "성공 기준과 근거", "작업별 절차 선택",
        "범위 정한 위임", "돌아온 결과 검증", "계획하고 시험하는 기본기는 모델에 스며들고", "111cf6a", "b739a8a"]
      : VER === "v11"
      ? ["참고 A", "기본기 다음은, 검증과 위임", "Superpowers", "pstack", "업무 운영 층", "실행 기본기", "잘 만든 기본 절차,",
        "계속 다듬어지는 습관", "성공 기준과 근거", "작업별 절차 선택", "범위 정한 위임", "돌아온 결과 검증",
        "계획하고 시험하는 기본기는 모델에 스며들고", "기본기는 모델에, 업무 기준과 위임은 하네스에", "111cf6a", "b739a8a"]
      : VER === "v10"
      ? ["참고 A", "AS-IS", "TO-BE", "Superpowers", "pstack", "작업별 절차 선택으로", "바뀌는 초점", "의도와 설계 합의",
        "테스트 먼저 구현", "작업별 플레이북", "범위 정해 위임", "실제 동작으로 검증", "111cf6a", "b739a8a"]
      : ["참고 A", "같은 개발 요청, 서로 다른 작업 설계", "pstack", "Superpowers", "공통점", "실제 동작으로 검증",
        "테스트 먼저 구현", "111cf6a", "b739a8a"];
    const needB = ["참고 B", "가져올 것은 기능 목록보다 작업 방식", "내 환경에서 쓸", "적용 예: OMH", "omh-rigorous",
      ...(VER < "v11" ? ["비교 참고"] : []),
      ...(VER === "v10" ? ["TO-BE pstack", "AS-IS Superpowers", "OMO 역할 구성"] : []),
      ...(VER >= "v11" ? ["pstack에서 참고할 운영 방식", "Superpowers에서 참고할 기본기", "포함", "OMO 역할 구성", "같음"] : [])];
    const pins = ["cursor/plugins/blob/111cf6a16b11cc822782c1585859af4a580a2490", "obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12"];
    [[ref[0], needA, "15"], [ref[1], needB, "16"]].forEach(([r, need, n]) => {
      const lack = need.filter((w) => !r.text.includes(w));
      if (lack.length) fail(`slide ${n} lacks: ${lack.join(", ")}`);
      if (r.skip !== "#s17") fail(`slide ${n} skip link: ${r.skip}`);
      if (!pins.every((u) => r.notes.includes(u))) fail(`slide ${n} notes lack pinned source links`);
    });
    evidence.reference_checks = { skip_links: ref.map((r) => r.skip), pinned_sources_in_notes: true };
    if (VER === "v10") {
      // AS-IS sits above TO-BE on slide 15, joined by the transition arrow
      const order = await page.evaluate(() => {
        const at = (w) => parseFloat([...document.querySelectorAll("#s15 svg text")].find((n) => n.textContent === w)?.getAttribute("y"));
        return { asis: at("AS-IS"), tobe: at("TO-BE"), arrow: !!document.querySelector("#s15 svg polygon") };
      });
      if (!(order.asis < order.tobe) || !order.arrow) fail(`slide 15 direction: ${JSON.stringify(order)}`);
      evidence.reference_direction = order;
    }
    if (VER >= "v11") {
      // slide 15 is an emphasis shift: no AS-IS/TO-BE anywhere on 15 or 16, no migration arrow,
      // the operating layer drawn above the execution habits, and no sweeping training claim
      const v11 = await page.evaluate(() => ["#s15", "#s16"].map((id) => {
        const s = document.querySelector(id);
        const c = s.querySelector(".canvas");
        const labels = [...c.querySelectorAll("[aria-label]")].map((n) => n.getAttribute("aria-label")).join(" ");
        const at = (w) => parseFloat([...s.querySelectorAll("svg text")].find((n) => n.textContent === w)?.getAttribute("y"));
        return { screen: c.textContent + " " + labels, notes: s.querySelector(".notes").innerHTML,
          title: s.querySelector(".case-title")?.textContent, polygons: s.querySelectorAll("svg polygon").length,
          upper: at("업무 운영 층"), lower: at("실행 기본기"),
          dashedSuper: !!s.querySelector('svg polyline[points="520,282 570,282 570,270 614,270"][stroke-dasharray]') };
      }));
      const [a, b] = v11;
      if (VER === "v11" && a.title !== "기본기 다음은, 검증과 위임") fail(`slide 15 title: ${a.title}`);
      v11.forEach((r, k) => {
        const n = 15 + k;
        if (/AS-IS|TO-BE/i.test(r.screen)) fail(`slide ${n} still shows AS-IS/TO-BE on screen`);
        if (/AS-IS|TO-BE/i.test(r.notes)) fail(`slide ${n} notes still frame AS-IS/TO-BE`);
      });
      if (a.polygons) fail("slide 15 keeps the migration arrow");
      if (VER === "v11" && !(a.upper < a.lower)) fail(`slide 15 layers: ${JSON.stringify({ upper: a.upper, lower: a.lower })}`);
      if (!b.dashedSuper) fail("slide 16 Superpowers line is no longer dashed");
      const sweeping = ["모든 모델", "모든 프론티어", "100%", "빠짐없이 따른다", "항상 따른다", "Superpowers를 학습했", "RL 때문에", "강화학습 때문에"];
      const said = sweeping.filter((w) => a.screen.includes(w) || b.screen.includes(w));
      if (said.length) fail(`slides 15/16 make a sweeping claim on screen: ${said.join(", ")}`);
      const factNeed = ["사실과 해석", "강화학습", "이 발표의 관점", "https://openai.com/index/introducing-codex/",
        "https://openai.com/index/harness-engineering/",
        "obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/RELEASE-NOTES.md"];
      const lackFact = factNeed.filter((w) => !a.notes.includes(w));
      if (lackFact.length) fail(`slide 15 notes lack fact/interpretation: ${lackFact.join(", ")}`);
      if (!b.notes.includes("RELEASE-NOTES.md")) fail("slide 16 notes lack the pinned release notes");
      evidence.reference_v11 = { title: a.title, polygons: a.polygons, upper_y: a.upper, lower_y: a.lower,
        superpowers_line_dashed: b.dashedSuper, as_is_to_be_on_15_16: false };
    }
    if (VER >= "v12") {
      // slide 15: the thesis is the title, above both rows; Superpowers is read first, pstack below it in blue
      const h = await page.evaluate(() => {
        const s = document.querySelector("#s15");
        const svg = s.querySelector("svg");
        const texts = [...svg.querySelectorAll("text")];
        const at = (w) => texts.find((n) => n.textContent === w);
        const boxFill = (w) => {  // the rect drawn just before a label is the box it sits in
          let n = at(w)?.previousElementSibling;
          while (n && n.tagName !== "rect") n = n.previousElementSibling;
          return n?.getAttribute("fill");
        };
        return { title: s.querySelector(".case-title").textContent,
          titleTop: parseFloat(getComputedStyle(s.querySelector(".case-title")).top), svgTop: parseFloat(svg.style.top),
          superY: parseFloat(at("Superpowers")?.getAttribute("y")), pstackY: parseFloat(at("pstack")?.getAttribute("y")),
          pstackFill: boxFill("pstack"), superFill: boxFill("Superpowers") };
      });
      if (h.title !== "기본기는 모델에, 업무 기준과 위임은 하네스에") fail(`slide 15 title: ${h.title}`);
      if (!(h.titleTop < h.svgTop)) fail(`slide 15 thesis must sit above both rows: ${JSON.stringify(h)}`);
      if (!(h.superY < h.pstackY)) fail(`slide 15 reading order (Superpowers then pstack): ${JSON.stringify(h)}`);
      if (h.pstackFill !== "#2457A6" || h.superFill === "#2457A6") fail(`slide 15 emphasis: ${JSON.stringify(h)}`);
      evidence.reference_v12 = h;
    }
  }

  if (VER >= "v12") {
    const flow = await page.evaluate(() => {
      const labels = (svg, rects) => rects.map((r) => {
        const out = [];
        for (let n = r.nextElementSibling; n && n.tagName === "text"; n = n.nextElementSibling) out.push(n.textContent);
        return [out.join(" "), r.getAttribute("fill"), r.getAttribute("stroke")];
      });
      const s2 = document.querySelector("#s2 svg");
      const r2 = [...s2.querySelectorAll("rect")].filter((r) => r.getAttribute("height") === "140");
      const s27 = document.querySelector('.slide[data-case="AI교양"]');  // physical 27 until v15, 28 from v16
      const r27 = [...s27.querySelectorAll("svg rect[data-step]")];
      return { s2: labels(s2, r2), s27: labels(s27, r27), roles: r27.map((r) => r.getAttribute("data-role")),
        text: s27.querySelector(".canvas").textContent, sec: s27.dataset };
    });
    if (flow.s27.length !== 7 || JSON.stringify(flow.s27) !== JSON.stringify(flow.s2)) {
      fail(`slide 27 flow must match slide 2: ${JSON.stringify(flow)}`);
    }
    if (flow.roles.join(",") !== "author,author,ai,author,run,run,run") fail(`slide 27 roles: ${flow.roles}`);
    const need27 = ["사례 4 / 5", "초고 v01을", "직접 쓰기", "AI와 함께", "작가가 결정", "확정 뒤 정해진 절차", "공개 발행은 이 흐름 밖",
      "규칙", "컨텍스트", "도구", "상태", "검증"];
    const lack27 = need27.filter((w) => !flow.text.includes(w));
    if (lack27.length) fail(`slide 27 lacks: ${lack27.join(", ")}`);
    if (flow.sec.original !== "25" || flow.sec.case !== "AI교양" || flow.sec.v10 !== "S21") fail("slide 27 source fields changed");
    evidence.ai_flow_v12 = { steps: flow.s27.map((x) => x[0]), roles: flow.roles, matches_slide2: true };
  }

  if (VER >= "v16") {
    // physical map: Grokbot case 20, 참고 C 21, AI교양 28, break 29, CEO Agent 34, Q&A 45
    const at = (f) => items.find(f)?.physical;
    const map = { grok: at((i) => i.case === "Grokbot"), refC: at((i) => i.reference === "C"), ai: at((i) => i.case === "AI교양"),
      brk: at((i) => i.kind === "break"), ceo: at((i) => i.case === "CEO Agent"), qa: at((i) => i.kind === "qa") };
    if (JSON.stringify(map) !== JSON.stringify({ grok: 20, refC: 21, ai: 28, brk: 29, ceo: 34, qa: 45 })) fail(`v16 physical map: ${JSON.stringify(map)}`);
    const v = await page.evaluate(() => {
      const read = (id) => {
        const s = document.querySelector(id);
        const c = s.querySelector(".canvas");
        const aria = [...c.querySelectorAll("[aria-label]")].map((n) => n.getAttribute("aria-label")).join(" ");
        return { text: c.textContent, aria, notes: s.querySelector(".notes").innerHTML,
          title: s.querySelector(".case-title")?.textContent, skip: c.querySelector("a.ref-skip")?.getAttribute("href") };
      };
      const box = (el) => {
        const [x, y, w, h] = ["x", "y", "width", "height"].map((a) => parseFloat(el.getAttribute(a)));
        return [x, y, x + w, y + h];
      };
      const cloud = document.querySelector('#s20 [data-box="cloud"]');
      const bots = [...document.querySelectorAll("#s20 [data-bot]")].map((el) => [el.getAttribute("data-bot"), box(el)]);
      const qa = [...document.querySelectorAll(".slide[data-kind='qa'] b")].map((b) => Number(b.textContent));
      return { s20: read("#s20"), s21: read("#s21"), s43: read("#s43"), s2notes: document.querySelector("#s2 .notes").innerHTML,
        cloud: cloud && box(cloud), bots, axes: !!document.querySelector("#s20 .grok-axes"), qa };
    });
    // slide 20: the four confirmed bots in one cloud, the no-own-hardware message, no stale captions anywhere current
    const names = ["록식이", "에식이", "소식이", "최저가봇"];
    if (JSON.stringify(v.bots.map((b) => b[0])) !== JSON.stringify(names)) fail(`slide 20 bots: ${v.bots.map((b) => b[0])}`);
    const inside = (a, b) => a && b && a[0] >= b[0] && a[1] >= b[1] && a[2] <= b[2] && a[3] <= b[3];
    if (!v.bots.every((b) => inside(b[1], v.cloud))) fail("slide 20 bots must sit inside the cloud box");
    const need20 = ["내 맥미니 없이도, 클라우드에서 도는 봇 넷", "클라우드", "공유 컴퓨터", "연결한 앱", "루틴", "직접 운영", "클식이",
      "클라우드 서비스", "Grok Bot", "늘 켜 둔 내 장비 없이도", "하네스를 쓸 수 있음", "서비스마다 권한과 이용 조건은 다름", "참고 C"];
    const lack20 = need20.filter((w) => !v.s20.text.includes(w));
    if (lack20.length) fail(`slide 20 lacks: ${lack20.join(", ")}`);
    if (v.axes || v.s20.text.includes("네 개의 비교 축")) fail("slide 20 still leads with the axis comparison");
    const stale = /미확인|첨부|원자료|설명상/;
    for (const [n, r] of [["20", v.s20], ["21", v.s21], ["43", v.s43]]) {
      if (stale.test(r.text) || stale.test(r.aria)) fail(`slide ${n} still shows a stale attachment caption`);
    }
    if (stale.test(v.s20.notes.replace(/<h3>v10 발췌[\s\S]*$/, ""))) fail("slide 20 current notes still call the source unverified");
    if (/첨부 자료를 열 수 없었다|첨부 미확인/.test(v.s20.notes + v.s43.notes)) fail("v16 excerpts still carry the stale attachment lines");
    if (!v.s20.notes.includes("https://x.ai/news/introducing-grok-bot")) fail("slide 20 notes lack the xAI source");
    // 참고 C: three cloud personal agents, their differences and what they share; no volatile conditions on screen
    const need21 = ["참고 C", "맥미니 없이도, 클라우드에서 쓰는 개인 에이전트", "dots", "OpenAI", "Grok Bot", "xAI", "Muse", "Meta",
      "들어가는 곳", "맡기는 일", "사람이 보는 곳", "ChatGPT에서 시작", "봇별 대화, 그룹 대화", "앱이나 WhatsApp",
      "셋의 공통점", "클라우드의 자기 컴퓨터", "연결한 앱", "이어지는 기억", "사람의 확인"];
    const lack21 = need21.filter((w) => !v.s21.text.includes(w));
    if (lack21.length) fail(`slide 21 lacks: ${lack21.join(", ")}`);
    if (v.s21.skip !== "#s22") fail(`slide 21 skip link: ${v.s21.skip}`);
    if (/\d{4}\.\s?\d|요금|구독|무료|Pro|Premium|\d,\d{3}|베타|미국|\$/.test(v.s21.text)) fail("slide 21 shows dates, pricing or regions");
    const src21 = ["https://help.openai.com/en/articles/20001530-getting-started-with-your-dot", "https://x.ai/news/introducing-grok-bot",
      "https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/"];
    if (!src21.every((u) => v.s21.notes.includes(u))) fail("slide 21 notes lack the three official sources");
    // pointers: the Q&A index and the slide 2 notes name the v16 physical pages
    const wantQa = items.filter((i) => i.kind === "term" || i.kind === "case").map((i) => i.physical);
    if (JSON.stringify(v.qa) !== JSON.stringify(wantQa)) fail(`Q&A index ${v.qa} != ${wantQa}`);
    const wf = at((i) => i.term === "워크플로우");
    if (!v.s2notes.includes(`AI교양 사례(${map.ai}번)`) || !v.s2notes.includes(`워크플로우(${wf}번)`)) fail("slide 2 note pointers not moved");
    evidence.v16 = { physical_map: map, bots: names, qa_index: v.qa, refC_skip: v.s21.skip };
  }

  if (VER >= "v08") {
    const text = await page.locator("#s9 .canvas").textContent();
    if (!text.includes("업무 난이도 자동 판단")) fail("slide9 lacks automatic difficulty judgment");
    const screen = await page.locator(".canvas").allTextContents();
    if (screen.some(t => t.includes("OpenClaw"))) fail("case naming still shows OpenClaw on screen");
    if (!text.includes("클식이")) fail("slide9 lacks the familiar case name");
  }

  if (VER >= "v09") {
    if (!(await page.locator("#s9 .canvas").textContent()).includes("채널, 세션, 스케줄러")) fail("slide9 gateway lacks scheduler");
  }

  // ---------------------------------------------------------------- per-slide layout
  for (let i = 0; i < items.length; i++) {
    const id = `s${i + 1}`;
    await page.evaluate((h) => { location.hash = h; }, `#${id}`);
    await page.waitForFunction((x) => document.querySelector(".slide.active")?.id === x, id);
    if (VER >= "v16") {
      // a newly shown slide can paint its Korean headings late; let fonts and paint settle before measuring
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(220);
    } else {
      await page.waitForTimeout(40);
    }
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
      const pn = canvas.querySelector(".pageno");
      out.pageno = pn ? { text: pn.textContent.trim(), ...box(pn.getBoundingClientRect()), color: getComputedStyle(pn).color } : null;
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
    if (PAGENO) {
      const q = r.pageno;
      const want = `${i + 1} / ${items.length}`;
      if (!q || q.text !== want) fail(`${tag}: page number is ${q ? q.text : "missing"}, expected ${want}`);
      else if (q.x < 1500 || q.y < 960 || q.x + q.w > 1880 || q.y + q.h > 1040) {
        fail(`${tag}: page number not in the bottom-right safe corner (${q.x.toFixed(0)},${q.y.toFixed(0)})`);
      }
    } else if (r.pageno) fail(`${tag}: ${VER} should not carry a page number`);
    const png = path.join(outDir, `s${String(i + 1).padStart(2, "0")}.png`);
    await page.screenshot({ path: png });
    evidence.slides.push({ physical: i + 1, kind: items[i].kind, layout: items[i].layout, text_runs: r.runs,
      min_font_px: r.minFont, ...(r.pageno ? { page_number: r.pageno.text, page_number_color: r.pageno.color } : {}),
      png: rel(png) });
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
  const want = { arrowRight: "s2", pageDown: "s3", arrowLeft: "s2", end: `s${TOTAL}`, home: "s1", nextButton: "s2", prevButton: "s1" };
  for (const [kk, v] of Object.entries(want)) if (ix[kk] !== v) fail(`interaction ${kk}: ${ix[kk]}`);
  if (!ix.prevDisabledOnFirst) fail("previous button is enabled on the first slide");
  if (!ix.notes.open || ix.notes.chars < 100 || !ix.notesClosed) fail("notes did not open and close");
  if (!ix.fullscreenOn || !ix.fullscreenOff) fail(`full screen toggle: ${ix.fullscreenOn}/${ix.fullscreenOff}`);
  const ceoAt = items.find((it) => it.case === "CEO Agent").physical;
  await p2.goto(url + `?notes=1#s${ceoAt}`);
  await p2.waitForSelector(".slide.active");
  ix.deepLinkCeo = await p2.evaluate(() => ({ id: document.querySelector(".slide.active").id,
    notesOpen: !document.getElementById("notes-panel").hidden,
    canonical: document.getElementById("notes-body").textContent.includes("CEO Agent: 조사한 페르소나를 상황에 맞게 적용하기"),
    counter: document.getElementById("counter").textContent }));
  if (ix.deepLinkCeo.id !== `s${ceoAt}` || !ix.deepLinkCeo.canonical || !ix.deepLinkCeo.notesOpen || ix.deepLinkCeo.counter !== `${ceoAt} / ${TOTAL}`) {
    fail(`deep link s${ceoAt}: ${JSON.stringify(ix.deepLinkCeo)}`);
  }
  await p2.goto(url + "#7");
  await p2.waitForSelector(".slide.active");
  ix.deepLinkNumber = await at();
  if (ix.deepLinkNumber !== "s7") fail(`deep link #7: ${ix.deepLinkNumber}`);
  await p2.screenshot({ path: path.join(outDir, "interaction-s7.png") });
  if (VER >= "v07") {
    // the optional reference slides can be skipped in one click
    await p2.goto(url + "#s15");
    await p2.waitForSelector(".slide.active");
    await p2.click("#s15 a.ref-skip");
    await p2.waitForFunction(() => document.querySelector(".slide.active")?.id === "s17");
    ix.referenceSkip = await at();
    if (ix.referenceSkip !== "s17") fail(`reference skip link: ${ix.referenceSkip}`);
    if (VER >= "v16") {
      await p2.goto(url + "#s21");
      await p2.waitForSelector(".slide.active");
      await p2.click("#s21 a.ref-skip");
      await p2.waitForFunction(() => document.querySelector(".slide.active")?.id === "s22");
      ix.referenceSkipC = await at();
      if (ix.referenceSkipC !== "s22") fail(`reference C skip link: ${ix.referenceSkipC}`);
    }
  }
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
  if (visibleNoJs !== TOTAL) fail(`without JavaScript only ${visibleNoJs} slides are visible`);
  await pn.screenshot({ path: path.join(outDir, "no-javascript.png") });
  await nj.close();

  // ---------------------------------------------------------------- single file from an empty folder
  const tmp = mkdtempSync(path.join(os.tmpdir(), `deck-${VER}-`));
  const copy = path.join(tmp, path.basename(file));
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
  if (solo.count !== TOTAL || solo.active !== "s15" || !solo.styled || solo.stageW < 800) fail(`standalone copy: ${JSON.stringify(solo)}`);
  await sc.close();

  // ---------------------------------------------------------------- print from a non-first slide
  const pp = await ctx.newPage();
  await pp.goto(url + "#s20");
  await pp.waitForSelector(".slide.active");
  const activeBeforePrint = await pp.evaluate(() => document.querySelector(".slide.active").id);
  await pp.emulateMedia({ media: "print" });
  if (VER >= "v12") {
    // print makes every slide visible at once: let fonts load and paint settle before printing,
    // and give the PDF the deck's own title rather than the active slide's label
    await pp.evaluate(async (title) => {
      document.title = title;
      await document.fonts.ready;
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    }, `하네스 엔지니어링 워크숍 ${VER}`);
    await pp.waitForTimeout(250);
  }
  await pp.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true });
  const raw = readFileSync(pdfPath).toString("latin1");
  const pages = (raw.match(/\/Type\s*\/Page(?![a-zA-Z])/g) || []).length;
  const box = raw.match(/\/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]/);
  const ratio = box ? Number(box[1]) / Number(box[2]) : 0;
  evidence.pdf = { file: rel(pdfPath), printed_from: activeBeforePrint, pages, media_box: box ? [Number(box[1]), Number(box[2])] : null,
    ratio: Number(ratio.toFixed(4)) };
  if (pages !== TOTAL) fail(`PDF has ${pages} pages, expected ${TOTAL}`);
  if (Math.abs(ratio - 16 / 9) > 0.01) fail(`PDF page ratio ${ratio}`);
  if (PAGENO) {
    // the printed page itself must carry its number (poppler pdftotext, one page at a time)
    const missing = [];
    for (let k = 1; k <= pages; k++) {
      const txt = execFileSync("pdftotext", ["-f", String(k), "-l", String(k), "-layout", pdfPath, "-"], { encoding: "utf8" });
      if (!txt.replace(/\s+/g, " ").includes(`${k} / ${pages}`)) missing.push(k);
    }
    evidence.pdf.page_numbers_in_text = missing.length ? `missing on ${missing.join(", ")}` : `all ${pages} pages`;
    if (missing.length) fail(`PDF pages without their page number: ${missing.join(", ")}`);
  }
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
writeFileSync(path.join(slidesDir, `${VER}-check-evidence.json`), JSON.stringify(evidence, null, 2) + "\n");
problems.forEach((x) => console.log("FAIL", x));
console.log(problems.length ? `${problems.length} problem(s)` : "ok");
process.exit(problems.length ? 1 : 0);
