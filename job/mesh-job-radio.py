"""Радио-адаптер: выбирает ОДИН переключатель работодателя там, где ПЕЧАТАТЬ нечего.

ПОЧЕМУ ЭТО ОТДЕЛЬЕННАЯ ФУНКЦИЯ С ЯВНЫМИ ПРАВИЛАМИ, А НЕ ПОИСК ПОХОЖЕСТИ.

Замерено на 84 уникальных радио-блоках живого hh-лога (2026-09-23): банк ответов — это
ЕГО ПРОЗА, а переключатели — это РАЗМЕТКА РАБОТОДАТЕЛЯ. Общего алфавита у них нет, и любое
правило «выбери вариант, наиболее похожий на ответ» выбирает НЕ ТОТ:

  * «Каковы ваши зарплатные ожидания?», банк «500 000 ₽/мес на руки», варианты
    «До 150к / 150-300к / 300-350к / 350-450к / От 450к» — токены «150», «300», «450»
    в ответе нет ни одного, overlap-оценка РАВНА для всех пяти; наивный счётчик берёт
    ПЕРВЫЙ и отправляет ему зарплату 150к.
  * «Как давно вы работаете с Go», банк «7 лет», варианты «Больше 6-ти лет / 4-6 лет /
    Менее 4х лет» — наилучшее совпадение по словам — «4-6 лет» (цифры в строке две).
  * «Какой формат работы рассматриваете», банк «Открыт к любому формату: удалёнка,
    гибрид, офис», варианты три — пересечение есть со всеми тремя.

То есть похожесть СИСТЕМАТИЧЕСКИ ложна, а не иногда. Поэтому здесь — ЯВНАЯ таблица:
вопрос опознаётся по своему ФАКТУ (зарплата, локация,Go-опыт…), а выбор делается
ПРАВИЛОМ для этого факта. Вопроса, которого таблица не знает, — нет выбора, и форма
уходит в `FORM_UNREADABLE` (снимает: КОД), как и до этой правки. Банк новых ответов
не пополняется: используются только существующие sourced-строки.

ГРАНИЦА. Совпадение по варианту должно быть СТРОГИМ: выбирается ровно один вариант, и
только если правило однозначно указало на него. Никаких «двух похоже подходящих»,
никаких догадок про числовые диапазоны, которых банк не дал.
"""

import re

# ── ЯВНЫЕ ПРАВИЛА ──────────────────────────────────────────────────────────────────────
# Каждое: (паттерн вопроса, селектор варианта). Селектор возвращает ИНДЕКС варианта или None.
# Паттерны пишутся под ФАКТ, а не под текст конкретного работодателя.

_NUM = re.compile(r"([0-9][0-9\s ]{0,8}[0-9]?)\s*[кk]?\s*(тыс|к|k)?", re.I)


def _norm(t):
    """Текст к одному виду: регистр, NBSP, пунктуация-разделители. Переносы внутри числа
    («150-300к», «500 000») специально сохраняются — их разбирает само правило."""
    return re.sub(r"\s+", " ", (t or "").replace("\u00a0", " ")).strip()


def _yes_answer(answer):
    """Да/Нет факт. Возвращает True/False/None(неясно)."""
    a = (answer or "").lower()
    if not a:
        return None
    # «Нет — 15+ лет backend» начинается с отрицания, и это важно не спутать с «Да, …».
    starts_no = bool(re.match(r"^\s*(нет|no)\b", a))
    starts_yes = bool(re.match(r"^\s*(да|yes)\b", a))
    if starts_yes:
        return True
    if starts_no:
        return False
    return None


