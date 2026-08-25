#!/usr/bin/env python3
"""D3 — window < cadence: a sample published as a state.

A scheduled sense observes the world through a *window* and reports on a *cadence*. When the
window is narrower than the cadence, the reading describes a fraction of wallclock and says
nothing at all about the rest — yet it is almost always published as a **state**, a single word
about how things *are*. The live case in the system under study: `mesh-psi` read `avg10` — a
10-second decaying kernel average — once every 600 seconds, and reported `CALM` for **14.2 days**
on a node that was repeatedly stalling between ticks (`fe35dd9`). Coverage was 10/600 = 1.7%. No
reading was wrong. Every reading was a true statement about ten seconds, published as a claim
about ten minutes.

The decision procedure is NOT "is coverage low" — a narrow window is often the only window the
kernel offers, and a 1.7% sample is a legitimate thing to *have*. It is:

    for every tool carrying a `# reflex-cadence:` header:
        period   := mean seconds between fires, from the EXPANDED fire set (never the step)
        window   := the span of wallclock the probe's own sample covers
        coverage := window / period

        FULL      iff coverage >= 1.0 — the reading spans its own interval, typically because the
                  tool delta's a monotonic ACCUMULATOR against a stored previous sample. This is
                  the cure, not merely a pass.
        HONEST    iff coverage < 1.0 AND the tool publishes a coverage/window term in its own
                  output. A 1.7% sample that SAYS it is a 1.7% sample is not this defect; the
                  consumer can weigh it. Honesty is cheaper than coverage and it is the fix that
                  is always available.
        SAMPLE-AS-STATE iff coverage < 1.0 and no coverage term is published — the defect. The
                  gap between ticks is unobserved and nothing in the reading records that.
        UNDECIDABLE iff the window cannot be resolved from the page (see below).

UNDECIDABLE IS A VERDICT, NOT A FAILURE. D1's lesson, kept: a third state that is never folded
into a rate. A window is only counted when the page states it — a kernel field that names its own
averaging window (`avg10`), a `sleep N` separating two reads of one source, or a duration flag on
a command known to take one. `timeout N` is deliberately NOT a window: it bounds how long the
probe may *take*, not what span of world it *observes*, and grading it as a window would turn a
deadline into evidence of coverage — the exact confusion this class is about.

  d3_window_under_cadence.py <dir> [...]     # human table
  d3_window_under_cadence.py --json <dir>
  d3_window_under_cadence.py --selftest
"""
import json, os, re, sys

# ── cadence ────────────────────────────────────────────────────────────────────────────────────
CADENCE_HDR = re.compile(r'^#\s*reflex-cadence:\s*(.+?)\s*$', re.M)

def _field(spec, lo, hi):
    """Expand one cron field into the set of values it fires on.

    Returns None if the field is not one this parser understands — an unparsed field must not
    silently become a wildcard, which would fabricate a fire set.
    """
    out = set()
    for part in spec.split(','):
        step = 1
        if '/' in part:
            part, _, s = part.partition('/')
            if not s.isdigit() or int(s) == 0:
                return None
            step = int(s)
        if part == '*':
            a, b = lo, hi
        elif '-' in part.lstrip('-'):
            a_s, _, b_s = part.partition('-')
            if not (a_s.isdigit() and b_s.isdigit()):
                return None
            a, b = int(a_s), int(b_s)
        elif part.isdigit():
            a = b = int(part)
        else:
            return None
        if a < lo or b > hi or a > b:
            return None
        out.update(range(a, b + 1, step))
    return out or None

def cadence_seconds(expr):
    """(mean_period_s, max_gap_s, fires_per_day) from a 5-field cron expression, or None.

    The period is derived from the EXPANDED fire set, never from the step. `2-59/5` and `*/5` both
    give 300s; `50-59/15` collapses to a single fire an hour and gives 3600s, which reading the
    step alone would report as 900s — a 4x understatement of the unobserved gap.
    """
    f = expr.split()
    if len(f) != 5:
        return None
    minute, hour = _field(f[0], 0, 59), _field(f[1], 0, 23)
    if minute is None or hour is None:
        return None
    # day-of-month / month / day-of-week: only the unrestricted case is modelled. A restricted
    # calendar field makes "per day" the wrong denominator, and guessing it is worse than n/a.
    if any(x.strip() != '*' for x in f[2:]):
        return None
    fires = sorted(h * 3600 + m * 60 for h in hour for m in minute)
    if not fires:
        return None
    if len(fires) == 1:
        return (86400.0, 86400.0, 1)
    gaps = [b - a for a, b in zip(fires, fires[1:])] + [fires[0] + 86400 - fires[-1]]
    return (86400.0 / len(fires), float(max(gaps)), len(fires))

