"""Содержание и редактируемые схемы доклада MIPIF."""
from __future__ import annotations

import base64
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
E = html.escape


def speaker() -> str:
    photo = base64.b64encode((HERE / 'assets' / 'dmitry.jpg').read_bytes()).decode('ascii')
    return (f'<div class="speaker-intro"><div class="speaker-card">'
            f'<img class="speaker-photo" src="data:image/jpeg;base64,{photo}" alt="Дмитрий Некрасов">'
            '<div><div class="speaker-name">Дмитрий Некрасов</div>'
            '<div class="speaker-role">Сооснователь JetMetrics</div>'
            '<div class="speaker-focus">Карты метрик, BI и обучение аналитике</div></div></div>'
            '<div class="speaker-proof"><b>19 000+</b><span>скачиваний карт метрик JetMetrics<br>в 131 стране</span></div></div>')


def dashboard() -> str:
    return (HERE / 'assets' / 'dashboard' / 'dashboard.html').read_text(encoding='utf-8')


LABELS = [
    ('Подключение', 'и сбор', 'данных'), ('Подготовка', 'данных'),
    ('Построение', 'графиков'), ('Создание', 'отчётности'),
    ('Определение', 'метрик'), ('Проверка', 'качества', 'данных'),
    ('Поиск', 'закономер-', 'ностей'), ('Проверка', 'выводов'),
    ('Осмысление', 'результатов'), ('Подготовка', 'решений'),
    ('Согласование', 'действий'),
]
BEFORE = (5, 4, 4, 5, 2, 2, 3, 1, 1, 1, 2)
NOW = (2, 3, 2, 2, 3, 4, 2, 4, 3, 5, 4)


def effort_chart(overlay: bool) -> str:
    xs = [64 + i * 107 for i in range(11)]
    def y(value: int) -> int:
        return 241 - (value - 1) * 47
    def series(vals: tuple[int, ...], klass: str) -> str:
        pts = ' '.join(f'{x},{y(v)}' for x, v in zip(xs, vals))
        marks = ''.join(f'<g class="{klass}"><circle cx="{x}" cy="{y(v)}" r="15"/>'
                        f'<text x="{x}" y="{y(v)+5}">{v}</text></g>'
                        for x, v in zip(xs, vals))
        return f'<polyline class="{klass} line" points="{pts}"/>{marks}'
    bands = ''.join(f'<rect x="{x-50}" y="37" width="100" height="219" class="band"/>'
                    for i, x in enumerate(xs) if i % 2 == 0)
    rules = ''.join(f'<line x1="{xs[0]}" y1="{y(v)}" x2="{xs[-1]}" y2="{y(v)}" class="rule"/>'
                    f'<text x="23" y="{y(v)+5}" class="axis">{v}</text>' for v in range(1, 6))
    captions = ''.join('<text x="%s" y="291" class="label">%s</text>' % (
        x, ''.join(f'<tspan x="{x}" dy="{0 if k == 0 else 19}">{E(line)}</tspan>'
                   for k, line in enumerate(label))) for x, label in zip(xs, LABELS))
    lines = series(BEFORE, 'before muted' if overlay else 'before')
    if overlay:
        lines += series(NOW, 'now')
    legend = ('<span><i class="dot old"></i>Раньше</span><span><i class="dot new"></i>Сейчас</span>'
              if overlay else '<span><i class="dot old"></i>Раньше</span>')
    return ('<div class="effort"><div class="effort-top"><span>УСИЛИЯ КОМАНДЫ · ОТ 1 ДО 5</span>'
            f'<div class="effort-legend">{legend}</div></div>'
            '<svg role="img" aria-label="Авторская оценка усилий по 11 видам аналитической работы" '
            'viewBox="0 0 1200 365" xmlns="http://www.w3.org/2000/svg">'
            f'{bands}{rules}{lines}{captions}</svg>'
            '<div class="effort-foot">Авторская оценка распределения усилий, не замер рынка · '
            '<a href="https://t.me/jetmetrics/499" target="_blank" rel="noopener">исходный пост</a></div></div>')


def ability() -> str:
    return '''<div class="ability-list">
      <div><span>01</span><b>Собрать</b><p>запрос, график, первый отчёт</p></div>
      <div><span>02</span><b>Найти</b><p>аномалии и расхождения в данных</p></div>
      <div><span>03</span><b>Объяснить</b><p>динамику и различия между срезами</p></div>
      <div><span>04</span><b>Предложить</b><p>гипотезы и способы их проверки</p></div>
      <div class="ability-note">Ответ и источники всё равно нужно проверять</div></div>'''


