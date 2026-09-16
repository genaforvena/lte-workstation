#!/usr/bin/env python3
"""Restore must work without an injected identity and must report reader failures."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/mesh-codex-context"


class ContextTest(unittest.TestCase):
    def run_restore(self, response, **overrides):
        with tempfile.TemporaryDirectory() as td:
            stub = Path(td) / "handoff"
            stub.write_text("#!/bin/bash\n" + response)
            stub.chmod(0o755)
            env = {key: value for key, value in os.environ.items()
                   if key not in ("MESH_WHO", "MESH_CODEX_WINDOW", "MESH_HANDOFF_TEST_WINDOW")}
            env.update(MESH_HANDOFF_BIN=str(stub), **overrides)
            return subprocess.run(["bash", str(SCRIPT)], env=env, text=True,
                                  capture_output=True)

    def test_unset_identity_uses_handoff_discovery(self):
        result = self.run_restore("echo '{\"hookSpecificOutput\":{\"additionalContext\":\"discovered charter\"}}'\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("discovered charter", result.stdout)

    def test_identity_precedence(self):
        for values, expected in [({"MESH_WHO": "job@node"}, "job"),
                                 ({"MESH_WHO": "job@node", "MESH_CODEX_WINDOW": "tg"}, "tg")]:
            payload = json.dumps({"hookSpecificOutput": {"additionalContext": expected}})
            result = self.run_restore(
                f'[ "$MESH_HANDOFF_TEST_WINDOW" = "{expected}" ] || exit 9\n'
                f"echo '{payload}'\n", **values)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), expected)

    def test_failed_restore_is_not_empty_success(self):
        result = self.run_restore("echo 'ledger unavailable' >&2\nexit 7\n", MESH_WHO="job")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ledger unavailable", result.stderr)

    def test_malformed_restore_is_not_empty_success(self):
        result = self.run_restore("echo '{broken'\n", MESH_WHO="job")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid restore payload", result.stderr)

    def test_no_context_is_valid(self):
        result = self.run_restore("exit 0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no charter or handoff", result.stdout)


if __name__ == "__main__":
    unittest.main()
