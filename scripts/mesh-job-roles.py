"""mesh-job-roles — ОДНА грамматика «его ли это роль», которую вызывают ОБА подающих тула.

Импортируется, а не копируется. mesh-job-apply (hh) и mesh-job-apply-getmatch решают один и тот же
вопрос — «попадает ли название в то, что оператор просил искать», — и пока предикат жил в одном
туле копией, второй отвечал иначе: 2026-08-25 hh-лана подала на «Senior SRE Engineer», «Системный
архитектор» и «Senior Go R&D Engineer» в тот же день, когда getmatch-лана эти же формы отсеивала,
потому что у hh-ланы гейта роли не было вовсе — только веса, а вес решает ПОРЯДОК, не ДОПУСК.
Две частные копии одного предиката обе зелёные и ни одна не полная.

ДВА КЛАССА РУКОВОДЯЩИХ СЛОВ, и они требуют разного:

* SELF_LEAD — титул, который САМ называет инженерную область: Tech Lead, Team Lead, тимлид,
  Engineering Manager, CTO, технический директор. Требовать от него ОТДЕЛЬНОГО предметного слова
  значит выбросить «Principal Tech Lead, домен Retail» и «Tech lead в Центр Робототехники» — ровно
  те вакансии, ради которых гейт и ставился. Это правило CLAUDE.md про освобождение ПОЗИЦИИ,
  которую грамматика уже зафиксировала.
* RANK_LEAD — голый РАНГ: руководитель, head of, начальник отдела, директор по. Ранг есть в каждой
  отрасли страны («Head of Legal», «Руководитель отдела ХоРеКа», «Бригадир участка»), поэтому
  здесь и только здесь предметное слово обязано стоять ОТДЕЛЬНО.

Замерено на живой доске 2026-08-25: hh-поиск по руководящим запросам вернул 415 строк, из них про
разработку 113 (27%). hh матчит нестрого, и запрос про ДОЛЖНОСТЬ возвращает должность.
"""
# orphan-ok: библиотека, а не рефлекс — у неё нет и не должно быть cron-строки. Исключение
# ссылается на ВЫЗЫВАЮЩИХ, а не на способность: `grep -l _load_roles scripts/` даёт ровно
# mesh-job-apply и mesh-job-apply-getmatch, и оба падают на старте, если этот файл не найден
# (raise SystemExit, а не тихий пропуск гейта). Проверять грепом, а не верить этой строке —
# сегодня же выяснилось, что orphan-ok, сославшийся на ФЛАГ вместо вызывающего, четверо суток
# прятал несплетённый mesh-tg-sweep.
import re

SELF_LEAD_RE = re.compile(r"team\s*lead|teamlead|тимлид|тим-лид|tech\s*lead|techlead|техлид|"
                          r"lead manager|engineering manager|engineering lead|(?<!\w)cto(?!\w)|"
                          r"технический директор|head of engineering|директор по разработ", re.I)

RANK_LEAD_RE = re.compile(r"руководител|head of|начальник отдел|директор по|лидер команд|"
                          r"(?<!\w)lead(?!\w)", re.I)

DOMAIN_RE = re.compile(r"разработ|develop|инженер|engineer|backend|бэкенд|fullstack|golang|"
                       r"(?<!\w)go(?!\w)|architect|архитект|devops|(?<!\w)sre(?!\w)|платформ|"
                       r"platform|engineering|software|программн", re.I)

# Роли, которые несут и руководящее слово, и предметное, и всё равно НЕ его: чужая инженерная
# специальность. Оператор 2026-08-25 просил руководителя РАЗРАБОТКИ, не тестирования и не
# поддержки. Список держится КОРОТКИМ и предметным — это не «фильтр всего плохого», а именование
# соседних инженерных цехов, которые иначе проходят обе половины гейта.
NOT_HIS_RE = re.compile(r"(?<!\w)qa(?!\w)|тестировани|тестировщик|автоматизац\w* тестир|"
                        r"технической поддержк|(?<!\w)1с(?!\w)|(?<!\w)1c(?!\w)|"
                        r"информационн\w* безопасност|media buying|медиабаинг", re.I)


def role_verdict(title, employer=""):
    """-> (ok: bool, reason: str). reason пуст, когда ok.

    Смотрит ТОЛЬКО на название и работодателя, никогда на нашу собственную служебную приписку:
    в note лежит текст запроса, по которому строка нашлась, то есть то, что спросили МЫ, а не то,
    что вакансия про себя говорит. Гейт, читающий свой же вопрос, пропускает всё."""
    hay = "%s %s" % (title or "", employer or "")
    if NOT_HIS_RE.search(hay):
        return False, "соседний инженерный цех, не разработка"
    if SELF_LEAD_RE.search(hay):
        return True, ""
    if not RANK_LEAD_RE.search(hay):
        return False, "не руководящая роль"
    if not DOMAIN_RE.search(hay):
        return False, "голый ранг без предметной области"
    return True, ""


def selftest():
    fails = []

    def check(name, ok, extra=""):
        print("%s %s%s" % ("ok:  " if ok else "FAIL:", name, ("  <- " + extra) if extra and not ok else ""))
        if not ok:
            fails.append(name)

    for title, want in [
        # Инженерный титул несёт область в себе.
        ("Principal Tech Lead, домен Retail", True),
        ("Tech lead в Центр Робототехники", True),
        ("Team Lead Go (GigaChat)", True),
        ("Engineering Manager: Offsite Discovery", True),
        ("CTO / Head of Engineering", True),
        # Голый ранг требует предметного слова рядом.
        ("Руководитель группы разработки", True),
        ("Руководитель IT отдела", False),
        ("Head of Legal", False),
        ("Руководитель отдела продаж / Head of Sales", False),
        ("Бригадир участка FBS", False),
        # IC-лейн снят оператором 2026-08-25.
        ("Senior Go Developer", False),
        ("Senior SRE Engineer", False),
        ("Ведущий Golang-разработчик", False),
        ("Системный архитектор (Python / Go)", False),
        # Соседний цех: обе половины есть, роль не его.
        ("Team Lead QA Automation", False),
        ("Руководитель отдела технической поддержки и операционного управления платформой", False),
        ("Тимлид команды 1С (ЗУП / ERP)", False),
        ("Head of Native / Team Lead Media Buying", False),
    ]:
        got, why = role_verdict(title)
        check("%-62s -> %s" % (title[:62], "ДА" if want else "нет"), got == want,
              "got=%s (%s)" % (got, why))

    # note НЕ читается: там наш собственный запрос, и гейт, читающий свой вопрос, пропускает всё.
    ok_self, _ = role_verdict("Senior Go Developer", "LLC Контора")
    check("наш собственный запрос не подаётся сюда (сигнатура принимает только title+employer)",
          ok_self is False)

    print("smoke-test: %s" % ("ok" if not fails else "FAIL (%s)" % ", ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    import sys
    sys.exit(selftest())
