import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/study")
NAMES = ["flask-old", "flask-new", "requests-old", "requests-new", "pydantic-old", "pydantic-new"]


def run(argv, *, cwd=None, env=None, log=None):
    completed = subprocess.run(argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if log is not None:
        Path(log).write_text(completed.stdout)
    return completed.returncode, completed.stdout


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for relative in ("envs", "logs", "requirements", "tmp", "home"):
        (ROOT / relative).mkdir(exist_ok=True)

    metadata = {
        "python": sys.version,
        "platform": platform.platform(),
        "run_started_epoch": time.time(),
        "additional_apt_build_dependencies": [],
    }
    metadata["openssl"] = run(["openssl", "version"])[1].strip()
    results = []

    for name in NAMES:
        source = ROOT / "work" / name
        venv = ROOT / "envs" / name
        tmp = ROOT / "tmp" / name
        home = ROOT / "home" / name
        tmp.mkdir(exist_ok=True)
        home.mkdir(exist_ok=True)
        req_path = ROOT / "requirements" / f"{name}.txt"
        lines = []
        for line in (Path("/freeze") / f"{name}.txt").read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#") or line.startswith("-e "):
                continue
            if name == "flask-old" and line.split("==", 1)[0].lower() in {"jinja2", "markupsafe", "werkzeug"}:
                continue
            if name == "requests-new" and line.startswith("greenlet=="):
                continue
            if name == "pydantic-old" and line.lower().startswith("mypy_extensions=="):
                continue
            lines.append(line)
        if name == "flask-old":
            lines.extend(["Jinja2==3.1.2", "MarkupSafe==2.1.5"])
            lines.append("Werkzeug==2.2.2")
        if name == "requests-new":
            lines.append("greenlet==2.0.2")
        if name == "pydantic-old":
            lines.append("mypy_extensions==0.4.3")
        lines.append(f"-e {source}")
        req_path.write_text("\n".join(lines) + "\n")

        create_rc, create_out = run([sys.executable, "-m", "venv", str(venv)])
        (ROOT / "logs" / f"{name}-venv.log").write_text(create_out)
        pip = str(venv / "bin/python")
        install_rc, install_out = run([pip, "-m", "pip", "install", "--disable-pip-version-check", "-r", str(req_path)])
        (ROOT / "logs" / f"{name}-install.log").write_text(install_out)
        freeze_rc, freeze_out = run([pip, "-m", "pip", "freeze"])
        (ROOT / "envs" / f"{name}.freeze.txt").write_text(freeze_out)
        test_rc = None
        test_out = ""
        if create_rc == 0 and install_rc == 0:
            test_env = os.environ.copy()
            source_path = source / "src" if (source / "src").is_dir() else source
            test_env.update({"HOME": str(home), "TMPDIR": str(tmp), "PYTHONPATH": str(source_path), "PYTHONUNBUFFERED": "1"})
            test_rc, test_out = run([pip, "-m", "pytest", "-q", "tests"], cwd=source, env=test_env)
            (ROOT / "logs" / f"{name}-pytest.log").write_text(test_out)
        results.append({
            "suite": name,
            "venv_exit": create_rc,
            "install_exit": install_rc,
            "freeze_exit": freeze_rc,
            "pytest_exit": test_rc,
            "pytest_tail": test_out[-1000:],
        })
        print(f"{name}: venv={create_rc} install={install_rc} freeze={freeze_rc} pytest={test_rc}", flush=True)

    metadata["run_finished_epoch"] = time.time()
    metadata["suites"] = results
    (ROOT / "results.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(results, indent=2), flush=True)
    return 0 if all(row["pytest_exit"] == 0 for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
