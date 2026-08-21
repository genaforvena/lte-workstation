#!/usr/bin/env python3
"""D2 — silent fallback: a failure converted into a plausible value.

`cmd 2>/dev/null || echo <literal>` turns a TOTAL failure of `cmd` into a constant that is
indistinguishable, at every downstream consumer, from a successful reading. The live case in the
system under study: a beat detector raised under a numpy-less python3, `|| echo 500` swallowed it,
and a "beat-driven" audio grinder ran flat for weeks — the outputs looked fine; only the params
log (`beat 500`, every line) showed the axis was dead (`f51e36d`).

The decision procedure is NOT "does a fallback exist" — a fallback is a correct construct. It is:

    for every failure branch that SUBSTITUTES A LITERAL VALUE:
        LOUD      iff the literal is a marker (na / unknown / error / empty), or control still
                  escapes the branch (exit/return/die), or the branch writes to stderr
        SILENT    iff the literal is a plausible datum in the success domain (a number, a word)
        CRITICAL  iff the literal is a HEALTHY reading (ok/up/true/0/pass/…): the failure does not
                  merely hide, it reports the all-clear
        COLLIDING iff the SAME literal is also emitted on a success path in the same file — the
                  only statically available PROOF that the fallback's value is inside the success
                  domain, rather than an inference from its spelling

`${VAR:-default}` is deliberately OUT of scope: it is a default for an *unset variable*, not a
failure branch, and it is so common in shell that including it would measure prevalence of the
idiom rather than of the defect. Sites where failure is silenced with NO substitute
(`2>/dev/null` alone) are counted and reported apart: they yield empty, which most consumers can
still distinguish from a reading.

  d2_silent_fallback.py <dir> [...]        # human table
  d2_silent_fallback.py --json <dir>
  d2_silent_fallback.py --selftest
"""
import json, os, re, sys

# the failure branch: `|| echo X`, `|| printf X`, optionally brace-wrapped
FALLBACK = re.compile(r'\|\|\s*(?:\{\s*)?(echo|printf)\s+(?:-\w+\s+)*(.+)$')
SILENCED = re.compile(r'2>\s*/dev/null|2>&-')
TERNARY  = re.compile(r'&&\s*(?:\{\s*)?(?:echo|printf)\b[^|]*\|\|')
ESCAPES  = re.compile(r'\b(exit|return|die|fatal|abort|usage)\b')

# A marker announces absence. A consumer can tell it from a reading; that is the whole point.
MARKERS = {"", "na", "n/a", "-", "?", "none", "null", "nil", "unknown", "unavailable", "absent",
           "missing", "error", "err", "fail", "failed", "failure", "empty", "unset", "undef",
           "нет", "n\\/a", "not-found", "notfound", "no-data", "nodata", "skip", "skipped"}
# A healthy token is the strongest form: the failure renders as the all-clear.
# A healthy token LEXICALLY asserts wellness. Numbers are deliberately NOT here: whether `|| echo
# 0` is the all-clear or a correct empty-count depends on the success DOMAIN of the left-hand
# command, which is not statically decidable — `0` is the healthy reading for a fault counter and
# the right answer for a count of matches, and nothing on the page separates them. Grading numbers
# critical inflated this detector's CRITICAL count from 34 to 549 on the first honest run.
HEALTHY = {"ok", "up", "true", "yes", "y", "pass", "passed", "green", "healthy",
           "active", "online", "running", "enabled", "alive", "clean", "good", "success"}
NUMERIC = __import__("re").compile(r"^-?\d+(?:\.\d+)?$")

def _literal(rest):
    """The substituted value. Returns (literal, redirected_to_stderr, undecidable).

    Two ways to be UNDECIDABLE, and keeping them out of the graded population is what makes the
    rate mean anything (D1's lesson: a third state, never folded into a verdict):
      * the value contains a substitution — its runtime text is not the text on the page;
      * the branch could not be PARSED cleanly out of its enclosing context. `$(cmd || echo 0)"`
        hands the naive cut `0)"`, which is in no vocabulary and therefore grades as a plausible
        datum — a false positive manufactured by the parser, not observed in the code. The first
        run of this detector reported 872 SILENT that way (`NA)"`, `absent)`, `null )" \\`).
    """
    depth, end = 0, len(rest)
    for k, ch in enumerate(rest):
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth == 0:
                end = k; break
            depth -= 1
        elif depth == 0 and ch in ";&|}":
            # `>&2` is a redirect, not a branch separator — breaking on its `&` truncates the
            # fragment to `"msg" >` and the parse-failure guard then calls a plainly LOUD
            # diagnostic undecidable. (Caught by the selftest going red, not by review.)
            if ch == "&" and k and rest[k-1] == ">":
                continue
            end = k; break
    cut = rest[:end].strip()
    redirected = bool(re.search(r">\s*&\s*2|>&2", cut))
    cut = re.sub(r"\s*>\s*&?\s*2\s*$", "", cut).strip()
    if re.search(r"(?<!\\)\$[A-Za-z_{(0-9]|`", cut):
        return None, redirected, True
    # unbalanced quotes / an escape left in the fragment == the cut landed mid-token
    if cut.count('"') % 2 or cut.count("'") % 2 or "\\" in cut:
        return None, redirected, True
    while len(cut) >= 2 and cut[0] == cut[-1] and cut[0] in "'\"":
        cut = cut[1:-1].strip()
    if '"' in cut or "'" in cut:
        return None, redirected, True
    return cut, redirected, False