# ── window evidence ────────────────────────────────────────────────────────────────────────────
# A kernel field that NAMES its own averaging window. The window is not inferred; it is read off
# the field's own spelling, which is why this is the strongest evidence available statically.
KERNEL_AVG = [
    (re.compile(r'\bavg(\d+)\s*='), lambda m: float(m.group(1))),      # /proc/pressure avg10/60/300
    (re.compile(r'\bavg(\d+)\b'),   lambda m: float(m.group(1))),
    (re.compile(r'/proc/loadavg'),  lambda m: 60.0),                   # first column is the 1-min avg
]
# A command whose duration flag is genuinely a capture window. Bound to the COMMAND, never to the
# bare flag: `-l 2` appears 55 times in this corpus and is almost never a duration.
CAPTURE = [
    (re.compile(r'termux-microphone-record\b[^\n|;&]*?-l\s+(\d+)'), 1.0),
    (re.compile(r'\btcpdump\b[^\n|;&]*?-G\s+(\d+)'),                1.0),
    (re.compile(r'\b(?:top|iostat|vmstat|sar|mpstat)\b[^\n|;&]*?-d\s+(\d+)'), 1.0),
    (re.compile(r'\barecord\b[^\n|;&]*?-d\s+(\d+)'),                1.0),
    (re.compile(r'\bffmpeg\b[^\n|;&]*?-t\s+(\d+)'),                 1.0),
    (re.compile(r'\bperf\s+stat\b[^\n|;&]*?\bsleep\s+(\d+)'),       1.0),
]
PING = re.compile(r'\bping\b[^\n|;&]*?-c\s+(\d+)')
PING_I = re.compile(r'\bping\b[^\n|;&]*?-i\s+([\d.]+)')
SLEEP = re.compile(r'(?:^|[;&|]|\bthen\b|\bdo\b)\s*sleep\s+([\d.]+)\s*(?:$|[;&|\n])', re.M)
# An accumulator delta'd across the interval: the reading spans the whole gap by construction.
# Requires BOTH a persisted previous sample and an arithmetic difference — either alone is not it.
PREV_STORE = re.compile(r'\b(prev|previous|last|baseline|_prev|_last)[a-z_]*\b', re.I)
STATE_FILE = re.compile(r'\.(state|cache|prev|last)\b|/\.[a-z0-9-]+\.state\b|MESH[A-Z_]*STATE')
DELTA_ARITH = re.compile(r'\b(?:delta|diff|_d)\s*=|=\s*\$?\(?\s*\$?\{?\w+\}?\s*-\s*\$?\{?(?:prev|last|baseline)', re.I)
# The tool publishing its own coverage. This is the cure that costs nothing.
COVERAGE_TERM = re.compile(r'\bcoverage\s*[=:]|\bcover\s*=|\bwindow\s*=|window_[a-z_]*"?\s*[:=]', re.I)

def strip_comments(text):
    """Remove shell comments before looking for window evidence.

    NOT cosmetic. `mesh-node-health` mentions `avg10/60/300` three times — every one inside a
    comment explaining a *different* tool's thresholds — and the first honest run of this detector
    graded it SAMPLE-AS-STATE on that prose. A detector whose evidence is source text it never
    parsed is the paper's own C1 one ring up: the assertion and its evidence are the same string.
    Line-initial comments go entirely; a trailing ` #` is cut only when no quote is open before it.
    """
    out = []
    for line in text.splitlines():
        st = line.lstrip()
        if st.startswith('#'):
            out.append('')
            continue
        cut, q = len(line), None
        i = 0
        while i < len(line):
            c = line[i]
            if q:
                if c == q:
                    q = None
            elif c in '"\'':
                q = c
            elif c == '#' and i > 0 and line[i-1] in ' \t':
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return '\n'.join(out)

