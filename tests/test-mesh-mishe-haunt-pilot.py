#!/usr/bin/env python3
"""A source-pinned report cannot be replaced or redirected on retry."""
from pathlib import Path
import runpy
import tempfile
import unittest


ADAPTER = Path(__file__).resolve().parents[1] / "scripts/haunt/mesh-haunt-mishe"


class HauntPilotReportTests(unittest.TestCase):
    def test_report_identity_collision_and_symlink_refuse_without_overwrite(self):
        write_immutable = runpy.run_path(str(ADAPTER))["write_immutable"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "reports" / "pinned.json"
            write_immutable(report, b'{"verdict":"BLIND"}\n')
            self.assertEqual(report.read_bytes(), b'{"verdict":"BLIND"}\n')
            write_immutable(report, b'{"verdict":"BLIND"}\n')
            with self.assertRaisesRegex(ValueError, "identity collision"):
                write_immutable(report, b'{"verdict":"FINDING"}\n')
            self.assertEqual(report.read_bytes(), b'{"verdict":"BLIND"}\n')
            redirect = root / "reports" / "redirect.json"
            redirect.symlink_to(report)
            with self.assertRaisesRegex(ValueError, "report symlink"):
                write_immutable(redirect, b'{"verdict":"FINDING"}\n')
            self.assertEqual(report.read_bytes(), b'{"verdict":"BLIND"}\n')


if __name__ == "__main__":
    unittest.main()
