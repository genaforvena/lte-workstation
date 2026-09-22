#!/usr/bin/env python3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "job" / "mesh-job-project-map"
result = subprocess.run([str(TOOL), "--test"], text=True, capture_output=True)
if result.returncode:
    raise SystemExit("project-map focused test failed:\n%s\n%s" % (result.stdout, result.stderr))
print(result.stdout.strip())
