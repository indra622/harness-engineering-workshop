/* Harness Engineering Workshop deck navigation. No dependencies, works offline.
   Keys: Right, Down, PageDown, Space: next. Left, Up, PageUp: previous.
   Home, End: first and last. N: presenter notes. F: full screen.
   Deep links: index.html#s7 opens slide S7 (index.html#7 also works). */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

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

  function indexFromHash() {
    var m = /^#s?(\d+)$/i.exec(window.location.hash || "");
    if (!m) return 0;
    var n = parseInt(m[1], 10);
    for (var i = 0; i < slides.length; i++) {
      if (parseInt(slides[i].getAttribute("data-sid"), 10) === n) return i;
    }
    return 0;
  }

  function show(i, updateHash) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === current) return;
    if (current >= 0) slides[current].classList.remove("active");
    current = i;
    var s = slides[i];
    s.classList.add("active");
    var sid = s.getAttribute("data-sid");
    counter.textContent = (i + 1) + " / " + slides.length;
    bar.style.width = ((i + 1) / slides.length * 100) + "%";
    nowTitle.textContent = "S" + sid + ". " + s.getAttribute("data-title");
    document.title = "S" + sid + ". " + s.getAttribute("data-title") + " | 하네스 엔지니어링 워크샵";
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i === slides.length - 1;
    var notes = s.querySelector(".notes");
    notesBody.innerHTML = notes ? notes.innerHTML : "";
    notesBody.scrollTop = 0;
    if (updateHash !== false && window.history && window.history.replaceState) {
      window.history.replaceState(null, "", "#s" + sid);
    }
  }

  function setNotes(open) {
    panel.hidden = !open;
    deck.classList.toggle("notes-open", open);
    toggle.setAttribute("aria-pressed", open ? "true" : "false");
  }

  function next() { show(current + 1); }
  function prev() { show(current - 1); }

  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);
  toggle.addEventListener("click", function () { setNotes(panel.hidden); });
  document.getElementById("notes-close").addEventListener("click", function () { setNotes(false); });

  document.addEventListener("keydown", function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    switch (e.key) {
      case "ArrowRight": case "ArrowDown": case "PageDown": case " ":
        e.preventDefault(); next(); break;
      case "ArrowLeft": case "ArrowUp": case "PageUp":
        e.preventDefault(); prev(); break;
      case "Home": e.preventDefault(); show(0); break;
      case "End": e.preventDefault(); show(slides.length - 1); break;
      case "n": case "N": setNotes(panel.hidden); break;
      case "f": case "F":
        if (document.fullscreenElement) { document.exitFullscreen(); }
        else if (document.documentElement.requestFullscreen) { document.documentElement.requestFullscreen(); }
        break;
    }
  });

  var touchX = null;
  document.getElementById("viewport").addEventListener("touchstart", function (e) {
    touchX = e.touches.length === 1 ? e.touches[0].clientX : null;
  }, { passive: true });
  document.getElementById("viewport").addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) { if (dx < 0) next(); else prev(); }
    touchX = null;
  });

  window.addEventListener("hashchange", function () { show(indexFromHash(), false); });

  var params = new URLSearchParams(window.location.search);
  setNotes(params.get("notes") === "1");
  show(indexFromHash());
})();
