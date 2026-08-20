#!/usr/bin/env python3
"""D1 — self-grepping gate: an assertion whose evidence is its own source text.

A test that proves a property by grepping the file it lives in (`grep -q '<literal>' "$0"`) also
matches the grep LINE, so the assertion asserts itself and can never fail. Mechanical decision
procedure, no heuristics:

    for every line L in file F that greps F's own source ($0 / __file__ / the script's own path):
        extract the pattern P actually passed to grep
        SELF-MATCHING  iff  P matches L itself   (run grep with the same flags against L alone)

A self-matching gate is vacuous by construction: the text it looks for is guaranteed present.
The complement (a non-self-matching source-grep) is reported separately — it is not vacuous, but
it still asserts a STRING is present, never that the code runs.

  d1_self_grepping_gate.py <dir> [...]        # human table
  d1_self_grepping_gate.py --json <dir>
  d1_self_grepping_gate.py --selftest
"""
import json, os, re, subprocess, sys

# a grep whose *target* is the script's own source
SELF_TARGET = re.compile(r'"\$0"|\$0\b|__file__|\$\{BASH_SOURCE\[0\]\}|"\$BASH_SOURCE"')
GREP_CALL   = re.compile(r'\b(?:z)?e?grep\b')

def _extract(line):
    """Return (pattern, flags) for a grep invocation, or None. The pattern is the first
    non-flag argument; flags carry -E/-F/-i so the re-run uses the same language."""
    m = GREP_CALL.search(line)
    if not m:
        return None
    rest = line[m.end():]
    flags, pat = [], None
    i, n = 0, len(rest)
    while i < n:
        while i < n and rest[i] in " \t":
            i += 1
        if i >= n:
            break
        if rest[i] == "-" and i + 1 < n and rest[i+1] not in " \t":
            j = i
            while j < n and rest[j] not in " \t":
                j += 1
            flags.append(rest[i:j]); i = j; continue
        q = rest[i]
        if q in "'\"":
            j = i + 1
            while j < n and rest[j] != q:
                j += 2 if rest[j] == "\\" else 1
            pat = rest[i+1:j]; break
        j = i
        while j < n and rest[j] not in " \t":
            j += 1
        pat = rest[i:j]; break
    if pat is None:
        return None
    return pat, "".join(flags)

def self_matches(pattern, line, flags):
    """Ask GREP ITSELF, with the same dialect — never a python-re approximation of BRE."""
    argv = ["grep", "-q"]
    for f in ("-E", "-F", "-i", "-w"):
        if f in flags or (len(f) == 2 and any(f[1] in g[1:] for g in flags.split() if False)):
            argv.append(f)
    for g in re.findall(r"-(\w+)", flags):
        for ch in g:
            if ch in "EFiw" and "-" + ch not in argv:
                argv.append("-" + ch)
    argv += ["--", pattern]
    try:
        return subprocess.run(argv, input=line, text=True, capture_output=True, timeout=10).returncode == 0
    except Exception:
        return False

