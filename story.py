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




def evidence() -> str:
    return '''<div class="evidence">
      <div class="evidence-stat"><div class="evidence-over">DATA AGENT BENCHMARK · EMNLP 2026</div>
        <div class="evidence-big">57<span>%</span></div><div class="evidence-meaning">pass@1: среднее по наборам</div>
        <p>GPT-5.5 + Codex · 104 запроса · 17 наборов данных · 5 запусков каждого запроса</p>
      </div>
      <div class="evidence-note"><b>Сложные задачи с несколькими источниками.</b><br>У агента были описания данных и подсказки.
        <div class="example-line"><span>ПРИМЕР ДЛЯ ДЕВЕЛОПЕРА</span><strong>Данные о ДДУ и отменах в разных системах</strong></div>
        <small>Результат зависит от задачи и настройки системы; это не оценка качества для вашей компании.</small>
      </div>
      <a class="source" href="https://aclanthology.org/2026.emnlp-main.1872/" target="_blank" rel="noopener">Ma et al., EMNLP 2026 ↗</a>
      </div>'''























# История пилота. Примеры ответов взяты из настроечной, а не закрытой
# контрольной серии; агрегаты последней загружаются из отдельного файла.
def case_setup() -> str:
    return '''<div class="case-setup">
      <div class="case-topline"><strong>3</strong><span>проекта</span><strong>2</strong><span>канала продаж</span></div>
      <div class="case-question">«ИИ видит данные.<br>Почему ответам всё ещё трудно доверять?»</div>
      <div class="case-lower"><span>ДДУ и оплаты</span><span>CRM и воронка</span><span>Планы и события</span></div>
      <p>Воспроизвели типовую ситуацию на подготовленных данных и проверили ответы модели.</p>
      </div>'''


def baseline_answer() -> str:
    return '''<div class="answer-example"><div class="answer-label">ВОПРОС · НАСТРОЕЧНАЯ СЕРИЯ</div>
      <h3>Как распределились ДДУ по каналам?</h3><div class="answer-grid">
      <div><span>НОЯБРЬ 2025</span><strong>20</strong><small>12 агентских · 8 собственных</small></div>
      <div><span>ДЕКАБРЬ 2025</span><strong>25</strong><small>15 агентских · 10 собственных</small></div></div>
      <div class="answer-conclusion">Базовая модель посчитала регистрации верно.</div>
      <p>Это ответ на конкретный вопрос, а не оценка всей системы.</p></div>'''


def stage_comparison(first: int, second: int) -> str:
    import json
    values=json.loads((HERE/'results_public.json').read_text(encoding='utf-8'))['conditions']
    def piece(i: int) -> str:
        item=values[i]
        return f'<b>B{i}</b> {item["low_count"]}–{item["high_count"]} / {item["n"]}'
    return ('<div class="stage-comparison"><span>МОДЕЛЬНЫЕ ОЦЕНКИ С УЧЁТОМ СПОРНЫХ СЛУЧАЕВ</span>'
            f'<div>{piece(first)}<i>→</i>{piece(second)}</div><small>Диапазоны пересекаются; нужна перепроверка.</small></div>')


def semantics_case() -> str:
    return '''<div class="semantic-case"><div class="answer-label">ОДИН И ТОТ ЖЕ МЕСЯЦ · ДЕКАБРЬ 2025</div>
      <div class="semantic-numbers"><div><strong>25</strong><span>ДДУ зарегистрировано</span></div>
      <div class="semantic-symbol">≠</div><div><strong>24</strong><span>из них действовали<br>на конец октября 2026</span></div></div>
      <div class="semantic-definition"><b>Что передали модели</b><p>Событие, период, когорта и правило расторжений.</p></div>
      <small>В настроечном примере B0 верно назвал 25; B1 дополнительно различил 25 и 24.</small>'''+stage_comparison(0,1)+'</div>'


def map_case() -> str:
    return '''<div class="case-map"><div class="answer-label">РАСКЛАДЫВАЕМ ОТКЛОНЕНИЕ</div>
      <div class="formula-row"><span>Факт</span><b>−</b><span>План</span><b>=</b><strong>Отклонение</strong></div>
      <div class="project-branches"><span>Проект A</span><span>Проект B</span><span>Проект C</span></div>
      <div class="case-map-caption">Сумма отклонений проектов при единых определениях</div>
      <div class="map-divider"></div><div class="answer-label">ВЫДВИГАЕМ ГИПОТЕЗЫ</div>
      <div class="driver-row"><span>Цена</span><span>Ипотека</span><span>Ассортимент</span></div>
      <svg class="hypothesis-links" viewBox="0 0 600 35" role="img" aria-label="Возможные влияния на продажи">
      <path d="M100 0 V12 H300 V35 M300 0 V35 M500 0 V12 H300"/></svg>
      <div class="map-outcome">Продажи</div>
      <div class="map-note">Гипотезы о влиянии требуют проверки. Дерево само по себе не доказывает причину.</div></div>'''


