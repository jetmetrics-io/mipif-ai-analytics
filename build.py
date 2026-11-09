#!/usr/bin/env python3
"""Собрать автономную HTML-презентацию из текста, стилей и шрифтов."""
from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

from story import SECTIONS, SLIDES

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
e = html.escape


def icon(name: str) -> str:
    text = (ASSETS / "icons" / (name + ".svg")).read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
    text = re.sub(r"<svg[^>]*>", lambda m: re.sub(r'\s(width|height|class)="[^"]*"', "", m.group()), text, count=1)
    text = re.sub(r"[ \t]+(?=\n)", "", text)
    return text.replace('stroke-width="2"', 'stroke-width="1.75"').replace("<svg", '<svg class="ic" aria-hidden="true"', 1)


def chip(name: str, tone: str = "good") -> str:
    return f'<span class="ichip tone-{tone}">{icon(name)}</span>'


def cards(items: list[tuple[str, str, str, str]], cols: int = 0) -> str:
    out = []
    for i, (title, subtitle, pic, tone) in enumerate(items):
        extra = '<div class="x">' + e(subtitle) + '</div>' if subtitle else ""
        out.append(
            f'<div class="sc-card tone-{tone} anim" style="--d:{.12 + i * .10:.2f}s">'
            f'{chip(pic, tone) if pic else ""}<div class="t">{e(title)}</div>'
            f'{extra}</div>'
        )
    return f'<div class="sc sc-cards n{cols or len(items)}">{"".join(out)}</div>'


def steps(items: list[tuple[str, str, str]], arrows: bool = True) -> str:
    out = []
    for i, (title, subtitle, tone) in enumerate(items):
        extra = '<div class="x">' + e(subtitle) + '</div>' if subtitle else ""
        out.append(
            f'<div class="sc-step tone-{tone} anim" style="--d:{.12+i*.16:.2f}s">'
            f'<div class="n">{i+1}</div><div class="t">{e(title)}</div>'
            f'{extra}</div>'
        )
        if arrows and i < len(items)-1:
            out.append(f'<div class="sc-arrow anim" style="--d:{.2+i*.16:.2f}s">{icon("arrow-right")}</div>')
    return f'<div class="sc sc-steps n{len(items)}">{"".join(out)}</div>'


def numbers(items: list[tuple[str, str, str]]) -> str:
    out = []
    for i, (value, label, tone) in enumerate(items):
        out.append(
            f'<div class="sc-num tone-{tone} anim" style="--d:{.1+i*.14:.2f}s">'
            f'<div class="v">{e(value)}</div><div class="x">{e(label)}</div></div>'
        )
    return f'<div class="sc sc-count n{len(items)}">{"".join(out)}</div>'


def b64_font(name: str) -> str:
    return base64.b64encode((ASSETS / "fonts" / name).read_bytes()).decode("ascii")


font_css = f"""
@font-face{{font-family:Onest;src:url(data:font/woff2;base64,{b64_font('Onest-variable.woff2')}) format('woff2');font-style:normal;font-weight:100 900;font-display:swap}}
@font-face{{font-family:'IBM Plex Mono';src:url(data:font/woff2;base64,{b64_font('IBMPlexMono-Regular.woff2')}) format('woff2');font-style:normal;font-weight:400;font-display:swap}}
@font-face{{font-family:'IBM Plex Mono';src:url(data:font/woff2;base64,{b64_font('IBMPlexMono-SemiBold.woff2')}) format('woff2');font-style:normal;font-weight:600;font-display:swap}}
"""
base_css = (ASSETS / "base.css").read_text(encoding="utf-8")
extra_css = (HERE / "overrides.css").read_text(encoding="utf-8")
js = (HERE / "app.js").read_text(encoding="utf-8")
dashboard_dir = ASSETS / "dashboard"
dashboard_css = (dashboard_dir / "dashboard.css").read_text(encoding="utf-8")
dashboard_js = (dashboard_dir / "dashboard.js").read_text(encoding="utf-8")
dashboard_sources = "\n".join(
    f'<script type="application/json" id="od-source-{name}">'
    + json.dumps(json.loads((dashboard_dir / (name + ".json")).read_text(encoding="utf-8")), ensure_ascii=False).replace("</", "<\\/")
    + '</script>'
    for name in ("crm", "ddu", "escrow", "inventory", "plans")
)
logo = (ASSETS / "jetmetrics.svg").read_text(encoding="utf-8")

