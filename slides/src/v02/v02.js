/* Harness Engineering deck v02. No dependencies, works offline.
   Keys: Right, Down, PageDown, Space: next. Left, Up, PageUp: previous.
   Home, End: first and last. N: presenter notes. F: full screen.
   Deep link: #s7, #P3 or #7 opens that slide. ?notes=1 opens notes. ?shot=1 hides chrome. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");
  var params = new URLSearchParams(window.location.search);
  if (params.get("shot") === "1") root.classList.add("shot");

  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  if (!slides.length) return;
  var deck = document.getElementById("deck");
  var panel = document.getElementById("notes-panel");
  var notesBody = document.getElementById("notes-body");
  var toggle = document.getElementById("notes-toggle");
  var prevBtn = document.getElementById("prev");
  var nextBtn = document.getElementById("next");
  var counter = document.getElementById("counter");
  var bar = document.getElementById("progress-bar");
  var nowTitle = document.getElementById("now-title");
  var current = -1;

  function fit(stage) {
    var canvas = stage.querySelector(".canvas");
    if (canvas && stage.clientWidth) canvas.style.setProperty("--scale", stage.clientWidth / 1920);
  }
  var ro = window.ResizeObserver ? new ResizeObserver(function (entries) {
    entries.forEach(function (e) { fit(e.target); });
  }) : null;
  slides.forEach(function (s) {
    var st = s.querySelector(".stage");
    if (ro) ro.observe(st); else fit(st);
  });
  window.addEventListener("resize", function () { slides.forEach(function (s) { fit(s.querySelector(".stage")); }); });

  function indexFromHash() {
    var m = /^#(?:[Ps])?(\d+)/i.exec(window.location.hash || "");
    if (!m) return 0;
    var n = parseInt(m[1], 10) - 1;
    return n >= 0 && n < slides.length ? n : 0;
  }

  function show(i, updateHash) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === current) return;
    if (current >= 0) slides[current].classList.remove("active");
    current = i;
    var s = slides[i];
    s.classList.add("active");
    fit(s.querySelector(".stage"));
    counter.textContent = (i + 1) + " / " + slides.length;
    bar.style.width = ((i + 1) / slides.length * 100) + "%";
    nowTitle.textContent = s.getAttribute("data-label");
    document.title = s.getAttribute("data-label") + " | 하네스 엔지니어링";
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i === slides.length - 1;
    var notes = s.querySelector(".notes");
    notesBody.innerHTML = notes ? notes.innerHTML : "";
    notesBody.scrollTop = 0;
    if (updateHash !== false && window.history && window.history.replaceState) {
      window.history.replaceState(null, "", window.location.search + "#" + s.id);
    }
  }

  function setNotes(open) {
    panel.hidden = !open;
    deck.classList.toggle("notes-open", open);
    toggle.setAttribute("aria-pressed", open ? "true" : "false");
  }

  prevBtn.addEventListener("click", function () { show(current - 1); });
  nextBtn.addEventListener("click", function () { show(current + 1); });
  toggle.addEventListener("click", function () { setNotes(panel.hidden); });
  document.getElementById("notes-close").addEventListener("click", function () { setNotes(false); });

  document.addEventListener("keydown", function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    switch (e.key) {
      case "ArrowRight": case "ArrowDown": case "PageDown": case " ":
        e.preventDefault(); show(current + 1); break;
      case "ArrowLeft": case "ArrowUp": case "PageUp":
        e.preventDefault(); show(current - 1); break;
      case "Home": e.preventDefault(); show(0); break;
      case "End": e.preventDefault(); show(slides.length - 1); break;
      case "n": case "N": setNotes(panel.hidden); break;
      case "f": case "F":
        if (document.fullscreenElement) document.exitFullscreen();
        else if (root.requestFullscreen) root.requestFullscreen();
        break;
    }
  });

  var touchX = null;
  var vp = document.getElementById("viewport");
  vp.addEventListener("touchstart", function (e) {
    touchX = e.touches.length === 1 ? e.touches[0].clientX : null;
  }, { passive: true });
  vp.addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
    touchX = null;
  });

  window.addEventListener("hashchange", function () { show(indexFromHash(), false); });
  setNotes(params.get("notes") === "1");
  show(indexFromHash());
})();
