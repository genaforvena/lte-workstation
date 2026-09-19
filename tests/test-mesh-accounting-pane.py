#!/usr/bin/env python3
"""The health pane reports accounting results with source freshness."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]


class AccountingPaneTests(unittest.TestCase):
    def render(self, content):
        source = (REPO / "scripts/mesh-dash").read_text()
        self.assertIn("render_accounting_reconciliation(){", source)
        body = source.split("render_accounting_reconciliation(){", 1)[1].split("\n}\n", 1)[0]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            if content is not None:
                (root / "reconciliation").mkdir()
                (root / "reconciliation/latest.txt").write_text(content)
            got = subprocess.run(["bash", "-c", "render_accounting_reconciliation(){" + body +
                                  '\n}\nM="$1"; render_accounting_reconciliation', "test", temp],
                                 capture_output=True, text=True, timeout=5)
            self.assertEqual(got.returncode, 0, got.stderr)
            return got.stdout

    def test_current_results_remain_distinct(self):
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        text = self.render(f"cutoff={now}\nsource=ledger status=KNOWN verdict=PASS\n"
                           "source=labor status=KNOWN verdict=FAIL\n"
                           "source=promises status=UNKNOWN reason=timeout\n")
        for token in ("ledger=PASS", "labor=FAIL", "promises=UNKNOWN(timeout)", "age="):
            self.assertIn(token, text)

    def test_missing_and_stale_reports_never_render_as_current_pass(self):
        self.assertIn("UNKNOWN", self.render(None))
        text = self.render("cutoff=2000-01-01T00:00:00Z\nsource=labor status=KNOWN verdict=PASS\n")
        self.assertIn("STALE", text)
        self.assertNotIn("labor=PASS", text)


if __name__ == "__main__":
    unittest.main()