parts = []
for i, sl in enumerate(SLIDES):
    kind = sl.get("type", "info")
    if kind == "cover":
        content = (
            f'<div class="cover-brand">{logo}</div><div class="cover-kicker">АНАЛИТИКА ДЕВЕЛОПЕРА · ИИ</div>'
            f'<h1>{e(sl["title"])}</h1>'
            f'<p class="cover-lead">{e(sl["lead"])}</p>'
        )
    else:
        eyebrow = f'<div class="eyebrow"><span class="sec">{e(SECTIONS[sl["sec"]])}</span></div>'
        content = eyebrow + f'<h2>{e(sl["title"])}</h2><p class="lead">{e(sl["lead"])}</p>'
    parts.append(
        f'<section class="slide t-{kind}" data-i="{i}" aria-label="Слайд {i+1}: {e(sl["title"])}">'
        f'<div class="txt">{content}</div><div class="vis v-schema"><div class="sc-wrap">{sl["visual"]}</div></div></section>'
    )

side = []
for k, label in enumerate(SECTIONS):
    side.append(
        f'<div class="sd-sec" data-sec="{k}"><button class="sd-h" aria-expanded="false">'
        f'<span class="t">{e(label)}</span><span class="c" data-c="{k}"></span></button><ol>'
        + "".join(
            f'<li data-go="{i}" tabindex="0"><i></i><span>{e(sl["title"])}</span></li>'
            for i, sl in enumerate(SLIDES) if sl["sec"] == k
        )
        + '</ol></div>'
    )

data = json.dumps(
    {"slides": [{"id": f"s{i+1:02}", "title": s["title"], "sec": s["sec"]} for i, s in enumerate(SLIDES)],
     "secs": SECTIONS, "key": "mipif-analytics-deck-v2"},
    ensure_ascii=False
).replace("</", "<\\/")

page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#F6F8FA">
<title>ИИ в аналитике и отчётности девелопера · JetMetrics</title>
<style>{font_css}\n{base_css}\n{extra_css}\n{dashboard_css}</style>
</head>
<body class="client">
<div class="app">
  <header class="top">
    <button class="ibtn menu" type="button" aria-label="Разделы">{icon("menu")}Разделы</button>
    <div class="brand">{logo}</div><div class="crumb"></div>
    <div class="prog"><span class="lbl">Просмотрено</span> <b class="n">0</b> из <span class="t">15</span> <span class="pl">пунктов</span></div>
    <button class="ibtn present" type="button" aria-label="Режим показа">Показ</button>
  </header>
  <div class="segs" aria-label="Прогресс по слайдам"></div>
  <div class="main">
    <aside class="side">{"".join(side)}<button class="sd-reset" type="button">Сбросить отметки «просмотрено»</button></aside>
    <div class="scrim"></div>
    <main class="deck">
      <div class="slides">{"".join(parts)}</div>
      <div class="foot">
        <button class="ibtn prev" type="button">{icon("arrow-left")}Назад</button>
        <span class="cnt" aria-live="polite"></span>
        <button class="ibtn next" type="button">Далее{icon("arrow-right")}</button>
        <span class="sp"></span><span class="kb">← → на клавиатуре</span>
        <button class="ibtn seen-t" type="button">{icon("check")}<span>Отметить просмотренным</span></button>
        <button class="ibtn end-present" type="button">Выйти из показа</button>
      </div>
    </main>
  </div>
</div>
<script type="application/json" id="data">{data}</script>
{dashboard_sources}
<script>{js}</script>
<script>{dashboard_js}</script>
</body></html>
"""
assert len(SLIDES) == 15
(HERE / "index.html").write_text(page, encoding="utf-8")
print(f"index.html: {len(SLIDES)} слайдов, {len(page.encode('utf-8')):,} байт")
