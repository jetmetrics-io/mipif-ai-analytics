(() => {
  "use strict";
  const root = document.querySelector(".owner-dashboard");
  if (!root) return;
  const readSource = id => JSON.parse(document.getElementById("od-source-" + id).textContent);
  const data = {
    crm: readSource("crm"), ddu: readSource("ddu"), bank: readSource("escrow"),
    stock: readSource("inventory"), plan: readSource("plans")
  };
  const projects = ["А", "Б", "В"];
  const months = ["май", "июн", "июл", "авг", "сен", "окт"];
  const projectSelect = root.querySelector(".od-project");
  const periodSelect = root.querySelector(".od-period");
  const number = new Intl.NumberFormat("ru-RU", {maximumFractionDigits: 1});
  const fmt = value => number.format(value);
  const el = name => root.querySelector('[data-od="' + name + '"]');
  const put = (name, value) => { el(name).textContent = value; };
  const period = () => Number(periodSelect.value);
  const picked = () => projectSelect.value === "all" ? projects : [projectSelect.value];
  const sum = (source, field, index, ids = picked()) => ids.reduce((total, id) => {
    const val = source.projects[id][field];
    return total + (Array.isArray(val) ? val[index] : val);
  }, 0);

  function drawChart(ids, selected) {
    const fact = months.map((_, i) => sum(data.ddu, "registered", i, ids));
    const plan = months.map((_, i) => sum(data.plan, "registered_ddu", i, ids));
    const peak = Math.max(10, Math.ceil(Math.max(...fact, ...plan) / 10) * 10);
    const left = 46, plotWidth = 650, step = plotWidth / months.length;
    const top = 18, bottom = 164, plotHeight = bottom - top;
    const y = value => bottom - value / peak * plotHeight;
    let body = `<rect class="od-chart-active" x="${left + selected * step + 4}" y="9" width="${step-8}" height="171" rx="10"/>`;
    for (const ratio of [0, .5, 1]) {
      const value = peak * ratio, yy = y(value);
      body += `<line class="od-chart-grid" x1="${left}" y1="${yy}" x2="696" y2="${yy}"/><text x="34" y="${yy + 4}" text-anchor="end">${fmt(value)}</text>`;
    }
    for (let i = 0; i < months.length; i++) {
      const x = left + i * step + step / 2;
      const fy = y(fact[i]), py = y(plan[i]);
      body += `<rect class="od-chart-plan" x="${x+4}" y="${py}" width="20" height="${bottom-py}" rx="4"/>`;
      body += `<rect class="od-chart-fact" x="${x-22}" y="${fy}" width="20" height="${bottom-fy}" rx="4"/>`;
      body += `<text class="od-chart-number" x="${x-12}" y="${Math.max(14, fy-5)}" text-anchor="middle">${fmt(fact[i])}</text>`;
      body += `<text x="${x}" y="188" text-anchor="middle">${months[i].toUpperCase()}</text>`;
    }
    const details = months.map((month, i) => `${month}: ${fact[i]} ДДУ, план ${plan[i]}`).join("; ");
    el("chart").innerHTML = `<svg role="img" aria-label="План и факт регистраций ДДУ, ${details}" viewBox="0 0 720 198" preserveAspectRatio="xMidYMid meet">${body}</svg>`;
  }

  function drawProjects(ids, i) {
    const rows = ids.map(id => {
      const actual = sum(data.ddu, "registered", i, [id]);
      const planned = sum(data.plan, "registered_ddu", i, [id]);
      const pct = planned ? actual / planned * 100 : 0;
      const width = Math.max(0, Math.min(100, pct));
      return `<div class="od-project-row"><span class="od-project-row-name">Проект ${id}</span><span class="od-project-row-num">${fmt(actual)} <small>/ ${fmt(planned)} ДДУ</small></span><div class="od-project-track" aria-label="Проект ${id}: выполнение плана ${fmt(pct)} процентов"><i class="${pct < 90 ? "short" : ""}" style="width:${width}%"></i></div></div>`;
    });
    el("project-rows").innerHTML = rows.join("");
    put("project-total", `${fmt(sum(data.ddu, "registered", i, ids))} / ${fmt(sum(data.plan, "registered_ddu", i, ids))} ДДУ`);
  }

  function drawStock(ids) {
    const total = sum(data.stock, "total", null, ids);
    const sold = sum(data.stock, "sold", null, ids);
    const available = sum(data.stock, "available", null, ids);
    const reserved = sum(data.stock, "reserved", null, ids);
    const other = sum(data.stock, "awaiting_registration", null, ids) + sum(data.stock, "not_released", null, ids);
    const parts = [
      ["Проданы", sold, "var(--jm-blue)"], ["Доступны", available, "var(--jm-green)"],
      ["Бронь", reserved, "var(--jm-yellow)"], ["Прочее", other, "var(--jm-chart-compare)"]
    ];
    put("stock-total", fmt(total));
    put("stock-available", fmt(available));
    el("stock-bar").innerHTML = parts.map(([, value, color]) => `<i style="width:${total ? value/total*100 : 0}%;background:${color}"></i>`).join("");
    el("stock-legend").innerHTML = parts.map(([label, value, color]) => `<span><i style="background:${color}"></i>${label} <b>${fmt(value)}</b></span>`).join("");
    el("stock-bar").setAttribute("aria-label", parts.map(([label, value]) => `${label}: ${fmt(value)}`).join(", "));
    put("inventory-note", `на 31.10.2026 · из ${fmt(total)}`);
  }

  function render() {
    const ids = picked(), i = period();
    put("period-label", periodSelect.selectedOptions[0].textContent.toLocaleLowerCase("ru-RU"));
    const fact = sum(data.ddu, "registered", i, ids);
    const plan = sum(data.plan, "registered_ddu", i, ids);
    const difference = fact - plan;
    put("deals", fmt(fact));
    const note = el("deal-note");
    note.textContent = difference === 0 ? "На уровне плана" : `${difference < 0 ? "−" : "+"}${fmt(Math.abs(difference))} ДДУ к плану`;
    note.className = "od-kpi-note " + (difference < 0 ? "negative" : "positive");
    put("fulfilment", plan ? fmt(fact / plan * 100) + "%" : "—");
    put("plan-note", `план ${fmt(plan)} ДДУ`);
    put("contracts", fmt(sum(data.ddu, "contract_mln", i, ids)));
    put("escrow", fmt(sum(data.bank, "receipts_mln", i, ids)));
    put("available", fmt(sum(data.stock, "available", null, ids)));
    const own = sum(data.crm, "own", i, ids), agency = sum(data.crm, "agency", i, ids), leads = own + agency;
    put("leads", fmt(leads)); put("meetings", fmt(sum(data.crm, "meetings", i, ids))); put("bookings", fmt(sum(data.crm, "bookings", i, ids)));
    put("own", fmt(own)); put("agency", fmt(agency));
    el("own-bar").style.width = (leads ? own / leads * 100 : 0) + "%";
    el("agency-bar").style.width = (leads ? agency / leads * 100 : 0) + "%";
    drawChart(ids, i); drawProjects(ids, i); drawStock(ids);
  }

  projectSelect.addEventListener("change", render);
  periodSelect.addEventListener("change", render);
  render();
})();
