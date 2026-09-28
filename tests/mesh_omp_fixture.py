"""Route only a test Mind's model invocation to a local OMP fixture.

Witness preflight still resolves and hashes the installed OMP executable.
"""
import os
from pathlib import Path


def wire_omp_fixture(root: Path, env: dict, fixture: Path) -> None:
    site = root / "python-site"
    site.mkdir(parents=True, exist_ok=True)
    (site / "sitecustomize.py").write_text(
        "import os, subprocess\n"
        "_real_run = subprocess.run\n"
        "def _run(args, *pos, **kw):\n"
        "    if (isinstance(args, (list, tuple)) and args and args[0] == 'omp'\n"
        "            and '--print' in args and os.environ.get('MESH_TEST_OMP_FIXTURE')):\n"
        "        args = [os.environ['MESH_TEST_OMP_FIXTURE'], *args[1:]]\n"
        "    return _real_run(args, *pos, **kw)\n"
        "subprocess.run = _run\n",
        encoding="utf-8",
    )
    env.pop("MESH_MISHE_OMP_CMD", None)
    env["MESH_TEST_OMP_FIXTURE"] = str(fixture)
    env["PYTHONPATH"] = str(site) + os.pathsep + env.get("PYTHONPATH", "")
