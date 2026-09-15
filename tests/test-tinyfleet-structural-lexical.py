#!/usr/bin/env python3
"""End-to-end contract test for pinned structural/lexical measurements."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "tinyfleet_structural_lexical.py"


def run(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True)


def main():
    with tempfile.TemporaryDirectory(prefix="tinyfleet-measure-test-") as temp:
        base = pathlib.Path(temp)
        repo = base / "repo"
        repo.mkdir()
        run("git", "init", "-q", str(repo))
        run("git", "-C", str(repo), "config", "user.email", "test@example.invalid")
        run("git", "-C", str(repo), "config", "user.name", "Test")
        (repo / "src").mkdir()
        sample_text = "import json\n\ndef public_api(value):\n    try:\n        return json.dumps(value)\n    except ValueError:\n        raise\n"
        (repo / "src" / "sample.py").write_text(sample_text, encoding="utf-8")
        (repo / "README.md").write_text("sample token sample\n", encoding="utf-8")
        (repo / "bad.py").write_bytes(b"\xff\xfe")
        run("git", "-C", str(repo), "add", ".")
        run("git", "-C", str(repo), "commit", "-qm", "fixture")
        commit = run("git", "-C", str(repo), "rev-parse", "HEAD").stdout.strip()
        manifest = base / "corpus.json"
        manifest.write_text(json.dumps({
            "schema": "tiny-fleet-corpus-manifest/v1",
            "candidates": [{
                "candidate_id": "fixture-python",
                "repo_path": str(repo),
                "commit": commit,
                "status": "resolved-local",
                "license_spdx": "MIT",
                "snapshot": {"commit": commit},
            }],
        }), encoding="utf-8")
        protocol = base / "protocol.md"
        protocol.write_text("frozen test protocol\n", encoding="utf-8")
        out = base / "out"
        run(sys.executable, str(TOOL), "--corpus-manifest", str(manifest),
            "--protocol", str(protocol), "--output-dir", str(out),
            "--bootstrap-rounds", "100")

        rows = [line.split("\t") for line in (out / "file-rows.tsv").read_text().splitlines()]
        header = rows[0]
        data = [dict(zip(header, row)) for row in rows[1:]]
        assert len(data) == 3
        assert sum(row["status"] == "included" for row in data) == 2
        malformed = next(row for row in data if row["path"] == "bad.py")
        assert malformed["status"] == "excluded"
        assert malformed["reason"] == "malformed-encoding"
        sample = next(row for row in data if row["path"] == "src/sample.py")
        assert sample["token_count"] == "13"
        assert sample["import_count"] == "1"
        assert sample["declaration_count"] == "1"
        assert sample["parse_status"] == "parsed"
        assert sample["sha256"] == hashlib.sha256(sample_text.encode()).hexdigest()

        summary = json.loads((out / "summary.json").read_text())
        assert summary["provenance"]["repositories"][0]["commit"] == commit
        assert summary["metrics"]["paired_snapshot_change"]["status"] == "na"
        assert summary["metrics"]["repository_architecture"]["status"] == "na"
        assert summary["metrics"]["lora_qlora"]["status"] == "blocked"
        assert {row["stratum"] for row in summary["metrics"]["repository_language_strata"]} == {"markdown", "python"}
        assert summary["denominators"]["candidate_files"] == 3
        assert summary["denominators"]["included_files"] == 2
        terms = (out / "term-counts.tsv").read_text()
        assert "sample\t" in terms
        repeat = base / "repeat"
        run(sys.executable, str(TOOL), "--corpus-manifest", str(manifest),
            "--protocol", str(protocol), "--output-dir", str(repeat),
            "--bootstrap-rounds", "100")
        for filename in ("summary.json", "file-rows.tsv", "term-counts.tsv", "repository-language-strata.tsv"):
            assert (out / filename).read_bytes() == (repeat / filename).read_bytes(), filename
    print("ok: pinned structural/lexical extraction, missingness, and explicit unavailable arms")


if __name__ == "__main__":
    main()
