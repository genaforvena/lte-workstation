# Verify optimized promise matching preserves capped identities and tokenization.
"""Differential checks for the capped matcher and lazy tokenization."""
import ast
import functools
import random
import re
from pathlib import Path

source = (Path(__file__).resolve().parents[1] / 'scripts/mesh-promises').read_text()
code = source.split("  python3 - \"$@\" <<'PYEOF'\n", 1)[1].split('\nPYEOF', 1)[0]
tree = ast.parse(code)
nodes = [n for n in tree.body if
         (isinstance(n, ast.FunctionDef) and n.name in ('toks', 'key_suffixes', 'keys_agree'))
         or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('STOP', 'SLUG_CAP') for t in n.targets))]
ns = dict(re=re, lru_cache=functools.lru_cache)
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<production-matchers>', 'exec'), ns)

def old_agree(ck, slug):
    if not ck or not slug:
        return False
    if ck == slug:
        return True
    a, b = (ck, slug) if len(ck) <= len(slug) else (slug, ck)
    if len(a) < 4:
        return False
    for start in [0] + [i + 1 for i, c in enumerate(b) if c == '-']:
        seg = b[start:]
        if seg == a or seg.startswith(a + '-'):
            return True
        if len(a) >= 40 and b.startswith(a):
            return True
        if len(b) >= 40 and len(seg) >= 4 and a.startswith(seg):
            return True
    return False

def old_toks(s, cap=None):
    out = []
    for w in re.split(r'[\W_]+', (s or '').lower()):
        if len(w) >= 4 and w not in ns['STOP']:
            out.append(w)
            if cap and len(out) >= cap:
                break
    return out

rng = random.Random(1926)
vocab = ('alpha', 'beta', 'mesh', 'проверка', 'a', 'x' * 40, 'x' * 39, 'tail')
keys = ['', None, '-', '---', 'pub', 'republish', 'pub-242370', 'route-orphan-pub-242370']
keys += ['-'.join(rng.choices(vocab, k=rng.randint(1, 9))) for _ in range(400)]
for _ in range(12000):
    a, b = rng.choices(keys, k=2)
    for left, right in ((a, b), (a, (a or '')[:40]), ((a or '')[-20:], a)):
        assert ns['keys_agree'](left, right) == old_agree(left, right), (left, right)
for _ in range(500):
    text = ''.join(rng.choice(vocab) + rng.choice((' ', '_', '-', '::', 'é', '🙂')) for _ in range(20))
    for cap in (None, 0, 1, 8, 12, -1):
        assert ns['toks'](text, cap) == old_toks(text, cap), (text, cap)
print('PASS: 36000 key comparisons and 3000 tokenization cases preserve exact semantics')