def scan_file(path):
    out = []
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    except Exception:
        return out
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("#") or not GREP_CALL.search(line) or not SELF_TARGET.search(line):
            continue
        # THE DISCRIMINATOR, and the one that decides whether this detector measures anything:
        #   grep -q 'P' "$0"        greps the SOURCE  -> in class
        #   "$0" --list | grep -q 'P'  EXECUTES the script and greps its OUTPUT -> a behavioural
        #                              gate, the OPPOSITE of this class, and it matches every
        #                              naive `$0 near grep` rule. Require $0 to be an OPERAND of
        #                              the grep: same pipeline segment, positioned AFTER the grep.
        seg = None
        for piece in re.split(r'\|\||&&|[|;]', line):
            if GREP_CALL.search(piece):
                seg = piece; break
        if seg is None:
            continue
        gm = GREP_CALL.search(seg)
        got = _extract(line)
        if not got:
            continue
        pat, flags = got
        # `$0` occurring INSIDE the pattern (a script that greps for the literal text "$0.0000")
        # is not a reference to this file. Remove the pattern before asking who the operand is.
        after = seg[gm.end():]
        if pat:
            after = after.replace(pat, " ")
        if not SELF_TARGET.search(after):
            continue
        if not pat or pat in ("-q",):
            continue
        # A pattern carrying an unexpanded shell expansion is statically UNDECIDABLE — its runtime
        # text is not the text on the page. Scoring it either way would be an invented verdict.
        undecidable = bool(re.search(r'(?<!\\)\$[A-Za-z_{(0-9]|`', pat))
        # A boolean gate (-q / used as a test) is the class. `grep -c`/`grep -n` on the source is a
        # COUNT or a LOCATION: the grep line inflates the count by one, which biases the threshold
        # instead of guaranteeing it, so it is a different (weaker) defect and is reported apart.
        mode = "count" if re.search(r"-\w*c", flags) else ("locate" if re.search(r"-\w*n", flags) else "bool")
        # Polarity decides the FATE of a self-match: in a positive assertion (|| fail) it always
        # passes and is silently vacuous; in a negative one (&& fail) it always fails, so it is
        # found immediately and never survives. Same construct, opposite outcome.
        polarity = "negative" if re.search(r'"\$0"\s*&&|\$0\s*&&', seg + line[len(seg):]) else "positive"
        sm = False if undecidable else self_matches(pat, line, flags)
        out.append({"file": path, "line": i, "pattern": pat, "undecidable": undecidable,
                    "mode": mode, "polarity": polarity,
                    "self_matching": sm, "vacuous": bool(sm and mode == "bool" and polarity == "positive"),
                    "src": s[:160]})
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
                if os.path.islink(p) or os.path.getsize(p) > 2_000_000:
                    continue
                try:
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
    # NB the load-bearing fact this fixture encodes: a LITERAL pattern is present in its own grep
    # line BY CONSTRUCTION, so a literal source-grep at $0 is always vacuous. The only source-greps
    # that escape are the ones whose pattern cannot match the line it is written on — anchors,
    # or a pattern held in a variable.
    p.write_text('#!/bin/sh\n'
                 'grep -q \'push_heal\' "$0" || exit 1\n'          # literal: self-matching, vacuous
                 'grep -qE \'^set -euo\' "$0" || exit 1\n'         # anchored: cannot match this line
                 'grep -q "$PAT" "$0" || exit 1\n'                 # variable: undecidable statically
                 'grep -q "push_heal" other.sh || exit 1\n'          # not self-targeted at all
                 '"$0" --list | grep -q \'mind:plan\' || exit 1\n'      # EXECUTES itself: behavioural
                 'n=$(grep -c \'bg_gate\' "$0")\n'                     # a COUNT, not a boolean gate
                 'grep -q \'TODO_LEFTOVER\' "$0" && exit 1\n'          # NEGATIVE: a self-match fails loudly
                 'grep -qF \'spent $0.0000\' <<< "$x" || exit 1\n')    # $0 inside the PATTERN
    got = scan([str(p)])
    assert len(got) == 5, "self-targeted grep count wrong: %r" % [(g["line"], g["pattern"]) for g in got]
    by = {g["line"]: g for g in got}
    assert by[7]["mode"] == "count" and not by[7]["vacuous"], "a grep -c on the source scored as a boolean gate"
    assert by[8]["polarity"] == "negative" and not by[8]["vacuous"], \
        "a NEGATIVE self-match scored vacuous — it always FAILS, it does not always pass"
    assert 9 not in by, "a $0 occurring inside the PATTERN was read as the grep's file operand"
    assert got[0]["vacuous"] is True, "a literal pattern in its own line read as non-vacuous"
    assert got[1]["self_matching"] is False, "an ANCHORED pattern that cannot match its line read as vacuous"
    assert got[2]["undecidable"] is True and got[2]["self_matching"] is False, \
        "an unexpanded variable pattern was scored instead of being called undecidable"
    print("d1 selftest: ok (literal positive source-grep = VACUOUS · anchored one not · unexpanded "
          "pattern = undecidable · another file, a self-EXECUTION pipeline, a grep -c count and a "
          "$0 inside the pattern all correctly not counted · a NEGATIVE self-match is not vacuous)")
    return 0

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.stdout.write(__doc__); return 0
    if a[0] == "--selftest":
        return selftest()
    asjson = "--json" in a
    roots = [x for x in a if not x.startswith("--")]
    hits = scan(roots)
    vac = [h for h in hits if h["vacuous"]]
    und = [h for h in hits if h["undecidable"]]
    bools = [h for h in hits if h["mode"] == "bool" and not h["undecidable"]]
    if asjson:
        print(json.dumps({"sites": len(hits), "bool_gates_decidable": len(bools),
                          "vacuous": len(vac), "undecidable": len(und), "hits": hits}, indent=1)); return 0
    for h in hits:
        tag = "VACUOUS" if h["vacuous"] else ("undec" if h["undecidable"] else
              (h["mode"] if h["mode"] != "bool" else "ok"))
        print("%-8s %s:%d  /%s/" % (tag, h["file"], h["line"], h["pattern"][:60]))
    print("\nD1 self-grepping gate: %d source-grep site(s) · %d undecidable (unexpanded pattern) · "
          "%d decidable BOOLEAN gate(s) · %d VACUOUS = %.0f%% of those"
          % (len(hits), len(und), len(bools), len(vac),
             100.0 * len(vac) / len(bools) if bools else 0))
    return 0

if __name__ == "__main__":
    sys.exit(main())
