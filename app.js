(() => {
  "use strict";
  const data = JSON.parse(document.getElementById("data").textContent);
  const slides = [...document.querySelectorAll(".slide")];
  const sections = [...document.querySelectorAll(".sd-sec")];
  const listItems = [...document.querySelectorAll(".sd-sec li")];
  const deck = document.querySelector(".deck");
  const stage = document.querySelector(".slides");
  const footer = document.querySelector(".foot");
  const progress = document.querySelector(".segs");
  const total = slides.length;
  let state = {};
  try { state = JSON.parse(localStorage.getItem(data.key)) || {}; } catch (_) { state = {}; }
  state.seen ||= {};
  const save = () => { try { localStorage.setItem(data.key, JSON.stringify(state)); } catch (_) {} };
  const groups = {};

  data.slides.forEach((slide, i) => {
    if (!groups[slide.sec]) {
      groups[slide.sec] = document.createElement("div");
      groups[slide.sec].className = "g";
      progress.appendChild(groups[slide.sec]);
    }
    const button = document.createElement("button");
    button.type = "button";
    button.title = (i + 1) + ". " + slide.title;
    button.setAttribute("aria-label", "Слайд " + (i + 1) + ": " + slide.title);
    button.addEventListener("click", () => go(i));
    groups[slide.sec].appendChild(button);
    groups[slide.sec].style.setProperty("--n", groups[slide.sec].children.length);
  });
  const progressButtons = [...progress.querySelectorAll("button")];
  let current = -1, seenTimer = null;

  function paintProgress() {
    const seen = data.slides.filter(slide => state.seen[slide.id]).length;
    document.querySelector(".prog .n").textContent = seen;
    document.querySelector(".prog .t").textContent = total;
    progressButtons.forEach((button, i) => {
      button.classList.toggle("seen", !!state.seen[data.slides[i].id]);
      button.classList.toggle("cur", i === current);
      if (i === current) button.setAttribute("aria-current", "step");
      else button.removeAttribute("aria-current");
    });
    listItems.forEach(li => {
      const i = Number(li.dataset.go);
      li.classList.toggle("seen", !!state.seen[data.slides[i].id]);
      li.classList.toggle("cur", i === current);
    });
    sections.forEach(section => {
      const k = Number(section.dataset.sec);
      const items = data.slides.filter(slide => slide.sec === k);
      const marked = items.filter(slide => state.seen[slide.id]).length;
      section.querySelector(".c").textContent = marked + "/" + items.length;
      section.classList.toggle("cur", current >= 0 && data.slides[current].sec === k);
      section.querySelector(".sd-h").setAttribute("aria-expanded", String(section.classList.contains("open")));
    });
    const toggle = document.querySelector(".seen-t");
    const marked = current >= 0 && !!state.seen[data.slides[current].id];
    toggle.classList.toggle("on", marked);
    toggle.querySelector("span").textContent = marked ? "Просмотрено" : "Отметить просмотренным";
  }

  function fitStage() {
    if (window.matchMedia("(max-width:820px)").matches) {
      stage.style.removeProperty("width");
      stage.style.removeProperty("height");
      footer.style.removeProperty("width");
      return;
    }
    const showing = document.body.classList.contains("presenting");
    const availableWidth = Math.max(1, deck.clientWidth - (showing ? 0 : 44));
    const availableHeight = Math.max(1, deck.clientHeight - (showing ? 0 : footer.offsetHeight + 42));
    const width = Math.floor(Math.min(availableWidth, availableHeight * 16 / 9));
    stage.style.width = width + "px";
    stage.style.height = Math.floor(width * 9 / 16) + "px";
    footer.style.width = width + "px";
  }

  function go(index, first = false) {
    index = Math.max(0, Math.min(total - 1, index));
    if (index === current && !first) return;
    if (current >= 0) {
      slides[current].classList.remove("is-active");
      slides[current].setAttribute("aria-hidden", "true");
    }
    current = index;
    slides[index].classList.add("is-active");
    slides[index].setAttribute("aria-hidden", "false");
    slides[index].querySelector(".txt").scrollTop = 0;
    const meta = data.slides[index];
    const crumb = document.querySelector(".crumb");
    crumb.textContent = "";
    const b = document.createElement("b");
    b.textContent = data.secs[meta.sec];
    crumb.appendChild(b);
    document.querySelector(".foot .cnt").textContent = (index + 1) + " / " + total;
    const section = sections.find(x => Number(x.dataset.sec) === meta.sec);
    if (section) section.classList.add("open");
    if (!first && !document.body.classList.contains("presenting")) {
      listItems[index]?.scrollIntoView({block:"nearest"});
    }
    clearTimeout(seenTimer);
    seenTimer = setTimeout(() => { state.seen[meta.id] = 1; save(); paintProgress(); }, 2500);
    state.last = index;
    save();
    if (location.hash !== "#" + (index + 1)) history.replaceState(null, "", "#" + (index + 1));
    paintProgress();
    requestAnimationFrame(fitStage);
  }

  listItems.forEach(item => {
    item.addEventListener("click", () => { go(Number(item.dataset.go)); document.body.classList.remove("side-open"); });
    item.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        item.click();
      }
    });
  });
  sections.forEach(section => section.querySelector(".sd-h").addEventListener("click", () => {
    section.classList.toggle("open");
    paintProgress();
  }));
  document.querySelector(".menu").addEventListener("click", () => document.body.classList.toggle("side-open"));
  document.querySelector(".scrim").addEventListener("click", () => document.body.classList.remove("side-open"));
  document.querySelector(".sd-reset").addEventListener("click", () => {
    if (confirm("Сбросить отметки «просмотрено»?")) { state.seen = {}; save(); paintProgress(); }
  });
  document.querySelector(".prev").addEventListener("click", () => go(current - 1));
  document.querySelector(".next").addEventListener("click", () => go(current + 1));
  document.querySelector(".seen-t").addEventListener("click", () => {
    const id = data.slides[current].id;
    clearTimeout(seenTimer);
    if (state.seen[id]) delete state.seen[id]; else state.seen[id] = 1;
    save();
    paintProgress();
  });
  document.querySelector(".present").addEventListener("click", async () => {
    try { await document.documentElement.requestFullscreen(); }
    catch (_) { document.body.classList.toggle("presenting"); fitStage(); }
  });
  document.querySelector(".end-present").addEventListener("click", async () => {
    if (document.fullscreenElement) await document.exitFullscreen();
    else { document.body.classList.remove("presenting"); fitStage(); }
  });
  document.addEventListener("fullscreenchange", () => {
    document.body.classList.toggle("presenting", !!document.fullscreenElement);
    fitStage();
  });
  document.addEventListener("keydown", event => {
    if (event.target.closest("input,textarea,select,[contenteditable],.owner-dashboard button")) return;
    if (["ArrowRight","PageDown"," "].includes(event.key)) { event.preventDefault(); go(current + 1); }
    else if (["ArrowLeft","PageUp"].includes(event.key)) { event.preventDefault(); go(current - 1); }
    else if (event.key === "Home") go(0);
    else if (event.key === "End") go(total - 1);
    else if (event.key === "Escape" && document.body.classList.contains("presenting") && !document.fullscreenElement) {
      document.body.classList.remove("presenting"); fitStage();
    }
  });
  let touchX = null;
  stage.addEventListener("touchstart", event => {
    // На телефоне широкие графики прокручиваются, не перелистывая слайд.
    const chart = event.target.closest(".effort,.od-chart,.od-finance-chart,.od-ticket-chart,.od-cumulative-chart,.od-structure-chart");
    touchX = chart && chart.scrollWidth > chart.clientWidth ? null : event.changedTouches[0].clientX;
  }, {passive:true});
  stage.addEventListener("touchend", event => {
    if (touchX === null) return;
    const delta = event.changedTouches[0].clientX - touchX;
    touchX = null;
    if (Math.abs(delta) > 60) go(current + (delta < 0 ? 1 : -1));
  }, {passive:true});
  window.addEventListener("hashchange", () => {
    const number = Number.parseInt(location.hash.slice(1), 10);
    if (number >= 1 && number <= total) go(number - 1);
  });
  window.addEventListener("resize", fitStage);
  slides.forEach(slide => slide.setAttribute("aria-hidden", "true"));
  const requested = Number.parseInt(location.hash.slice(1), 10);
  go(requested >= 1 && requested <= total ? requested - 1 : (Number(state.last) || 0), true);
  window.addEventListener("load", fitStage);
})();
