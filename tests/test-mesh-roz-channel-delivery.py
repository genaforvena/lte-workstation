import os, pathlib, subprocess, tempfile, unittest

ROOT=pathlib.Path(__file__).parents[1]; SCRIPT=ROOT/"scripts/mesh-roz-channel"

def setup_env(d, tmux='ok', tell='ok'):
    d=pathlib.Path(d); b=d/'bin'; b.mkdir()
    (b/'tmux').write_text(f'''#!/bin/sh
if [ "$1" = has-session ]; then {'exit 0' if tmux == 'ok' else 'exit 1'}; fi
exit 1
''')
    (b/'tmux').chmod(0o755)
    (b/'mesh-tell').write_text(f'''#!/bin/sh
    n=$(wc -l < "$MESH_TEST_CALLS" 2>/dev/null || echo 0); n=$((n+1)); printf '%s|%s' "$n" "$*" | tr '\\n' ' ' >> "$MESH_TEST_CALLS"; printf '\\n' >> "$MESH_TEST_CALLS"
    {'exit 0' if tell == 'ok' else 'if [ "$n" -eq 1 ]; then exit 1; else exit 0; fi'}
''')
    (b/'mesh-tell').chmod(0o755)
    # shell children cannot persist exported counters; the call log is the durable test oracle.
    return os.environ | {'HOME':str(d), 'PATH':str(b)+':'+os.environ['PATH'], 'ROZ_CHAT_ID':'12', 'MESH_ROZ_STRANGERS':str(d/'tg-strangers.log'), 'MESH_ROZ_OFFSET':str(d/'offset'), 'MESH_ROZ_IN_LOG':str(d/'roz-in.log'), 'MESH_ROZ_LOCK':str(d/'lock'), 'MESH_TEST_CALLS':str(d/'calls'), 'MESH_ROZ_WINDOW':'tg-roz'}

def run(d, env): return subprocess.run([str(SCRIPT)], env=env, capture_output=True, text=True)

class RozChannelDelivery(unittest.TestCase):
    def test_unwritable_receipt_is_detected_before_delivery(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); (d/'tg-strangers.log').write_text('2026-09-16T00:00:00Z  from=12  "hi"\n')
            (d/'roz-in.log').mkdir(); env=setup_env(d)
            self.assertNotEqual(run(d,env).returncode,0)
            self.assertFalse((d/'calls').exists())

    def test_partial_input_waits_for_newline(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); source=d/'tg-strangers.log'
            source.write_text('2026-09-16T00:00:00Z  from=12  "hello"')
            env=setup_env(d); self.assertEqual(run(d,env).returncode,0)
            self.assertFalse((d/'calls').exists())
            with source.open('a') as handle: handle.write('\n')
            self.assertEqual(run(d,env).returncode,0)
            self.assertEqual(len((d/'calls').read_text().splitlines()),1)

    def test_truncated_source_is_not_healthy(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); (d/'tg-strangers.log').write_text('')
            (d/'offset').write_text('9\n'); env=setup_env(d)
            self.assertNotEqual(run(d,env).returncode,0)
            self.assertEqual((d/'offset').read_text(),'9\n')

    def test_failed_first_retries_same_message(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); d/'tg-strangers.log'
            (d/'tg-strangers.log').write_text('2026-09-16T00:00:00Z  from=12  "hello"\n')
            env=setup_env(d, tell='fail-first'); r=run(d,env); self.assertNotEqual(r.returncode,0); self.assertFalse((d/'offset').exists())
            r=run(d,env); self.assertEqual(r.returncode,0); self.assertEqual(len((d/'calls').read_text().splitlines()),2); self.assertEqual(len((d/'roz-in.log').read_text().splitlines()),1)
    def test_second_failure_does_not_replay_first(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); (d/'tg-strangers.log').write_text('2026-09-16T00:00:00Z  from=12  "one"\n2026-09-16T00:00:01Z  from=12  "two"\n')
            env=setup_env(d); env['MESH_TEST_FAIL_ON']='2'
            # Replace stub with deterministic second-call failure.
            (d/'bin/mesh-tell').write_text('#!/bin/sh\nn=$(wc -l < "$MESH_TEST_CALLS" 2>/dev/null || echo 0); n=$((n+1)); printf "%s|%s" "$n" "$*" | tr "\\n" " " >> "$MESH_TEST_CALLS"; printf "\\n" >> "$MESH_TEST_CALLS"; [ "$n" -ne 2 ]\n'); (d/'bin/mesh-tell').chmod(0o755)
            r=run(d,env); self.assertNotEqual(r.returncode,0); self.assertEqual(len((d/'roz-in.log').read_text().splitlines()),1); self.assertEqual((d/'offset').read_text().strip(),'1')
            self.assertEqual(run(d,env).returncode,0); calls=(d/'calls').read_text().splitlines(); self.assertEqual(len(calls),3); self.assertIn('two',calls[-1]); self.assertNotIn('one',calls[-1])
    def test_exact_sender_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); (d/'tg-strangers.log').write_text('2026-09-16T00:00:00Z  from=123  "other"\n2026-09-16T00:00:01Z  from=12  "mine"\n')
            env=setup_env(d); self.assertEqual(run(d,env).returncode,0); self.assertEqual(len((d/'calls').read_text().splitlines()),1); self.assertEqual((d/'offset').read_text().strip(),'2')
    def test_sequential_duplicate_run_no_delivery(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); (d/'tg-strangers.log').write_text('2026-09-16T00:00:00Z  from=12  "one"\n'); env=setup_env(d); self.assertEqual(run(d,env).returncode,0); self.assertEqual(run(d,env).returncode,0); self.assertEqual(len((d/'calls').read_text().splitlines()),1)
    def test_missing_window_keeps_pending(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td); (d/'tg-strangers.log').write_text('2026-09-16T00:00:00Z  from=12  "one"\n'); env=setup_env(d,tmux='missing'); r=run(d,env); self.assertNotEqual(r.returncode,0); self.assertFalse((d/'offset').exists())

if __name__=='__main__': unittest.main()