def _grade(lit, filetext, line):
    """MARKER / HEALTHY / plausible datum — and the collision check, which is the only one that
    proves rather than infers."""
    t = lit.strip().strip('"\'').lower()
    if t in MARKERS or re.search(r'\b(err|error|fail|unknown|unavailable|n/a)\b', t):
        return "loud", False
    if len(t.split()) > 3:                      # a sentence is a message, not a datum
        return "loud", False
    # does this exact literal also get emitted on a SUCCESS path elsewhere in the same file?
    esc = re.escape(lit.strip().strip('"\''))
    collide = False
    for other in filetext.split("\n"):
        if other == line or "||" in other:
            continue
        if re.search(r'\b(?:echo|printf)\b[^|;]*(?<![\w-])%s(?![\w-])' % esc, other):
            collide = True; break
    if t in HEALTHY:
        return "critical", collide
    return "silent", collide

def scan_file(path):
    out = []
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return out
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("#"):
            continue
        # `cond && echo Y || echo n` is a two-way TERNARY: the `||` arm is the deliberate FALSE
        # value, not a failure substitute. It matched every naive rule and produced 5 of the first
        # run's hits (`mesh-verify:29,58,64,65,67`, all literal `n`).
        ternary = bool(TERNARY.search(line))
        m = FALLBACK.search(line)
        if not m:
            if SILENCED.search(line):
                out.append({"file": path, "line": i, "kind": "silenced-no-substitute",
                            "verdict": "n/a", "literal": None, "src": s[:160]})
            continue
        lit, redirected, undec = _literal(m.group(2))
        if undec:
            out.append({"file": path, "line": i, "kind": "fallback", "verdict": "undecidable",
                        "literal": None, "src": s[:160]})
            continue
        # A TEST on the left (`[ ... ] || printf ','`) is a conditional, not a failed measurement:
        # nothing was being read, so nothing was silently substituted for a reading.
        left = line[:m.start()].rstrip()
        conditional = left.endswith("]") or bool(re.search(r"\btest\s+[^|]*$", left))
        tail = line[m.end():] + " " + m.group(2)
        # Control ESCAPING the branch (exit/return/die) makes the substitution irrelevant: the
        # failure still propagates. A branch writing to stderr is a diagnostic, not a value.
        if ternary or conditional:
            verdict, collide = "not-a-fallback", False
        elif ESCAPES.search(tail) or redirected:
            verdict, collide = "loud", False
        else:
            verdict, collide = _grade(lit, text, line)
        out.append({"file": path, "line": i, "kind": "fallback", "verdict": verdict,
                    "literal": lit, "colliding": collide,
                    "numeric": bool(NUMERIC.match((lit or "").strip())),
                    "silenced": bool(SILENCED.search(line)), "src": s[:160]})
    return out

def scan(roots):
    hits = []
    for root in roots:
        if os.path.isfile(root):
            hits += scan_file(root); continue
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "vendor", ".venv", "target")]
            for f in files:
                p = os.path.join(d, f)
                try:
                    if os.path.islink(p) or os.path.getsize(p) > 2_000_000:
                        continue
                    with open(p, "rb") as fh:
                        head = fh.read(200)
                except Exception:
                    continue
                if b"\0" in head:
                    continue
                if (head.startswith(b"#!") or os.access(p, os.X_OK)
                        or f.endswith((".sh", ".bash", ".zsh", ".ksh", ".fish", ".py", ".bats"))):
                    hits += scan_file(p)
    return hits

