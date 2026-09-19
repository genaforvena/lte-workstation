# Verify one shared hledger balance preserves every promise-family verdict and fails closed.
"""Check reuses one real hledger balance and refuses failed balance reads."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
real = shutil.which('hledger')
assert real, 'hledger required'
with tempfile.TemporaryDirectory(prefix='promise-check-balances-') as temp:
    root = Path(temp)
    bindir = root / '.local/bin'
    bindir.mkdir(parents=True)
    stub = bindir / 'hledger'
    stub.write_text('''#!/usr/bin/env bash
printf '%s\n' "$*" >> "$HL_CALLS"
if [[ " $* " == *" balance "* && "${HL_FAIL_BALANCE:-0}" == 1 ]]; then
  echo 'fixture balance unavailable' >&2
  exit 73
fi
if [[ " $* " == *" balance "* && -n "${HL_NEGATIVE_FAMILY:-}" ]]; then
  printf ' -1 TEST  liabilities:%s:alpha:negative\n' "$HL_NEGATIVE_FAMILY"
  exit 0
fi
exec "$HL_REAL" "$@"
''')
    stub.chmod(0o755)
    board = root / 'chat.log'
    board.write_text('2026-09-19T00:00:00Z alpha@n :: [task] sample: build sample; task:sample owner:alpha\n'
                     '2026-09-19T00:00:01Z alpha@n :: [taking] sample: starting; task:sample\n'
                     '2026-09-19T00:00:02Z beta@n :: [verify] alpha: independent check; task:independent\n')
    voice = root / 'voice'
    voice.write_text('')
    calls = root / 'calls'
    env = dict(os.environ, HOME=temp, MESH_DIR=temp, MESH_CHAT_LOG=str(board),
               MESH_ASK_VOICE_IN=str(voice), MESH_ASK_TG_SENT=str(root / 'no-sent'),
               MESH_PROMISE_ROSTER='alpha beta', MESH_PROMISE_LIVE_WINDOWS='alpha beta',
               HL_REAL=real, HL_CALLS=str(calls))
    result = subprocess.run(['bash', str(repo / 'scripts/mesh-promises'), '--check'],
                            env=env, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, (result.stdout, result.stderr)
    balances = [row for row in calls.read_text().splitlines() if ' balance ' in ' ' + row + ' ']
    assert len(balances) == 1, balances
    assert result.stdout.count('agreement: PASS') == 4, result.stdout
    env['HL_FAIL_BALANCE'] = '1'
    result = subprocess.run(['bash', str(repo / 'scripts/mesh-promises'), '--check'],
                            env=env, capture_output=True, text=True, timeout=20)
    assert result.returncode == 73, (result.returncode, result.stdout, result.stderr)
    assert 'balance' in result.stderr and 'failed' in result.stderr, result.stderr
    assert 'agreement: PASS' not in result.stdout, result.stdout
    print('PASS: one balance parse, four family agreements, failed balance read returns rc73')
    env.pop('HL_FAIL_BALANCE')
    for family in ('promises', 'claims', 'holds', 'asks'):
        env['HL_NEGATIVE_FAMILY'] = family
        result = subprocess.run(['bash', str(repo / 'scripts/mesh-promises'), '--check'],
                                env=env, capture_output=True, text=True, timeout=20)
        assert result.returncode == 1 and 'over-discharge' in result.stdout and 'FAIL' in result.stdout, (
            family, result.returncode, result.stdout, result.stderr)
    print('PASS: every family refuses a negative leaf in the shared balance')

    # Real local hledger differential: flat snapshot retains family-level totals
    # and exact negative leaves, including quarantined accounts and long names.
    journal = root / 'differential.journal'
    postings = []
    for family, commodity in [('promises', 'PROMISE'), ('claims', 'CLAIM'), ('holds', 'HOLD'), ('asks', 'ASK')]:
        postings.extend([f'    liabilities:{family}:alpha:long-account-name-with-many-segments  2 {commodity}',
                         f'    liabilities:{family}:unrouted:negative  -1 {commodity}',
                         f'    equity:{family}  -1 {commodity}'])
    journal.write_text('2026-09-19 Differential\n' + '\n'.join(postings) + '\n')
    def balance(account, flat=False):
        return subprocess.check_output([real, '-f', str(journal), 'balance', account,
                                        '--no-total', '-N'] + (['--flat'] if flat else []), text=True)
    snapshot = balance('liabilities', flat=True).splitlines()
    for family in ('promises', 'claims', 'holds', 'asks'):
        account = 'liabilities:' + family
        old = balance(account).splitlines()
        new = [row for row in snapshot if row.split()[-1] == account or row.split()[-1].startswith(account + ':')]
        assert sum(float(row.split()[0]) for row in old) == sum(float(row.split()[0]) for row in new)
        assert {tuple(row.split()) for row in old if row.lstrip().startswith('-')} == {
            tuple(row.split()) for row in new if row.lstrip().startswith('-')}
    print('PASS: all family totals and negative leaves equal separate hledger queries')