def evidence() -> str:
    return '''<div class="evidence">
      <div class="evidence-stat"><div class="evidence-over">DATA AGENT BENCHMARK · EMNLP 2026</div>
        <div class="evidence-big">57<span>%</span></div><div class="evidence-meaning">средняя точность за одну попытку</div>
        <p>GPT-5.5 + Codex · 104 запроса · 17 наборов данных · 5 запусков каждого запроса</p>
      </div>
      <div class="evidence-note"><b>Сложные задачи с несколькими источниками.</b><br>У агента были описания данных и подсказки.
        <div class="example-line"><span>ПРИМЕР ДЛЯ ДЕВЕЛОПЕРА</span><strong>Данные о ДДУ и отменах в разных системах</strong></div>
        <small>Результат зависит от задачи и настройки системы; это не оценка качества для вашей компании.</small>
      </div>
      <a class="source" href="https://aclanthology.org/2026.emnlp-main.1872/" target="_blank" rel="noopener">Ma et al., EMNLP 2026 ↗</a>
      </div>'''


def limitations() -> str:
    return '''<div class="limit-visual"><div class="limit-row"><div><b>Пропуск в CRM</b><span>ИИ может найти пустые поля.</span></div>
      <strong>Но факты нужно сверять с другими источниками.</strong></div>
      <div class="limit-row"><div><b>Падение продаж</b><span>ИИ может предложить объяснения.</span></div>
      <strong>Но совпадение ещё не доказывает причину.</strong></div>
      <div class="limit-row"><div><b>Решение руководителя</b><span>ИИ может сравнить варианты.</span></div>
      <strong>Но цели и допустимый риск нужно задать.</strong></div>
      <div class="limit-source">Неоднозначные вопросы требуют уточнений: <a href="https://arxiv.org/abs/2510.05318" target="_blank" rel="noopener">BIRD-INTERACT, ICLR 2026 ↗</a></div></div>'''


def layers() -> str:
    return '''<div class="layer-stack">
      <div class="layer-entry">ВОПРОС РУКОВОДИТЕЛЯ</div><div class="layer-arrow">↓</div>
      <div class="layer-row semantic"><b>Семантика</b><span>Что означают показатели?</span></div>
      <div class="layer-row causal"><b>Причинные связи</b><span>Как показатели связаны?</span></div>
      <div class="layer-row context"><b>Контекст</b><span>Что происходит в бизнесе?</span></div>
      <div class="layer-arrow">↓</div><div class="layer-base">ДАННЫЕ · ИСТОЧНИКИ · КАЧЕСТВО</div>
      </div>'''


def semantics() -> str:
    return '''<div class="definition-example"><div class="definition-head">«СКОЛЬКО МЫ ПРОДАЛИ?»</div>
      <div class="definition-pair"><div><b>120</b><strong>ДДУ зарегистрировано</strong><span>за период</span></div>
      <div class="definition-divider">≠</div><div><b>108</b><strong>из них действуют</strong><span>на дату отчёта</span></div></div>
      <div class="definition-note">Одна когорта договоров · разное определение показателя</div>
      <div class="example-tag">Условный пример</div></div>'''


def metric_tree() -> str:
    return '''<div class="tree-visual"><div class="tree-label">ОДНА КОГОРТА БРОНЕЙ</div>
      <div class="tree-root"><strong>ДДУ</strong><span>сколько дошло до договора</span></div>
      <div class="tree-stem"></div><div class="tree-branches"><div><strong>Брони</strong><span>сколько было</span></div>
      <em>×</em><div><strong>Конверсия в ДДУ</strong><span>доля дошедших до договора</span></div></div>
      <p>Дерево раскладывает показатель по определению.<br>Само по себе оно не доказывает причины.</p></div>'''


def causal() -> str:
    return '''<div class="causal-visual"><div class="causal-title">ЧТО МОГЛО ПОВЛИЯТЬ НА ПРОДАЖИ?</div>
      <div class="causal-grid"><div class="cause a">Цена</div><div class="cause b">Ипотека</div><div class="cause c">Ассортимент</div>
      <div class="cause-arrows" aria-hidden="true"><span>↓</span><span>↓</span><span>↓</span></div>
      <div class="causal-hub"><div>Обращения</div><span>→</span><div>Брони</div><span>→</span><div>ДДУ</div></div></div>
      <div class="causal-check"><b>Гипотеза</b> → данные и сравнение → <b>проверка</b></div>
      <p>Стрелка — предположение о влиянии, а не доказанный эффект.</p></div>'''


def context() -> str:
    return '''<div class="context-visual"><div class="context-question">Почему план не выполнен?</div><div class="context-grid">
      <div><span>01</span><b>Цель и приоритеты</b><p>Что компания пыталась изменить</p></div>
      <div><span>02</span><b>Решения и причины</b><p>Что решили и почему</p></div>
      <div><span>03</span><b>События и ограничения</b><p>Что изменилось по ходу периода</p></div>
      <div><span>04</span><b>Обсуждения команды</b><p>Что уже известно и что спорно</p></div></div>
      <div class="context-example">Например: ускорить продажи, сохранив цены</div></div>'''