def selftest():
    import tempfile, pathlib
    d = tempfile.mkdtemp()
    p = pathlib.Path(d) / "t.sh"
    p.write_text('#!/bin/sh\n'
        'beat=$(detect 2>/dev/null || echo 500)\n'          # 2 SILENT: a plausible datum
        'st=$(probe 2>/dev/null || echo na)\n'              # 3 loud: marker
        'h=$(check || echo ok)\n'                           # 4 CRITICAL: failure reads healthy
        'v=$(read_it || echo "$DEFAULT")\n'                 # 5 undecidable: value not on the page
        'x=$(cmd) || { echo "cannot read x" >&2; exit 1; }\n'  # 6 loud: stderr + exit
        'y=$(cmd || echo unknown)\n'                        # 7 loud: marker
        'z=$(cmd 2>/dev/null)\n'                            # 8 silenced, no substitute
        'echo 500\n'                                        # 9 a SUCCESS path emitting 500
        'q=$(cmd || echo "could not determine the value here")\n'   # 10 loud: a sentence
        'r=$(probe && echo Y || echo n)\n'                          # 11 TERNARY: n is the false arm
        '[ "$first" = 1 ] || printf ","\n'                          # 12 CONDITIONAL, not a read
        'c=$(count 2>/dev/null || echo 0)\n'                        # 13 numeric: domain-dependent
        'w=$(cmd || echo na\\ b)\n')                                 # 14 cut landed mid-token
    got = {g["line"]: g for g in scan([str(p)])}
    assert got[2]["verdict"] == "silent", "a plausible-datum fallback was not flagged"
    assert got[2]["colliding"] is True, \
        "the same literal emitted on a success path (line 9) was not detected as a domain collision"
    assert got[3]["verdict"] == "loud", "a marker fallback (na) scored as silent"
    assert got[4]["verdict"] == "critical", "a fallback whose value is the all-clear scored as merely silent"
    assert got[5]["verdict"] == "undecidable", "an unexpanded fallback value was graded instead of deferred"
    assert got[6]["verdict"] == "loud", "a branch that writes stderr AND exits scored as a silent fallback"
    assert got[7]["verdict"] == "loud", "marker 'unknown' scored as a datum"
    assert got[8]["kind"] == "silenced-no-substitute", "2>/dev/null with no substitute was miscounted"
    assert got[10]["verdict"] == "loud", "a sentence (a message, not a datum) scored as a value fallback"
    assert got[11]["verdict"] == "not-a-fallback", \
        "the false arm of a `&& echo Y || echo n` ternary scored as a failure substitute"
    assert got[12]["verdict"] == "not-a-fallback", \
        "a `[ test ] || printf` conditional scored as a fallback — nothing was being read"
    assert got[14]["verdict"] == "undecidable", \
        "a branch fragment carrying an escape (the cut landed mid-token) was GRADED instead of " \
        "deferred — this is the guard that removed 872 manufactured false positives"
    assert got[13]["verdict"] == "silent" and got[13]["numeric"] is True, \
        "`|| echo 0` graded critical: whether 0 is the all-clear or a correct empty count is not " \
        "statically decidable, so it must not be asserted to be the all-clear"
    print("d2 selftest: ok (plausible datum = SILENT and its success-path collision proved · "
          "marker = loud · all-clear WORD = CRITICAL but a NUMBER is not · unexpanded value and "
          "an unparseable cut = undecidable · stderr+exit branch = loud · bare 2>/dev/null counted "
          "apart · sentence = loud · ternary false-arm and `[ test ] ||` conditional = not a fallback)")
    return 0

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.stdout.write(__doc__); return 0
    if a[0] == "--selftest":
        return selftest()
    asjson = "--json" in a
    hits = scan([x for x in a if not x.startswith("--")])
    fb = [h for h in hits if h["kind"] == "fallback"]
    dec = [h for h in fb if h["verdict"] != "undecidable"]
    sil = [h for h in dec if h["verdict"] in ("silent", "critical")]
    crit = [h for h in dec if h["verdict"] == "critical"]
    coll = [h for h in dec if h.get("colliding")]
    num = [h for h in sil if h.get("numeric")]
    nfb = [h for h in fb if h["verdict"] == "not-a-fallback"]
    if asjson:
        print(json.dumps({"fallback_sites": len(fb), "decidable": len(dec), "silent": len(sil),
                          "critical": len(crit), "colliding": len(coll), "numeric": len(num),
                          "not_a_fallback": len(nfb),
                          "silenced_no_substitute": len(hits) - len(fb), "hits": hits}, indent=1))
        return 0
    for h in sorted(sil, key=lambda x: (x["verdict"] != "critical", x["file"], x["line"])):
        print("%-9s%s %s:%d  <- %r" % (h["verdict"].upper(), "+coll" if h.get("colliding") else "     ",
                                       h["file"], h["line"], h["literal"]))
    print("\nD2 silent fallback: %d `|| echo` site(s) · %d undecidable · %d ternary/conditional "
          "(not a failure substitute) · %d decidable fallbacks · %d SILENT = %.0f%% "
          "(of which %d CRITICAL — a word asserting the all-clear; %d NUMERIC — domain-dependent, "
          "NOT asserted to be the all-clear; %d with a proven success-domain collision) · "
          "%d bare 2>/dev/null with no substitute"
          % (len(fb), len(fb) - len(dec), len(nfb), len(dec) - len(nfb), len(sil),
             100.0 * len(sil) / (len(dec) - len(nfb)) if len(dec) - len(nfb) else 0,
             len(crit), len(num), len(coll), len(hits) - len(fb)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