def _pick_yes(options):
    """Из вариантов Да/Нет выбираем утвердительный. Возвращает индекс или None.

    Сигнал — «вариант, который не есть отказ»: вырианты бывают «Да»/«Нет», а бывают
    развёрнутые («Я живу в Москве и готов…» vs «Не готов»). Берём утверждение, ОДНО.
    """
    cands = []
    for i, o in enumerate(options):
        s = _norm(o).lower().strip(" .;:!?")
        if not s:
            continue
        # «не» в начале = отказ. «Не уверен» — тоже не согласие, но и не отказ — пропускаем.
        if s.startswith("не ") or s.startswith("нет"):
            continue
        if s.startswith("да") and (len(s) <= 4 or s[2] in ",. "):
            cands.append(i)
            continue
        if re.match(r"^(yes|я )", s):
            cands.append(i)
            continue
        # Развёрнутый утвердительный вариант: не отказ и не «не знаю».
        if not re.match(r"^(не знаю|не уверен)", s):
            cands.append(i)
    return cands[0] if len(cands) == 1 else None


def _pick_no(options):
    cands = []
    for i, o in enumerate(options):
        s = _norm(o).lower().strip(" .;:!?")
        if s.startswith("нет") or s.startswith("не ") or s.startswith("no"):
            cands.append(i)
    return cands[0] if len(cands) == 1 else None


def _pick_russia(options, answer):
    """«Проживаете в РФ / located outside of Russia» — выбираем «нахожусь в РФ».

    Банк: «Да, проживаю в России (Нижний Новгород)» / «No, I am located in Russia».
    Инверсия (английский вариант спрашивает «снаружи ли России?») здесь же: для него
    ответ — «in Russia», а НЕ «outside of Russia». Правило ищет формулировку «в России»
    и отвергает «вне РФ».
    """
    cands = []
    for i, o in enumerate(options):
        s = _norm(o).lower()
        if not s:
            continue
        if re.search(r"outside of russia|вне рф|постоянной основе прожива", s):
            continue
        if re.search(r"\b(rf|рф|russia|росси)\b", s) or "в россии" in s or "in russia" in s:
            cands.append(i)
    return cands[0] if len(cands) == 1 else None


def _pick_relocate_moscow(options, answer):
    """«Вакансия подразумевает офис в Москве — вы готовы?» — он не в Москве, но готов
    переехать. Выбираем «живу в другом городе, готов к переезду»."""
    cands = []
    for i, o in enumerate(options):
        s = _norm(o).lower()
        if re.search(r"другом городе|готов\s+к\s+переезду|relocat", s):
            cands.append(i)
    return cands[0] if len(cands) == 1 else None


def _pick_salary(options, answer):
    """Зарплатный диапазон. Банк даёт число (500 000 ₽/мес) — выбираем диапазон,
    который ЕГО содержит. СТРОГО одно вхождение, иначе отказ.

    Варианты вида «До 150к», «150-300к», «От 450к», «300-350к». Парсим числа каждого
    варианта и сравниваем с числом из ответа.
    """
    m = re.search(r"([0-9][0-9\s\u00a0]{0,10})\s*000?", _norm(answer))
    if not m:
        return None
    try:
        target = float(re.sub(r"[\s\u00a0]", "", m.group(1)))
    except ValueError:
        return None
    if target <= 0:
        return None
    if target < 1000:  # «500 ₽/мес» — явно не то, что имелось в виду
        return None
    hits = []
    for i, o in enumerate(options):
        s = _norm(o).lower()
        nums = [int(x) for x in re.findall(r"[0-9]{1,7}", s.replace(" ", ""))]
        # «До 150к» -> 150 (тыс), «150-300к» -> 150 и 300, «От 450к» -> 450.
        # «350-450к» — это диапазон.
        if not nums:
            continue
        thou = [n * 1000 if n < 1000 else n for n in nums]
        if re.match(r"^\s*до\b|^до\b", s) or s.startswith("до"):
            lo, hi = 0, thou[0]
            if lo <= target <= hi:
                hits.append(i)
        elif re.match(r"^\s*от\b|^от\b", s) or s.startswith("от"):
            lo, hi = thou[0], float("inf")
            if target >= lo:
                hits.append(i)
        elif len(thou) >= 2:
            lo, hi = thou[0], thou[1]
            if lo <= target <= hi:
                hits.append(i)
        else:
            # Одно число без «до»/«от» — однозначно не диапазон, не угадываем.
            continue
    return hits[0] if len(hits) == 1 else None


