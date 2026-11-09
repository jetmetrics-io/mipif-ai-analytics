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
  const decimal = new Intl.NumberFormat("ru-RU", {maximumFractionDigits: 2});
  const fmt = value => number.format(value);
  const fmt2 = value => decimal.format(value);
  const el = name => root.querySelector('[data-od="' + name + '"]');
  const put = (name, value) => { el(name).textContent = value; };
  const period = () => Number(periodSelect.value);
  const picked = () => projectSelect.value === "all" ? projects : [projectSelect.value];
  const sum = (source, field, index, ids = picked()) => ids.reduce((total, id) => {
    const val = source.projects[id][field];
    return total + (Array.isArray(val) ? val[index] : val);
  }, 0);
  const series = (source, field, ids) => months.map((_, i) => sum(source, field, i, ids));

  function smallLine(values) {
    const min = Math.min(...values), max = Math.max(...values), range = max - min || 1;
    const points = values.map((v, i) => `${2+i*15.2},${23-(v-min)/range*19}`).join(" ");
    return `<svg viewBox="0 0 80 26" preserveAspectRatio="none" aria-hidden="true"><polyline points="${points}" fill="none" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>`;
  }

  function lineGraph(values, selected, suffix) {
    const w=400, left=47, right=388, top=12, bottom=95;
    const min = Math.min(...values), max = Math.max(...values), range = max - min || 1;
    const points = values.map((v,i) => [left+i*(right-left)/5, bottom-(v-min)/range*(bottom-top-12)-6]);
    const path = points.map(([x,y]) => `${x},${y}`).join(" ");
    let body = `<line class="od-chart-grid" x1="${left}" y1="${bottom}" x2="${right}" y2="${bottom}"/><line class="od-chart-grid" x1="${left}" y1="${top+24}" x2="${right}" y2="${top+24}"/><text x="${left-5}" y="${top+10}" text-anchor="end">${fmt2(max)}</text><text x="${left-5}" y="${bottom-2}" text-anchor="end">${fmt2(min)}</text>`;
    body += `<polyline points="${path}" fill="none" stroke="var(--jm-green)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>`;
    points.forEach(([x,y],i) => {
      body += `<circle cx="${x}" cy="${y}" r="${i===selected ? 5 : 3}" fill="${i===selected ? 'var(--jm-green-deep)' : 'var(--jm-green)'}" stroke="white" stroke-width="2"/>`;
      body += `<text x="${x}" y="116" text-anchor="middle">${months[i].toUpperCase()}</text>`;
    });
    const desc=months.map((m,i)=>`${m}: ${fmt2(values[i])}${suffix}`).join('; ');
    return `<svg role="img" aria-label="${desc}" viewBox="0 0 ${w} 122" preserveAspectRatio="none">${body}</svg>`;
  }

  function donut(parts, description) {
    const total=parts.reduce((n,p)=>n+p[1],0), r=39, circumference=2*Math.PI*r;
    let offset=0;
    const rings=parts.map(([,value,color])=>{
      const length=total ? value/total*circumference : 0;
      const circle=`<circle cx="50" cy="50" r="${r}" fill="none" stroke="${color}" stroke-width="13" stroke-dasharray="${length} ${circumference-length}" stroke-dashoffset="${-offset}" transform="rotate(-90 50 50)"/>`;
      offset+=length; return circle;
    }).join('');
    return `<svg role="img" aria-label="${description}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="${r}" fill="none" stroke="#edf2ef" stroke-width="13"/>${rings}<circle cx="50" cy="50" r="28" fill="white"/></svg>`;
  }

  function drawChart(ids, selected) {
    const fact=series(data.ddu,"registered",ids), plan=series(data.plan,"registered_ddu",ids);
    const peak=Math.max(10,Math.ceil(Math.max(...fact,...plan)/10)*10);
    const left=35, plotWidth=340, step=plotWidth/months.length, top=16, bottom=132, height=bottom-top;
    const y=v=>bottom-v/peak*height;
    let body=`<rect class="od-chart-active" x="${left+selected*step+2}" y="7" width="${step-4}" height="139" rx="7"/>`;
    for(const ratio of [0,.5,1]){const val=peak*ratio, yy=y(val);body+=`<line class="od-chart-grid" x1="${left}" y1="${yy}" x2="375" y2="${yy}"/><text x="28" y="${yy+3}" text-anchor="end">${fmt(val)}</text>`;}
    for(let i=0;i<months.length;i++){
      const x=left+i*step+step/2, fy=y(fact[i]), py=y(plan[i]);
      body+=`<rect class="od-chart-plan" x="${x+3}" y="${py}" width="12" height="${bottom-py}" rx="3"/><rect class="od-chart-fact" x="${x-14}" y="${fy}" width="12" height="${bottom-fy}" rx="3"/>`;
      body+=`<text class="od-chart-number" x="${x-8}" y="${Math.max(10,fy-4)}" text-anchor="middle">${fmt(fact[i])}</text><text x="${x}" y="158" text-anchor="middle">${months[i].toUpperCase()}</text>`;
    }
    const details=months.map((m,i)=>`${m}: ${fact[i]} ДДУ, план ${plan[i]}`).join('; ');
    el("chart").innerHTML=`<svg role="img" aria-label="План и факт регистраций ДДУ, ${details}" viewBox="0 0 400 165" preserveAspectRatio="none">${body}</svg>`;
    put("six-month-deals",fmt(fact.reduce((a,b)=>a+b,0))+' ДДУ');
    put("six-month-plan",'план '+fmt(plan.reduce((a,b)=>a+b,0)));
  }

  function drawProjects(ids, i) {
    const rows=ids.map(id=>{
      const actual=sum(data.ddu,"registered",i,[id]), planned=sum(data.plan,"registered_ddu",i,[id]);
      const pct=planned?actual/planned*100:0, width=Math.max(0,Math.min(100,pct));
      return `<div class="od-project-row"><span class="od-project-row-name">Проект ${id}</span><span class="od-project-row-num">${fmt(actual)} <small>/ ${fmt(planned)} · ${fmt(pct)}%</small></span><div class="od-project-track" aria-label="Проект ${id}: выполнение плана ${fmt(pct)} процентов"><i class="${pct<90?'short':''}" style="width:${width}%"></i></div></div>`;
    });
    el("project-rows").innerHTML=rows.join('');
    put("project-total",`${fmt(sum(data.ddu,"registered",i,ids))} / ${fmt(sum(data.plan,"registered_ddu",i,ids))} ДДУ`);
  }

  function drawStock(ids) {
    const total=sum(data.stock,"total",null,ids), sold=sum(data.stock,"sold",null,ids);
    const available=sum(data.stock,"available",null,ids), reserved=sum(data.stock,"reserved",null,ids);
    const other=sum(data.stock,"awaiting_registration",null,ids)+sum(data.stock,"not_released",null,ids);
    const parts=[["Проданы",sold,"var(--jm-blue)"],["Доступны",available,"var(--jm-green)"],["Бронь",reserved,"var(--jm-yellow)"],["Прочее",other,"var(--jm-chart-compare)"]];
    const desc=parts.map(([name,value])=>`${name}: ${fmt(value)}`).join(', ');
    put("stock-total",fmt(total));put("stock-available",fmt(available));put("inventory-note",`на 31.10 · из ${fmt(total)}`);
    el("stock-donut").innerHTML=donut(parts,desc);
    el("stock-mini").innerHTML=`<i style="width:${total?available/total*100:0}%"></i>`;
    el("stock-bar").innerHTML=parts.map(([,value,color])=>`<i style="width:${total?value/total*100:0}%;background:${color}"></i>`).join('');
    el("stock-legend").innerHTML=parts.map(([name,value,color])=>`<span><i style="background:${color}"></i>${name} <b>${fmt(value)}</b></span>`).join('');
    el("stock-bar").setAttribute("aria-label",desc);
  }

  function drawFunds(ids, selected) {
    const contracts=series(data.ddu,"contract_mln",ids), cash=series(data.bank,"receipts_mln",ids);
    const peak=Math.max(10,Math.ceil(Math.max(...contracts,...cash)/100)*100);
    const left=35, plotWidth=340, step=plotWidth/6, top=16, bottom=132, y=v=>bottom-v/peak*(bottom-top);
    let body=`<rect class="od-chart-active" x="${left+selected*step+2}" y="7" width="${step-4}" height="139" rx="7"/>`;
    for(const ratio of [0,.5,1]){const yy=y(peak*ratio);body+=`<line class="od-chart-grid" x1="${left}" y1="${yy}" x2="375" y2="${yy}"/><text x="28" y="${yy+3}" text-anchor="end">${fmt(peak*ratio)}</text>`;}
    months.forEach((month,i)=>{const x=left+i*step+step/2, ay=y(contracts[i]), by=y(cash[i]);body+=`<rect class="od-finance-contract" x="${x-14}" y="${ay}" width="12" height="${bottom-ay}" rx="3"/><rect class="od-finance-escrow" x="${x+3}" y="${by}" width="12" height="${bottom-by}" rx="3"/><text x="${x}" y="158" text-anchor="middle">${month.toUpperCase()}</text>`;});
    const desc=months.map((m,i)=>`${m}: ДДУ ${fmt(contracts[i])}, эскроу ${fmt(cash[i])} млн рублей`).join('; ');
    el("funds-chart").innerHTML=`<svg role="img" aria-label="${desc}" viewBox="0 0 400 165" preserveAspectRatio="none">${body}</svg>`;
  }

  function drawHeatmap(selected) {
    const max=Math.max(...projects.flatMap(id=>data.ddu.projects[id].registered));
    let out='<span></span>'+months.map(m=>`<span>${m.toUpperCase()}</span>`).join('');
    projects.forEach(id=>{
      out+=`<span class="heat-name">${id}</span>`;
      data.ddu.projects[id].registered.forEach((value,i)=>{
        const opacity=.1+.65*value/max;
        const isSelected=i===selected&&(projectSelect.value==='all'||projectSelect.value===id);
        out+=`<button type="button" data-project-id="${id}" data-month-index="${i}" class="${isSelected?'selected':''}" style="background:rgba(14,156,125,${opacity})" aria-label="Проект ${id}, ${months[i]}: ${value} ДДУ. Выбрать">${value}</button>`;
      });
    });
    el("heatmap").innerHTML=out;
  }

  function drawChannel(own, agency) {
    const total=own+agency, pct=total?agency/total*100:0;
    const parts=[["Собственный",own,"var(--jm-green)"],["Агентский",agency,"var(--jm-blue)"]];
    put("channel-total",fmt(total));put("channel-agency-pct",fmt(pct)+'%');put("channel-own",fmt(own));put("channel-agency",fmt(agency));
    el("channel-donut").innerHTML=donut(parts,`Собственный вход ${fmt(own)}, агентский ${fmt(agency)} обращений`);
  }

  function drawCumulative(ids, selected) {
    const cumulative=values=>{let total=0;return values.map(value=>(total+=value));};
    const actual=cumulative(series(data.ddu,'registered',ids)), plan=cumulative(series(data.plan,'registered_ddu',ids));
    const max=Math.max(...actual,...plan,1), left=28, right=382, top=12, bottom=115;
    const points=values=>values.map((v,i)=>[left+i*(right-left)/5,bottom-v/max*(bottom-top)]);
    const a=points(actual), b=points(plan), coords=arr=>arr.map(([x,y])=>`${x},${y}`).join(' ');
    let body=`<line class="od-chart-grid" x1="${left}" y1="${bottom}" x2="${right}" y2="${bottom}"/><line class="od-chart-grid" x1="${left}" y1="${(top+bottom)/2}" x2="${right}" y2="${(top+bottom)/2}"/><text x="${left-5}" y="${top+5}" text-anchor="end">${fmt(max)}</text><text x="${left-5}" y="${bottom}" text-anchor="end">0</text>`;
    body+=`<polyline points="${coords(b)}" fill="none" stroke="var(--jm-chart-compare)" stroke-width="3"/><polyline points="${coords(a)}" fill="none" stroke="var(--jm-green)" stroke-width="3"/>`;
    a.forEach(([x,y],i)=>{body+=`<circle cx="${x}" cy="${y}" r="${i===selected?5:3}" fill="var(--jm-green)"/><text x="${x}" y="139" text-anchor="middle">${months[i].toUpperCase()}</text>`;});
    const desc=months.map((m,i)=>`${m}: факт ${fmt(actual[i])}, план ${fmt(plan[i])}`).join('; ');
    el('cumulative-chart').innerHTML=`<svg role="img" aria-label="Накопленные ДДУ: ${desc}" viewBox="0 0 400 145" preserveAspectRatio="none">${body}</svg>`;
  }

  function drawStructure(ids) {
    const colors={'А':'var(--jm-green)','Б':'var(--jm-blue)','В':'var(--jm-purple)'};
    const totals=months.map((_,i)=>sum(data.ddu,'registered',i,ids)), max=Math.max(...totals,1);
    const left=28, step=354/6, bottom=120, height=100;
    let body=`<line class="od-chart-grid" x1="${left}" y1="${bottom}" x2="382" y2="${bottom}"/><text x="${left-5}" y="${bottom-height+5}" text-anchor="end">${fmt(max)}</text><text x="${left-5}" y="${bottom}" text-anchor="end">0</text>`;
    months.forEach((month,i)=>{
      const x=left+i*step+step/2;let y=bottom;
      ids.forEach(id=>{const value=data.ddu.projects[id].registered[i], h=value/max*height;y-=h;body+=`<rect x="${x-12}" y="${y}" width="24" height="${h}" fill="${colors[id]}"/>`;});
      body+=`<text x="${x}" y="140" text-anchor="middle">${month.toUpperCase()}</text>`;
    });
    const desc=months.map((m,i)=>`${m}: ${fmt(totals[i])} ДДУ`).join('; ');
    el('structure-chart').innerHTML=`<svg role="img" aria-label="Регистрации по проектам, ${desc}" viewBox="0 0 400 145" preserveAspectRatio="none">${body}</svg>`;
  }

  function drawCashProjects(ids, i) {
    const values=ids.map(id=>sum(data.bank,'receipts_mln',i,[id])), peak=Math.max(...values,1);
    el('cash-rows').innerHTML=ids.map((id,k)=>`<div class="od-cash-row"><span>Проект ${id}</span><b>${fmt(values[k])}</b><div class="od-cash-track"><i style="width:${values[k]/peak*100}%"></i></div></div>`).join('');
    put('cash-total',fmt(values.reduce((a,b)=>a+b,0))+' млн ₽');
  }

  function drawStockTable(ids) {
    let out='<span></span><span class="head">ПРОД.</span><span class="head">СВОБ.</span><span class="head">БРОНЬ</span><span class="head">ПРОЧ.</span>';
    ids.forEach(id=>{const s=data.stock.projects[id], other=s.awaiting_registration+s.not_released;out+=`<span class="name">${id}</span><span class="value">${fmt(s.sold)}</span><span class="value">${fmt(s.available)}</span><span class="value">${fmt(s.reserved)}</span><span class="value">${fmt(other)}</span>`;});
    el('stock-table').innerHTML=out;
  }

  function render() {
    const ids=picked(), i=period();
    put("period-label",periodSelect.selectedOptions[0].textContent.toLocaleLowerCase('ru-RU'));
    const fact=sum(data.ddu,"registered",i,ids), plan=sum(data.plan,"registered_ddu",i,ids), diff=fact-plan;
    const contracts=sum(data.ddu,"contract_mln",i,ids), escrow=sum(data.bank,"receipts_mln",i,ids);
    const own=sum(data.crm,"own",i,ids), agency=sum(data.crm,"agency",i,ids), leads=own+agency;
    const bookings=sum(data.crm,"bookings",i,ids), avg=fact?contracts/fact:0;
    put("deals",fmt(fact));const note=el("deal-note");note.textContent=diff===0?'На уровне плана':`${diff<0?'−':'+'}${fmt(Math.abs(diff))} ДДУ к плану`;note.className='od-kpi-note '+(diff<0?'negative':'positive');
    put("fulfilment",plan?fmt(fact/plan*100)+'%':'—');put("plan-note",`план ${fmt(plan)} ДДУ`);
    put("contracts",fmt(contracts));put("avg-price",fact?fmt2(avg):'—');put("escrow",fmt(escrow));
    put("available",fmt(sum(data.stock,"available",null,ids)));put("leads",fmt(leads));put("bookings",fmt(bookings));
    put("activity-leads",fmt(leads));put("meetings",fmt(sum(data.crm,"meetings",i,ids)));put("activity-bookings",fmt(bookings));put("own",fmt(own));put("agency",fmt(agency));
    el("own-bar").style.width=(leads?own/leads*100:0)+'%';el("agency-bar").style.width=(leads?agency/leads*100:0)+'%';
    const factSeries=series(data.ddu,'registered',ids), planSeries=series(data.plan,'registered_ddu',ids);
    const moneySeries=series(data.ddu,'contract_mln',ids), escrowSeries=series(data.bank,'receipts_mln',ids);
    const leadsSeries=months.map((_,n)=>sum(data.crm,'own',n,ids)+sum(data.crm,'agency',n,ids));
    const bookingsSeries=series(data.crm,'bookings',ids), avgSeries=factSeries.map((n,k)=>n?moneySeries[k]/n:0);
    const sparkData={deals:factSeries,fulfilment:factSeries.map((n,k)=>planSeries[k]?n/planSeries[k]*100:0),contracts:moneySeries,'avg-price':avgSeries,escrow:escrowSeries,leads:leadsSeries,bookings:bookingsSeries};
    Object.entries(sparkData).forEach(([key,values])=>{root.querySelector('[data-spark="'+key+'"]').innerHTML=smallLine(values);});
    put('ticket-value',fact?fmt2(avg):'—');
    const change=el('ticket-change');
    if(i>0&&avgSeries[i-1]){const d=(avg/avgSeries[i-1]-1)*100, rounded=Math.round(Math.abs(d)*10)/10;change.textContent=`${rounded===0?'':d<0?'−':'+'}${fmt(rounded)}% к пред. мес.`;change.className='';}
    else{change.textContent='';change.className='';}
    el('ticket-chart').innerHTML=lineGraph(avgSeries,i,' млн ₽');
    el('activity-spark').innerHTML=lineGraph(leadsSeries,i,' обращений');
    drawChart(ids,i);drawProjects(ids,i);drawStock(ids);drawFunds(ids,i);drawHeatmap(i);drawChannel(own,agency);
    drawCumulative(ids,i);drawStructure(ids);drawCashProjects(ids,i);drawStockTable(ids);
  }

  projectSelect.addEventListener('change',render);
  periodSelect.addEventListener('change',render);
  el('heatmap').addEventListener('click',event=>{
    const cell=event.target.closest('button[data-project-id]');
    if(!cell)return;
    projectSelect.value=cell.dataset.projectId;periodSelect.value=cell.dataset.monthIndex;render();
  });
  render();
})();
