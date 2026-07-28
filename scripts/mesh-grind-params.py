#!/usr/bin/env python3
# mesh-grind-params — deterministic-but-DECORRELATED amc param generator for a grind batch.
#
# Operator 2026-07-24: "ты ужасно однообразно комбинируешь … делай совсем разное, все параметры
# крутятся разом (детерминистически, но не скучно и по-разному все)." The old batches held ss/s
# fixed and nudged one knob = a readable straight line through param space. This turns EVERY knob at
# once, each from its OWN hash salt so no two params move together — deterministic (a (src,i) pair
# always yields the same amc, so a render is reproducible) yet spread, never a line.
#
#   usage: mesh-grind-params <src-key> <n>   -> prints n lines, each: "<label>\t<amc tokens...>"
# Non-rw only (operator: "но не rw"); lib+similarity ("close loop") is favoured (operator preference).
import hashlib, sys

src = sys.argv[1] if len(sys.argv) > 1 else "x"
n   = int(sys.argv[2]) if len(sys.argv) > 2 else 4

def u(salt, i):
    """A uniform [0,1) deterministic in (src, i, salt) — independent per salt."""
    h = hashlib.sha256(f"{src}|{i}|{salt}".encode()).hexdigest()
    return int(h[:12], 16) / 0xFFFFFFFFFFFF

def pick(salt, i, seq):
    return seq[int(u(salt, i) * len(seq)) % len(seq)]

def rng(salt, i, lo, hi, nd=2):
    return round(lo + u(salt, i) * (hi - lo), nd)

# mode pool: lib heavily favoured (close loop), then q, poly — never rw. Rotated by i AND jittered by
# a hash so the sequence isn't a fixed cycle either.
MODE_POOL = ["lib", "lib", "q", "lib", "poly", "q", "lib", "poly"]
# Cyclic timelines for `m q` (grainneukeln `amc pat`, 2026-07-24). The euclidean generator can only
# spread k hits evenly over ONE beat, so every q recipe the mesh ever emitted lived in the same
# metric universe — a large part of why the batches read as monotonous. These are real timelines
# spanning multiple beats (12/8 bells, 16-pulse claves, tala thekas, aksak meters), each carrying
# its own cycle length and accent map. None -> keep the euclidean ek/en path, so the two coexist.
TIMELINES = [None, "bembe", "clave32", "teental", "aksak9", "colotomic", "bell6", "gnawa",
             "tresillo", "jajinmori", "rumba32", "maqsum", "khandachapu", "aksak7"]
BANDS  = [None, "300,12000", "100,8000", "80,4000", "500,15000", "1,250", "200,6000", "40,2000"]
EUCLID = [(3, 8), (5, 8), (2, 5), (7, 16), (4, 9), (5, 16), (3, 4), (7, 12)]
WDIV   = [2, 4, 8]
SWING  = [0, 0, 33, 50, 66]
REVP   = [0.0, 0.0, 0.15, 0.3]
LPOL   = ["sim", "sim", "sim", "con"]   # close loop favoured
LK     = [4, 6, 8, 10]

for i in range(n):
    mode = MODE_POOL[(i + int(u("mjit", i) * 3)) % len(MODE_POOL)]
    toks = ["m", mode]
    if mode == "q":
        tl = pick("timeline", i, TIMELINES)
        if tl:
            # `rot` is its own salt: rotating a familiar timeline against unfamiliar material is
            # the cheapest way to a groove that is neither, and it decorrelates from the timeline
            # choice so the same bell never comes back at the same rotation.
            toks += ["pat", tl, "rot", str(int(u("rot", i) * 12))]
        else:
            ek, en = pick("euclid", i, EUCLID)
            toks += ["ek", str(ek), "en", str(en)]
    elif mode == "lib":
        toks += ["lib", pick("lpol", i, LPOL), "lk", str(pick("lk", i, LK))]
    elif mode == "poly":
        # 1–2 streams, decorrelated ratios (';'-joined, single token — safe in an argv array)
        r1 = pick("pr1", i, [2, 3, 4, 5, 6])
        pr = str(r1) if u("pr2", i) < 0.45 else f"{r1};{pick('pr3', i, [2,3,4])}"
        toks += ["pr", pr]
    # universal knobs — all spun, each from its own salt
    toks += ["l",  str(int(rng("l",  i, 90, 560, 0)))]
    toks += ["ss", str(rng("ss", i, 0.55, 1.75))]
    toks += ["s",  str(rng("s",  i, 0.75, 1.35))]
    toks += ["w",  str(pick("w", i, WDIV))]
    band = pick("band", i, BANDS)
    if band:
        toks += ["c", band]
    sw = pick("sw", i, SWING)
    if sw:
        toks += ["sw", str(sw)]
    rv = pick("rv", i, REVP)
    if rv:
        toks += ["rv", str(rv)]
    toks += ["d", str(int(rng("d", i, 40, 60, 0)))]
    toks += ["seed", str(int(u("seed", i) * 100000))]
    print(f"{mode}\t" + " ".join(toks))