def causal_case() -> str:
    return '''<div class="causal-case"><div class="answer-label">ЧТО ПОЛУЧИЛА МОДЕЛЬ В B2</div>
      <div class="causal-stage"><strong>Обращения</strong><span>→</span><strong>Встречи</strong><span>→</span><strong>Брони</strong><span>→</span><strong>ДДУ</strong></div>
      <div class="causal-detail"><div><b>Последовательность</b><p>Сопоставимая когорта и окно наблюдения</p></div>
      <div><b>Причина</b><p>Вопрос о воздействии, сравнение и проверка допущений</p></div></div>
      <div class="case-callout">Структура помогает искать версии, но не заменяет проверку влияния.</div>'''+stage_comparison(1,2)+'</div>'


def context_case() -> str:
    return '''<div class="context-case"><div class="answer-label">ВОПРОС СОКРАЩЁННО · КОРПУС A1 И ПРОДАЖИ ПРОЕКТА A</div>
      <div class="demo-question">«Старт задержался и продажи просели?»</div>
      <div class="demo-start"><b>План и факт старта A1</b><span>1 февраля 2025</span></div>
      <div class="demo-answer-pair"><div><span>B2 · ПЕРВЫЙ ПОВТОР</span><b>Квартальный расчёт<br>не завершён</b><small>Исчерпан лимит запросов</small></div>
      <div><span>B3 · ПЕРВЫЙ ПОВТОР</span><b>9 · 19 · 24 · 37</b><small>Регистрации ДДУ по кварталам 2025</small></div></div>
      <small>В первом повторе B0 тоже посчитал кварталы. Эти отдельные ответы не доказывают эффект слоя.</small>'''+stage_comparison(2,3)+'</div>'


def limitation_case() -> str:
    return '''<div class="limit-case"><div class="answer-label">РЕАЛЬНЫЙ ФРАГМЕНТ ОТВЕТА · B3</div>
      <blockquote>«1 900 000,00 руб. <span>(190 000 400 коп. / 10 записей)</span>»</blockquote>
      <div class="limit-math"><b>1 900 000 ₽ = 190 000 000 коп.</b><span>Разница: 4 ₽</span></div>
      <p>Основная сумма верна. В скобках — несогласованность; в принятых оценках её не отметили.</p>
      <small>Настроечная серия: небольшая ошибка в детали, не провал всей задачи.</small></div>'''


def method_case() -> str:
    return '''<div class="method-case"><div class="method-hero"><div><b>30</b><span>сценариев</span></div><i>×</i>
      <div><b>4</b><span>условия</span></div><i>×</i><div><b>3</b><span>повтора</span></div></div>
      <div class="method-stack"><div><b>B0</b><span>Данные и базовая инструкция</span></div>
      <div><b>B1</b><span>+ определения показателей</span></div><div><b>B2</b><span>+ карты и деревья</span></div>
      <div><b>B3</b><span>+ факты о стартах и планах</span></div></div>
      <p>Одна модель, отдельная сессия на ответ. Два модельных оценщика сверяют ответы с эталоном.</p>
      <small>Повторы и связанные сценарии не являются независимыми компаниями.</small></div>'''


def measured_comparison() -> str:
    import json
    p=HERE/'results_public.json'
    if not p.exists():
        raise RuntimeError('Ожидаются проверенные агрегаты контрольной серии')
    data=json.loads(p.read_text(encoding='utf-8'))
    rows=[]
    for x in data['conditions']:
        low,high,n=x['low_count'],x['high_count'],x['n']
        rows.append(f'<div class="measure-row"><b>{E(x["name"])}</b><div class="measure-track">'
                    f'<i class="measure-possible" style="width:{100*high/n:.3f}%"></i>'
                    f'<i class="measure-confirmed" style="width:{100*low/n:.3f}%"></i></div>'
                    f'<strong>{low}–{high} <small>/ {n}</small></strong></div>')
    return ('<div class="measured"><div class="answer-label">ПРИГОДНЫЕ ОТВЕТЫ · ПРЕДВАРИТЕЛЬНАЯ ОЦЕНКА</div>'
            +''.join(rows)+'<div class="measure-legend"><span><i></i>согласие моделей без известных проблем</span>'
            '<span><i></i>нужна перепроверка</span></div>'
            '<p>Перепроверка: спорные оценки, проблемный эталон и один оборванный ответ.</p>'
            '<small>Две модели-оценщика, один подготовленный набор и одна модель-аналитик. '
            'Диапазоны пересекаются и не являются доверительными интервалами; ошибки оценщиков могут оставаться. Нужна проверка человеком.</small></div>')