def window_of(raw):
    """(window_seconds, evidence_kind) or (None, 'undecidable').

    Strongest evidence first. Ties inside a kind take the LARGEST window on the page — an
    overstated window understates the defect, so the detector errs against its own finding.
    """
    text = strip_comments(raw)
    if PREV_STORE.search(text) and STATE_FILE.search(text) and DELTA_ARITH.search(text):
        return (None, 'accumulator')          # window == period by construction; graded FULL
    best = None
    for rx, fn in KERNEL_AVG:
        for m in rx.finditer(text):
            v = fn(m)
            if best is None or v > best:
                best = v
    if best is not None:
        return (best, 'kernel-avg')
    for rx, _ in CAPTURE:
        for m in rx.finditer(text):
            v = float(m.group(1))
            if best is None or v > best:
                best = v
    if best is not None:
        return (best, 'capture')
    m = PING.search(text)
    if m:
        n = int(m.group(1))
        mi = PING_I.search(text)
        iv = float(mi.group(1)) if mi else 1.0
        return (max(0.0, (n - 1) * iv), 'ping-train')
    # A bare `sleep N` is a window only if it separates two reads; that is not decidable here, so
    # it is reported as its own kind and NOT graded. Counting it would measure retry backoff.
    if SLEEP.search(text):
        return (None, 'sleep-unresolved')
    return (None, 'undecidable')

# ── grading ────────────────────────────────────────────────────────────────────────────────────
def grade(path, text):
    m = CADENCE_HDR.search(text)
    if not m:
        return None
    expr = m.group(1)
    cad = cadence_seconds(expr)
    win, kind = window_of(text)
    honest = bool(COVERAGE_TERM.search(text))
    row = {"file": os.path.basename(path), "cadence": expr, "evidence": kind,
           "period_s": None, "max_gap_s": None, "fires_per_day": None,
           "window_s": win, "coverage": None, "publishes_coverage": honest, "verdict": None}
    if cad is None:
        row["verdict"] = "UNDECIDABLE"
        row["why"] = "cadence expression not modelled (calendar field, or unparsed)"
        return row
    period, maxgap, fires = cad
    row.update(period_s=period, max_gap_s=maxgap, fires_per_day=fires)
    row["irregular"] = maxgap > 2 * period
    if kind == 'accumulator':
        row["verdict"], row["coverage"] = "FULL", 1.0
        row["why"] = "monotonic accumulator delta'd against a persisted previous sample"
        return row
    if win is None:
        row["verdict"] = "UNDECIDABLE"
        row["why"] = ("a bare `sleep` is present but nothing on the page says it separates two "
                      "reads" if kind == 'sleep-unresolved' else
                      "no construct on the page states the span the probe samples")
        return row
    cov = win / period if period else None
    row["coverage"] = cov
    if cov >= 1.0:
        row["verdict"], row["why"] = "FULL", "window spans the interval"
    elif honest:
        row["verdict"] = "HONEST"
        row["why"] = "coverage < 1 but the reading carries its own coverage/window term"
    else:
        row["verdict"] = "SAMPLE-AS-STATE"
        row["why"] = (f"{win:g}s window on a {period:g}s cadence = {cov*100:.1f}% of wallclock, "
                      "published with no coverage term")
    return row

def scan(paths):
    rows = []
    for root in paths:
        if os.path.isfile(root):
            files = [root]
        else:
            files = [os.path.join(dp, f) for dp, dns, fs in os.walk(root)
                     if not (dns.__setitem__(slice(None), [d for d in dns if d != '__pycache__']) or True) or True
                     for f in fs if not f.endswith(('.pyc', '.pyo', '.so'))]
        for p in sorted(files):
            try:
                text = open(p, encoding='utf-8', errors='replace').read()
            except (OSError, IsADirectoryError):
                continue
            r = grade(p, text)
            if r:
                rows.append(r)
    return rows