def comparison() -> str:
    return '''<div class="comparison"><div class="compare-column"><div class="compare-head">БЕЗ ЭТИХ ЗНАНИЙ</div>
      <p>Слова понимаются по-разному</p><p>Важное событие остаётся за кадром</p><p>Совпадение принимают за причину</p></div>
      <div class="compare-column improved"><div class="compare-head">КОГДА ОНИ ДОСТУПНЫ</div>
      <p>Понятны определения и даты</p><p>Видны решения и ограничения</p><p>Гипотезы можно предметно проверить</p></div>
      <div class="compare-foot">Как именно меняется качество ответов — будем измерять отдельно</div></div>'''


def responsibility() -> str:
    return '''<div class="responsibility"><div><span>ИИ</span><b>Собрать и предложить</b><p>Запросы, сводки, версии причин</p></div>
      <div><span>КОМАНДА</span><b>Проверить и уточнить</b><p>Данные, определения, гипотезы</p></div>
      <div><span>РУКОВОДИТЕЛЬ</span><b>Выбрать действие</b><p>Приоритеты, риски, ответственность</p></div>
      <div class="responsibility-note">Степень автоматизации зависит от задачи и цены ошибки</div></div>'''


def first_step() -> str:
    return '''<div class="first-step"><div class="first-question">Один вопрос, по которому<br>вы принимаете решение</div>
      <div class="first-steps"><div><b>01</b><span>Определите показатели</span></div><div><b>02</b><span>Соберите контекст</span></div>
      <div><b>03</b><span>Проверьте данные и ответ</span></div></div>
      <div class="first-close">Начните с полезного решения — затем масштабируйте.</div></div>'''


SLIDES = [
    {'sec': 0, 'type': 'cover', 'title': 'ИИ построит дашборд. Что дальше?',
     'lead': 'Где ИИ помогает девелоперу — и что нужно для надёжной аналитики', 'visual': speaker()},
    {'sec': 0, 'type': 'dashboard', 'title': 'Первый дашборд теперь собирается быстрее',
     'lead': 'Покажем контраст на примере отчёта для руководителя девелопера.', 'visual': dashboard()},
    {'sec': 1, 'type': 'wide', 'title': 'Раньше: больше усилий уходило на сборку',
     'lead': 'Подключение, графики и отчётность занимали значительную часть работы.', 'visual': effort_chart(False)},
    {'sec': 1, 'type': 'wide', 'title': 'Сейчас: усилия смещаются к проверке и решениям',
     'lead': 'Одинаковые виды работы · авторская оценка относительных усилий', 'visual': effort_chart(True)},
    {'sec': 2, 'title': 'Дашборд готов. Что спросить дальше?',
     'lead': 'ИИ может помочь исследовать данные и подготовить варианты для проверки.',
     'visual': '''<div class="question-visual"><div class="question-bubble">«Продажи отстают от плана.<br>Что стоит проверить?»</div>
       <div class="question-path"><span>Данные и срезы</span><i>→</i><span>Гипотезы</span><i>→</i><span>Проверка</span></div>
       <p>ИИ помогает начать исследование. Достоверность выводов нужно подтверждать.</p></div>'''},
    {'sec': 2, 'title': 'Что ИИ уже может сделать',
     'lead': 'При доступе к данным и подходящих инструментах.', 'visual': ability()},
    {'sec': 2, 'title': 'Хороший ответ не гарантирован',
     'lead': 'Даже сильный агент ошибается на сложных аналитических задачах.', 'visual': evidence()},
    {'sec': 2, 'title': 'Где ИИ нужна проверка',
     'lead': 'Три типичные ситуации в аналитике девелопера.', 'visual': limitations()},
    {'sec': 3, 'title': 'Какие знания нужны аналитике',
     'lead': 'Для сложных вопросов ИИ нужны определения, связи и бизнес-контекст.', 'visual': layers()},
    {'sec': 3, 'title': 'Семантический слой: что считаем продажей',
     'lead': 'Определения, периоды и исключения меняют смысл ответа.', 'visual': semantics()},
    {'sec': 3, 'title': 'Дерево метрик: из чего складывается результат',
     'lead': 'Формула помогает разложить показатель и найти место изменения.', 'visual': metric_tree()},
    {'sec': 3, 'title': 'Причинный слой: что могло повлиять',
     'lead': 'Карта помогает сформулировать гипотезы и выбрать, что проверять.', 'visual': causal()},
    {'sec': 3, 'title': 'Контекстный слой: что происходило в бизнесе',
     'lead': 'Цели, решения и события дают цифрам управленческий смысл.', 'visual': context()},
    {'sec': 3, 'title': 'Что дают эти знания',
     'lead': 'Они делают постановку вопроса и проверку ответа предметнее.', 'visual': comparison()},
    {'sec': 4, 'type': 'end', 'title': 'С чего начать',
     'lead': 'Возьмите один важный управленческий вопрос.', 'visual': first_step()},
]

SECTIONS = ['Вступление', 'Куда уходят усилия', 'Возможности и ограничения ИИ', 'Три слоя аналитики', 'Первый шаг']