def practical_plan() -> str:
    return '''<div class="plan-case"><div class="plan-row"><b>01</b><div><strong>Выберите вопросы руководителя</strong><span>И проверьте исходные ответы ИИ</span></div></div>
      <div class="plan-row"><b>02</b><div><strong>Согласуйте определения и связи</strong><span>Метрики, периоды, гипотезы, владельцы</span></div></div>
      <div class="plan-row"><b>03</b><div><strong>Добавьте доступный контекст</strong><span>Решения, события и ограничения</span></div></div>
      <div class="plan-row"><b>04</b><div><strong>Повторите проверку</strong><span>Сравните ответы и разберите ошибки</span></div></div></div>'''


SLIDES = [
    {'sec': 0, 'type': 'cover', 'title': 'ИИ построит дашборд. Что дальше?',
     'lead': 'Как добиться полезных ответов в аналитике девелопера', 'visual': speaker()},
    {'sec': 0, 'type': 'dashboard', 'title': 'Дашборд теперь собрать проще',
     'lead': 'Сразу несколько источников и десятки визуализаций.', 'visual': dashboard()},
    {'sec': 1, 'type': 'wide', 'title': 'Раньше: больше усилий уходило на сборку',
     'lead': 'Подключение, графики и отчётность занимали значительную часть работы.', 'visual': effort_chart(False)},
    {'sec': 1, 'type': 'wide', 'title': 'Сейчас: усилия смещаются к проверке и решениям',
     'lead': 'Одинаковые виды работы · авторская оценка относительных усилий', 'visual': effort_chart(True)},
    {'sec': 2, 'title': 'ИИ уже работает с данными. Но ответам не всегда верят',
     'lead': 'Мы проверили, что меняется после добавления знаний.', 'visual': case_setup()},
    {'sec': 2, 'title': 'Начинаем с исходного ответа',
     'lead': 'Дадим модели вопрос, схему данных и доступ к SQL.', 'visual': baseline_answer()},
    {'sec': 2, 'title': 'Даже сильный агент может ошибиться',
     'lead': 'Сложность задачи и качество постановки имеют значение.', 'visual': evidence()},
    {'sec': 3, 'title': '1. Семантика: что именно считаем?',
     'lead': 'Согласовали определения, периоды и исключения.', 'visual': semantics_case()},
    {'sec': 3, 'title': '2. Дерево и карта: как устроен результат?',
     'lead': 'Формула показывает состав результата. Карта помогает искать причины.', 'visual': map_case()},
    {'sec': 3, 'title': 'Связь показателей ещё не доказывает влияние',
     'lead': 'Передали модели последовательность и гипотезы для проверки.', 'visual': causal_case()},
    {'sec': 3, 'title': '3. Контекст: один вопрос, два ответа',
     'lead': 'Добавили доступную историю событий и версий плана.', 'visual': context_case()},
    {'sec': 3, 'title': 'Даже после добавления знаний ответ надо проверять',
     'lead': 'Дополнительные знания не гарантируют безошибочного ответа.', 'visual': limitation_case()},
    {'sec': 4, 'title': 'Как мы сравнили четыре условия',
     'lead': 'Один и тот же банк вопросов. Знания добавляются последовательно.', 'visual': method_case()},
    {'sec': 4, 'title': 'Как менялись ответы после добавления знаний',
     'lead': 'Предварительная оценка для этой модели и этого набора заданий.', 'visual': measured_comparison()},
    {'sec': 5, 'type': 'end', 'title': 'С чего начать у себя',
     'lead': 'Проверяйте ИИ на вопросах, по которым вы действительно принимаете решения.', 'visual': practical_plan()},
]

SECTIONS = ['Вступление', 'Куда уходят усилия', 'Ситуация и исходный ответ', 'Три пакета знаний', 'Проверка результатов', 'Первый шаг']