# ── selftest ───────────────────────────────────────────────────────────────────────────────────
FIXTURES = [
    # (name, source, expected verdict, expected coverage-or-None)
    ("the live case: avg10 on a 600s tick, no coverage term", """#!/bin/sh
# reflex-cadence: 3-59/10 * * * *
v=$(awk '/^some/{for(i=1;i<=NF;i++) if($i~/^avg10=/){sub("avg10=","",$i);print $i}}' /proc/pressure/cpu)
case "$v" in *) echo "level=CALM";; esac
""", "SAMPLE-AS-STATE", 10/600),

    ("same window, same cadence, but it says so", """#!/bin/sh
# reflex-cadence: 3-59/10 * * * *
v=$(awk '/^some/{for(i=1;i<=NF;i++) if($i~/^avg10=/){sub("avg10=","",$i);print $i}}' /proc/pressure/cpu)
echo "level=CALM coverage=1.7%"
""", "HONEST", 10/600),

    ("accumulator delta'd across the interval", """#!/bin/sh
# reflex-cadence: */5 * * * *
now=$(cat /proc/net/dev | awk '{s+=$2} END{print s}')
prev=$(cat ~/.mesh/.netio.state 2>/dev/null || echo 0)
delta=$((now - prev)); echo "$now" > ~/.mesh/.netio.state
echo "rate=$delta"
""", "FULL", 1.0),

    ("a stepped range that COLLAPSES to one fire an hour", """#!/bin/sh
# reflex-cadence: 50-59/15 * * * *
v=$(awk '/^some/{for(i=1;i<=NF;i++) if($i~/^avg10=/){sub("avg10=","",$i);print $i}}' /proc/pressure/cpu)
echo "level=CALM"
""", "SAMPLE-AS-STATE", 10/3600),

    ("a real capture window that spans its cadence", """#!/bin/sh
# reflex-cadence: */1 * * * *
termux-microphone-record -l 90 -f /tmp/a.m4a
echo "room=quiet"
""", "FULL", 1.5),

    ("timeout is a deadline, not a window", """#!/bin/sh
# reflex-cadence: */5 * * * *
timeout 30 curl -s https://example.com > /tmp/x
echo "egress=ok"
""", "UNDECIDABLE", None),

    ("a bare sleep is not evidence of a delta", """#!/bin/sh
# reflex-cadence: */5 * * * *
for i in 1 2 3; do curl -s x || sleep 5; done
echo "up=yes"
""", "UNDECIDABLE", None),

    ("a ping train is a real window", """#!/bin/sh
# reflex-cadence: */10 * * * *
ping -c 11 -i 1 192.168.8.1 > /tmp/p
echo "lan=up"
""", "SAMPLE-AS-STATE", 10/600),

    ("no cadence header at all -> not a subject", """#!/bin/sh
echo hi
""", None, None),

    ("naming a `last` variable is not an accumulator", """#!/bin/sh
# reflex-cadence: */5 * * * *
last_run=$(date -u +%s)
v=$(awk '/^some/{for(i=1;i<=NF;i++) if($i~/^avg10=/){sub("avg10=","",$i);print $i}}' /proc/pressure/cpu)
echo "level=CALM last_run=$last_run"
""", "SAMPLE-AS-STATE", 10/300),

    ("a persisted previous sample that is never subtracted is not one either", """#!/bin/sh
# reflex-cadence: */5 * * * *
prev=$(cat ~/.mesh/.x.state 2>/dev/null)
v=$(awk '/^some/{for(i=1;i<=NF;i++) if($i~/^avg10=/){sub("avg10=","",$i);print $i}}' /proc/pressure/cpu)
echo "$v" > ~/.mesh/.x.state
echo "level=CALM"
""", "SAMPLE-AS-STATE", 10/300),

    ("a window named only in a COMMENT is not evidence", """#!/bin/sh
# reflex-cadence: */5 * * * *
# thresholds below mirror mesh-psi, which reads avg10/60/300 on its own cadence
v=$(cat /sys/class/thermal/thermal_zone0/temp)
echo "temp=$v"
""", "UNDECIDABLE", None),

    ("an unmodelled calendar field is n/a, never a guess", """#!/bin/sh
# reflex-cadence: 0 3 * * 1
v=$(awk '/^some/{print $2}' /proc/pressure/cpu)  # avg10
echo "weekly=CALM"
""", "UNDECIDABLE", None),
]

MUTANTS = [
    # (name, source, verdict that must NOT be produced) — each is a fixture with the defect
    # REMOVED or INVERTED; a detector that still reports the same verdict is not deciding.
    ("coverage term removed from the honest case", FIXTURES[1][1].replace(" coverage=1.7%", ""),
     "HONEST"),
    ("accumulator's persisted previous sample removed", """#!/bin/sh
# reflex-cadence: */5 * * * *
now=$(cat /proc/net/dev | awk '{s+=$2} END{print s}')
echo "rate=$now"
""", "FULL"),
    ("step read literally would give 900s, not 3600s", FIXTURES[3][1], None),  # checked numerically
    ("timeout relabelled as a capture flag", """#!/bin/sh
# reflex-cadence: */5 * * * *
arecord -d 30 /tmp/a.wav
echo "x=1"
""", "UNDECIDABLE"),
    ("a window wider than the cadence must not read as the defect", """#!/bin/sh
# reflex-cadence: */1 * * * *
tcpdump -G 120 -w /tmp/x.pcap
echo "net=ok"
""", "SAMPLE-AS-STATE"),
]