def _pick_go_years(options, answer):
    """«Как давно вы работаете с Go» — банк: «7 лет» / «Более 2-х лет… с 2023».
    Число лет сравнивается с диапазонами варианта. Цифры в варианте — годы,
    а не зарплата и не RPS: это РАЗНЫЕ правила, хотя грамматика похожая."""
    nums = [int(x) for x in re.findall(r"\d+", _norm(answer))]
    years = None
    for n in nums:
        if 1 <= n <= 45:
            years = n
            break
    if years is None:
        return None
    hits = []
    for i, o in enumerate(options):
        s = _norm(o).lower()
        onums = [int(x) for x in re.findall(r"\d+", s)]
        if not onums:
            # «Больше 6-ми лет» — слова «больше/менее/от/свыше» БЕЗ числа: число берём из
            # числительного слова, если оно есть.
            word = re.search(r"(больш|меньш|свыше|от |more|less)", s)
            if word:
                wn = re.search(r"(шесть|шести|six|четыре|четырёх|four|два|двух|two)", s)
                if wn:
                    onums = [{"шесть": 6, "шести": 6, "six": 6, "четыре": 4, "четырёх": 4,
                              "four": 4, "два": 2, "двух": 2, "two": 2}[wn.group(1).lower()]]
        if not onums:
            continue
        n = onums[0]
        if re.search(r"больш|свыше|more|от \d|от\d", s):
            if years >= n:
                hits.append(i)
        elif re.search(r"меньш|less", s):
            if years < n:
                hits.append(i)
        elif len(onums) >= 2:
            if onums[0] <= years <= onums[1]:
                hits.append(i)
        elif s.startswith("менее"):
            if years < n:
                hits.append(i)
    return hits[0] if len(hits) == 1 else None


def _pick_experience_years(options, answer):
    """«Сколько лет коммерческого опыта» — банк: «15+ лет в разработке (с 2011)».
    Диапазоны вида «0-1.99 / 2-3.99 / 4-5.99 / 6+»."""
    m = re.search(r"(\d+)\s*\+?\s*лет", _norm(answer).lower())
    if not m:
        return None
    years = int(m.group(1))
    hits = []
    for i, o in enumerate(options):
        s = _norm(o).lower().strip()
        onums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s)]
        if not onums:
            continue
        if re.search(r"\d\s*\+|\d\+$|от\s*\d", s):
            if years >= onums[0]:
                hits.append(i)
        elif len(onums) >= 2:
            if onums[0] <= years <= onums[1]:
                hits.append(i)
    return hits[0] if len(hits) == 1 else None


def _pick_deepest(options, answer, keywords):
    """Выбираем САМЫЙ глубокий вариант, упоминающий keyword, когда банк подтверждает
    продакшен-опыт. Это для решёток «локально / базово / проектировал»: ответ «в проде»
    однозначно соответствует самой сильной ступени, и только ей.

    Опасность: взять ступень, которой он не соответствует. Поэтому условие — в ответе
    ОБЯЗАТЕЛЬНО есть продакшен-маркер («проде», «production», «проде»), а ступень
    выбирается по её собственному маркеру глубины.
    """
    a = _norm(answer).lower()
    if not re.search(r"\b(проде|production|прод-?|in prod)\b", a):
        return None
    best = None
    for i, o in enumerate(options):
        s = _norm(o).lower()
        if not re.search(keywords, s):
            continue
        # Глубина: самая сильная ступень в решётке.
        if re.search(r"проектировал|самостоятельно\s+настраивал|архитектур", s):
            best = i
        elif best is None:
            best = i
    return best


