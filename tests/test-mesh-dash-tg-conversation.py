import os, pathlib, subprocess, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class TgConversation(unittest.TestCase):
    def test_both_directions_chronological_bounded_and_private(self):
        with tempfile.TemporaryDirectory() as directory:
            home = pathlib.Path(directory); mesh = home / '.mesh'; mesh.mkdir()
            (mesh / 'voice-in.log').write_text(''.join(
                f'2026-09-16T00:00:0{i}Z  TEXT  inbound-{i}\n' for i in range(5)))
            (mesh / 'tg-sent.log').write_text(''.join(
                f'2026-09-16T00:00:0{i}Z  outbound-{i}\n' for i in (3,5,6)))
            (mesh / 'roz-in.log').write_text('PRIVATE_ROZ_NOT_FOR_TG\n')
            env = dict(os.environ, HOME=str(home), MESH_DIR=str(mesh), MESH_DASH_FAST='1')
            result = subprocess.run([str(ROOT / 'scripts/mesh-dash'), '--once', 'tg'],
                                    env=env, text=True, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('-- conversation (last 3 each)', result.stdout)
            rows = [r for r in result.stdout.splitlines() if r.startswith('2026-')]
            self.assertEqual(len(rows), 6, result.stdout)
            self.assertTrue(any('[IN]' in row for row in rows))
            self.assertTrue(any('[OUT]' in row for row in rows))
            self.assertEqual([r.split()[0] for r in rows], sorted(r.split()[0] for r in rows))
            self.assertNotIn('PRIVATE_ROZ_NOT_FOR_TG', result.stdout)

if __name__ == '__main__': unittest.main()