def selftest():
    fails = []
    for name, src, want, wantcov in FIXTURES:
        got = grade("fixture", src)
        gv = got["verdict"] if got else None
        if gv != want:
            fails.append(f"FIXTURE {name!r}: verdict {gv!r} != {want!r}")
            continue
        if want and wantcov is not None:
            gc = got.get("coverage")
            if gc is None or abs(gc - wantcov) > 1e-6:
                fails.append(f"FIXTURE {name!r}: coverage {gc!r} != {wantcov!r}")
    # the stepped-range trap, asserted numerically rather than by verdict
    for expr, want_period in (("*/5 * * * *", 300.0), ("2-59/5 * * * *", 300.0),
                              ("50-59/15 * * * *", 3600.0), ("7,37 * * * *", 1800.0),
                              ("17 * * * *", 3600.0), ("* * * * *", 60.0)):
        got = cadence_seconds(expr)
        if got is None or abs(got[0] - want_period) > 1e-6:
            fails.append(f"CADENCE {expr!r}: period {got and got[0]!r} != {want_period}")
    if cadence_seconds("none") is not None:
        fails.append("CADENCE 'none' must be n/a, not a period")
    for name, src, must_not in MUTANTS:
        if must_not is None:
            continue
        got = grade("mutant", src)
        gv = got["verdict"] if got else None
        if gv == must_not:
            fails.append(f"MUTANT {name!r}: still reports {must_not!r} — the gate did not move")
    for f in fails:
        print("FAIL:", f)
    n = len(FIXTURES) + 7 + len([m for m in MUTANTS if m[2]])
    print(f"selftest: {n - len(fails)}/{n} arms pass" if fails else
          f"selftest: {n}/{n} arms pass ({len(FIXTURES)} fixtures, 7 cadence, "
          f"{len([m for m in MUTANTS if m[2]])} mutants)")
    return 1 if fails else 0

# ── main ───────────────────────────────────────────────────────────────────────────────────────
def main(argv):
    if "--selftest" in argv:
        return selftest()
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("-")]
    if not paths:
        print(__doc__.strip().splitlines()[-4].strip(), file=sys.stderr)
        return 2
    rows = scan(paths)
    if as_json:
        print(json.dumps(rows, indent=2))
        return 0
    order = {"SAMPLE-AS-STATE": 0, "HONEST": 1, "FULL": 2, "UNDECIDABLE": 3}
    rows.sort(key=lambda r: (order.get(r["verdict"], 9), r.get("coverage") or 0, r["file"]))
    print(f"{'verdict':<16} {'cov':>7}  {'win':>6} {'period':>7}  {'evidence':<16} file")
    for r in rows:
        cov = f"{r['coverage']*100:.1f}%" if r["coverage"] is not None else "—"
        win = f"{r['window_s']:g}s" if r["window_s"] is not None else "—"
        per = f"{r['period_s']:g}s" if r["period_s"] is not None else "—"
        print(f"{r['verdict']:<16} {cov:>7}  {win:>6} {per:>7}  {r['evidence']:<16} {r['file']}")
    tot = len(rows)
    from collections import Counter
    c = Counter(r["verdict"] for r in rows)
    graded = tot - c["UNDECIDABLE"]
    print(f"\n{tot} tools carry a cadence header. Graded {graded}; UNDECIDABLE {c['UNDECIDABLE']} "
          f"(not folded into any rate).")
    if graded:
        print(f"  SAMPLE-AS-STATE {c['SAMPLE-AS-STATE']}  ({c['SAMPLE-AS-STATE']/graded*100:.0f}% of graded)"
              f"   HONEST {c['HONEST']}   FULL {c['FULL']}")
    irr = sum(1 for r in rows if r.get("irregular"))
    if irr:
        print(f"  {irr} have an irregular cadence (max gap > 2x mean): coverage varies across the day.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