def _pick_team_size(options, answer):
    """«Какой у вас опыт руководства командами» — банк: «вёл команду из 9 инженеров».
    Решётка: «3-5 / 6-9 / 10-15 / 15+». Берём диапазон, содержащий 9."""
    m = re.search(r"команд[а-я]*\s+из\s+(\d+)|команд[а-я]*\s+(\d+)", _norm(answer).lower())
    if not m:
        return None
    size = int(next(g for g in m.groups() if g))
    if size <= 0:
        return None
    hits = []
    for i, o in enumerate(options):
        s = _norm(o).lower()
        onums = [int(x) for x in re.findall(r"\d+", s)]
        if not onums:
            continue
        if re.search(r"15\s*\+|15\s*человек", s):
            if size >= 15:
                hits.append(i)
            continue
        if len(onums) >= 2:
            if onums[0] <= size <= onums[1]:
                hits.append(i)
    return hits[0] if len(hits) == 1 else None


def _pick_rps(options, answer):
    """Нагрузка: банк — «50 000 HTTP req/s … 50+ млн запросов в сутки». Решётка по RPS.
    Самая высокая ступень, и только она: 50k RPS — это «10 000+ RPS»."""
    a = _norm(answer).lower()
    m = re.search(r"([\d\s\u00a0]{1,12})\s*(http\s*req/s|rps)", a)
    if not m:
        return None
    try:
        rps = float(re.sub(r"[\s\u00a0]", "", m.group(1)))
    except ValueError:
        return None
    if rps <= 0:
        return None
    best = None
    for i, o in enumerate(options):
        s = _norm(o).lower()
        if "rps" not in s:
            continue
        onums = [int(x) for x in re.findall(r"\d+", s.replace(" ", "").replace("\u00a0", ""))]
        if not onums:
            continue
        hi = max(onums)
        if rps >= hi and (best is None or hi >= max(
                int(x) for x in re.findall(r"\d+", _norm(options[best]).lower()
                                           .replace(" ", "").replace("\u00a0", "")))):
            best = i
    return best


# Таблица: (паттерн вопроса) -> правило. Порядок важен: частные раньше общих.
SLOTS = [
    (re.compile(r"зарплат|оклад|доход|salary|expectation", re.I), _pick_salary),
    (re.compile(r"how many years|сколько лет коммерческого|коммерческого опыта", re.I),
     _pick_experience_years),
    (re.compile(r"как давно.*\bgo\b|работаете с go|go на коммерческих", re.I), _pick_go_years),
    (re.compile(r"руководства командами|командой разработки|team lead|тимлид", re.I),
     _pick_team_size),
    (re.compile(r"нагрузк|rps|high-?load|qps", re.I), _pick_rps),
    (re.compile(r"located outside of russia|прожива\w+ в рф|находитесь в рф|в рф или казахстан",
                re.I), _pick_russia),
    (re.compile(r"офисный формат работы|офис.*5 дн|готовы к переезду в москву", re.I),
     _pick_relocate_moscow),
]


def radio_choice(question, options, answer):
    """ЧИСТАЯ. (вопрос, список вариантов, ответ банка) -> индекс варианта | None.

    None — НЕ отказ от формы, а отсутствие решения: вызывающий оставляет строку в
    needs-human с причиной `form` (снимает: КОД), как и до этой правки.
    """
    q = _norm(question)
    a = _norm(answer or "")
    if not q or not a or not options:
        return None
    opts = [_norm(o) for o in options]
    # Да/Нет-вопрос — отдельный класс: вариант «Да»/«Нет», и ответ банка начинается с Да/Нет.
    yn = _yes_answer(a)
    if yn is not None:
        idx = _pick_yes(opts) if yn else _pick_no(opts)
        if idx is not None:
            return idx
        # Развёрнутые варианты («Я живу в другом городе, но готов…») — да/нет-логика не та:
        # выбирает правило для факта ниже.
    for pat, rule in SLOTS:
        if pat.search(q):
            idx = rule(opts, a)
            if idx is not None:
                return idx
            # Правило узнало факт, но не выбрало — отказ, а не падение в следующий слот.
            return None
    return None
