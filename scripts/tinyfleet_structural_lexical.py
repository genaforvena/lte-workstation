#!/usr/bin/env python3
"""Extract deterministic, pinned structural and lexical features from a corpus lock."""
import argparse
import collections
import hashlib
import json
import pathlib
import random
import re
import subprocess


SCHEMA = "tiny-fleet-structural-lexical/v1"
MAX_BYTES = 1_048_576
TEXT_EXTENSIONS = {
    ".sh", ".bash", ".py", ".md", ".txt", ".json", ".tsv", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".conf", ".c", ".h", ".cc", ".hh", ".cpp",
    ".hpp", ".rs", ".go", ".js", ".jsx", ".ts", ".tsx", ".java", ".kt",
    ".rb", ".pl", ".lua", ".sql", ".html", ".css", ".xml", ".make", ".mk",
    ".dockerfile", ".proto", ".r", ".jl", ".php", ".swift", ".ex", ".exs",
    ".scala", ".sc", ".vue", ".svelte", ".gradle", ".patch", ".diff",
}
LANGUAGE = {
    ".sh": "shell", ".bash": "shell", ".py": "python", ".md": "markdown",
    ".txt": "text", ".json": "json", ".tsv": "tsv", ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml", ".ini": "config", ".cfg": "config", ".conf": "config",
    ".c": "c", ".h": "c", ".cc": "cpp", ".hh": "cpp", ".cpp": "cpp", ".hpp": "cpp",
    ".rs": "rust", ".go": "go", ".js": "javascript", ".jsx": "javascript",
    ".ts": "typescript", ".tsx": "typescript", ".java": "java", ".kt": "kotlin",
    ".rb": "ruby", ".pl": "perl", ".lua": "lua", ".sql": "sql", ".html": "html",
    ".css": "css", ".xml": "xml", ".mk": "make", ".proto": "protobuf", ".r": "r",
    ".jl": "julia", ".php": "php", ".swift": "swift", ".ex": "elixir", ".exs": "elixir",
    ".scala": "scala", ".sc": "scala", ".vue": "vue", ".svelte": "svelte",
    ".gradle": "gradle", ".patch": "patch", ".diff": "patch",
}
TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
GENERATED_PARTS = {"generated", "vendor", "vendors", "third_party", "third-party", "node_modules"}
LOCK_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "Cargo.lock", "go.sum"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def pinned_entries(repo, commit):
    tree = git(repo, "ls-tree", "-rz", "--full-tree", commit)
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8", "surrogateescape")
        yield mode, kind, oid, path


def blob_text(repo, oid):
    return subprocess.run(["git", "-C", str(repo), "cat-file", "blob", oid], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def exclusion_reason(mode, kind, path):
    p = pathlib.PurePosixPath(path)
    lower_parts = {part.lower() for part in p.parts}
    if mode == "120000":
        return "symlink"
    if kind != "blob":
        return "non-blob"
    if lower_parts & GENERATED_PARTS or p.name.endswith((".generated", ".min.js", ".min.css")):
        return "generated-or-vendored"
    if p.name in LOCK_NAMES:
        return "lockfile-separate-arm"
    if p.suffix.lower() not in TEXT_EXTENSIONS and p.name.lower() not in {"makefile", "dockerfile"}:
        return "unsupported-extension"
    return None


def metrics_for(text, path, size, sha256):
    ext = pathlib.PurePosixPath(path).suffix.lower()
    language = LANGUAGE.get(ext, "make" if pathlib.PurePosixPath(path).name.lower() in {"makefile", "dockerfile"} else "unknown")
    lines = text.splitlines()
    tokens = [token.lower() for token in TOKEN.findall(text)]
    import_re = {
        "python": re.compile(r"^\s*(?:from\s+\S+\s+import\b|import\s+\S+)", re.M),
        "shell": re.compile(r"^\s*(?:source\s+|\.\s+)", re.M),
        "go": re.compile(r"^\s*import\s+(?:\(|[\"`])", re.M),
        "rust": re.compile(r"^\s*(?:use|extern\s+crate)\s+", re.M),
        "javascript": re.compile(r"^\s*(?:import\b|require\s*\()", re.M),
        "typescript": re.compile(r"^\s*(?:import\b|require\s*\()", re.M),
        "c": re.compile(r"^\s*#\s*include\b", re.M),
        "cpp": re.compile(r"^\s*#\s*include\b", re.M),
    }
    declaration_re = {
        "python": re.compile(r"^\s*(?:async\s+)?(?:def|class)\s+\w+", re.M),
        "shell": re.compile(r"^\s*(?:function\s+\w+|\w+\s*\(\s*\)\s*\{)", re.M),
        "go": re.compile(r"^\s*func\s+(?:\([^)]*\)\s*)?\w+", re.M),
        "rust": re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?(?:fn|struct|enum|trait)\s+\w+", re.M),
        "javascript": re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+\w+", re.M),
        "typescript": re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+\w+", re.M),
    }
    imports = len(import_re[language].findall(text)) if language in import_re else None
    declarations = len(declaration_re[language].findall(text)) if language in declaration_re else None
    comment_lines = sum(bool(re.match(r"^\s*(?:#|//|/\*|\*|<!--)", line)) for line in lines)
    test_lines = sum(bool(re.search(r"\b(?:test|tests|unittest|pytest|describe|it)\b", line, re.I)) for line in lines)
    error_lines = sum(bool(re.search(r"\b(?:try|catch|except|Result<|Error|raise|throw)\b", line)) for line in lines)
    parse_status, parse_nodes, parse_error = "na", None, None
    if language == "python":
        import ast
        try:
            tree = ast.parse(text)
            parse_status = "parsed"
            parse_nodes = sum(1 for _ in ast.walk(tree))
        except SyntaxError as exc:
            parse_status, parse_error = "parse-error", f"line-{exc.lineno or 0}"
    return {
        "path": path, "status": "included", "reason": "", "bytes": size,
        "sha256": sha256, "extension": ext or "[none]", "language": language,
        "line_count": len(lines), "token_count": len(tokens), "identifier_count": len(tokens),
        "vocabulary_size": len(set(tokens)), "comment_line_count": comment_lines,
        "import_count": imports if imports is not None else "na",
        "declaration_count": declarations if declarations is not None else "na",
        "test_marker_line_count": test_lines, "error_handling_line_count": error_lines,
        "parse_status": parse_status, "parse_node_count": parse_nodes if parse_nodes is not None else "na",
        "parse_error": parse_error or "", "tokens": tokens,
    }


def bootstrap(values, seed, rounds):
    if not values:
        return {"estimate": "na", "lower": "na", "upper": "na", "n": 0, "method": "na"}
    rng = random.Random(seed)
    samples = []
    for _ in range(rounds):
        samples.append(sum(values[rng.randrange(len(values))] for _ in values) / len(values))
    samples.sort()
    return {"estimate": sum(values) / len(values),
            "lower": samples[int(0.025 * (rounds - 1))],
            "upper": samples[int(0.975 * (rounds - 1))],
            "n": len(values), "method": "percentile bootstrap over files within repository",
            "seed": seed, "rounds": rounds}


def tsv(path, columns, rows):
    def cell(value):
        if value is None:
            return "na"
        if isinstance(value, (dict, list)):
            value = json.dumps(value, sort_keys=True, separators=(",", ":"))
        value = str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ")
        return value
    path.write_text("\t".join(columns) + "\n" + "".join(
        "\t".join(cell(row.get(col)) for col in columns) + "\n" for row in rows), encoding="utf-8")


def summarize(repo_rows, rounds, seed):
    included = [r for r in repo_rows if r["status"] == "included"]
    for row in repo_rows:
        row["stratum"] = row["language"] if row["status"] == "included" else "na"
    langs = collections.Counter(r["language"] for r in included)
    token_counter = collections.Counter(token for row in included for token in row["tokens"])
    values = {
        "candidate_files": len(repo_rows), "included_files": len(included),
        "excluded_files": len(repo_rows) - len(included),
        "included_bytes": sum(r["bytes"] for r in included),
        "line_count": sum(r["line_count"] for r in included),
        "token_count": sum(r["token_count"] for r in included),
        "identifier_count": sum(r["identifier_count"] for r in included),
        "vocabulary_size": len(token_counter), "comment_line_count": sum(r["comment_line_count"] for r in included),
        "test_marker_line_count": sum(r["test_marker_line_count"] for r in included),
        "error_handling_line_count": sum(r["error_handling_line_count"] for r in included),
        "parse_files": sum(r["parse_status"] == "parsed" for r in included),
        "parse_errors": sum(r["parse_status"] == "parse-error" for r in included),
        "python_files": sum(r["language"] == "python" for r in included),
        "parse_node_count": sum(int(r["parse_node_count"]) for r in included if str(r["parse_node_count"]).isdigit()),
        "language_file_counts": dict(sorted(langs.items())),
        "extension_file_counts": dict(sorted(collections.Counter(r["extension"] for r in included).items())),
        "import_count": sum(int(r["import_count"]) for r in included if str(r["import_count"]).isdigit()),
        "import_count_missing_files": sum(r["import_count"] == "na" for r in included),
        "declaration_count": sum(int(r["declaration_count"]) for r in included if str(r["declaration_count"]).isdigit()),
        "declaration_count_missing_files": sum(r["declaration_count"] == "na" for r in included),
        "top_terms": token_counter.most_common(50),
        "marker_rates": {
            "comment_marker_lines_per_line": (sum(r["comment_line_count"] for r in included) / sum(r["line_count"] for r in included)) if sum(r["line_count"] for r in included) else "na",
            "test_marker_lines_per_line": (sum(r["test_marker_line_count"] for r in included) / sum(r["line_count"] for r in included)) if sum(r["line_count"] for r in included) else "na",
            "error_handling_marker_lines_per_line": (sum(r["error_handling_line_count"] for r in included) / sum(r["line_count"] for r in included)) if sum(r["line_count"] for r in included) else "na",
            "python_parse_success_rate": (sum(r["parse_status"] == "parsed" for r in included) / sum(r["language"] == "python" for r in included)) if sum(r["language"] == "python" for r in included) else "na",
            "interpretation": "lexical marker rates; not semantic test or comment coverage",
        },
        "uncertainty": {
            "mean_bytes_per_file": bootstrap([r["bytes"] for r in included], seed, rounds),
            "mean_tokens_per_file": bootstrap([r["token_count"] for r in included], seed + 1, rounds),
            "mean_identifiers_per_file": bootstrap([r["identifier_count"] for r in included], seed + 2, rounds),
            "interpretation": "within-repository file variation only; not between-repository or temporal uncertainty",
        },
    }
    return values


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus-manifest", required=True)
    ap.add_argument("--protocol", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--bootstrap-rounds", type=int, default=2000)
    args = ap.parse_args()
    if args.bootstrap_rounds < 100:
        ap.error("--bootstrap-rounds must be at least 100")
    manifest_path, protocol_path = pathlib.Path(args.corpus_manifest), pathlib.Path(args.protocol)
    manifest_bytes, protocol_bytes = manifest_path.read_bytes(), protocol_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get("schema") != "tiny-fleet-corpus-manifest/v1":
        raise SystemExit("unsupported corpus manifest schema")
    output = pathlib.Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    all_rows, repo_summaries, term_rows = [], [], []
    resolved = [c for c in manifest.get("candidates", []) if c.get("status") == "resolved-local"]
    for index, candidate in enumerate(resolved):
        repo = pathlib.Path(candidate["repo_path"])
        locked_commit = candidate.get("commit") or candidate.get("snapshot", {}).get("commit")
        if not repo.is_dir() or not locked_commit:
            raise SystemExit(f"unreadable locked repository: {candidate.get('candidate_id')}")
        actual_commit = git(repo, "rev-parse", "--verify", f"{locked_commit}^{{commit}}").decode().strip()
        if actual_commit != locked_commit:
            raise SystemExit(f"resolved commit mismatch for {candidate['candidate_id']}: {actual_commit}")
        rows = []
        for mode, kind, oid, path in pinned_entries(repo, locked_commit):
            reason = exclusion_reason(mode, kind, path)
            raw = b"" if reason else blob_text(repo, oid)
            if not reason and len(raw) > MAX_BYTES:
                reason = "over-size-cap"
            if reason:
                row = {"path": path, "status": "excluded", "reason": reason, "bytes": len(raw) if raw else "na",
                       "sha256": digest(raw) if raw else "na", "extension": pathlib.PurePosixPath(path).suffix.lower() or "[none]",
                       "language": "na", "line_count": "na", "token_count": "na", "identifier_count": "na",
                       "vocabulary_size": "na", "comment_line_count": "na", "import_count": "na",
                       "declaration_count": "na", "test_marker_line_count": "na", "error_handling_line_count": "na",
                       "parse_status": "na", "parse_node_count": "na", "parse_error": "", "tokens": []}
            else:
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError:
                    row = {"path": path, "status": "excluded", "reason": "malformed-encoding", "bytes": len(raw),
                           "sha256": digest(raw), "extension": pathlib.PurePosixPath(path).suffix.lower() or "[none]",
                           "language": "na", "line_count": "na", "token_count": "na", "identifier_count": "na",
                           "vocabulary_size": "na", "comment_line_count": "na", "import_count": "na",
                           "declaration_count": "na", "test_marker_line_count": "na", "error_handling_line_count": "na",
                           "parse_status": "na", "parse_node_count": "na", "parse_error": "", "tokens": []}
                else:
                    row = metrics_for(text, path, len(raw), digest(raw))
            row.update({"repository": candidate["candidate_id"], "commit": locked_commit})
            rows.append(row)
        values = summarize(rows, args.bootstrap_rounds, 20260912 + index * 10)
        summary_row = {"repository": candidate["candidate_id"], "stratum": "all-languages", "commit": locked_commit, **values}
        repo_summaries.append(summary_row)
        all_rows.extend(rows)
        by_language = collections.defaultdict(list)
        for row in rows:
            if row["status"] == "included":
                by_language[row["language"]].append(row)
        for language, language_rows in sorted(by_language.items()):
            for token, count in sorted(collections.Counter(t for row in language_rows for t in row["tokens"]).items()):
                term_rows.append({"repository": candidate["candidate_id"], "stratum": language, "term": token, "count": count})

    stratum_groups = collections.defaultdict(list)
    repo_stratum_groups = collections.defaultdict(list)
    for row in all_rows:
        if row["status"] == "included":
            stratum_groups[row["language"]].append(row)
            repo_stratum_groups[(row["repository"], row["language"])].append(row)
    stratum_summaries = []
    repository_language_summaries = []
    for (repository, stratum), group in sorted(repo_stratum_groups.items()):
        terms = collections.Counter(token for row in group for token in row["tokens"])
        repository_language_summaries.append({"repository": repository, "stratum": stratum,
            "included_files": len(group), "included_bytes": sum(r["bytes"] for r in group),
            "line_count": sum(r["line_count"] for r in group), "token_count": sum(r["token_count"] for r in group),
            "vocabulary_size": len(terms),
            "mean_tokens_per_file_ci": bootstrap([r["token_count"] for r in group], 20261000 + len(repository_language_summaries), args.bootstrap_rounds),
            "uncertainty_scope": "within-repository language-stratum file resampling only"})
    for stratum, group in sorted(stratum_groups.items()):
        terms = collections.Counter(token for row in group for token in row["tokens"])
        repos = sorted({r["repository"] for r in group})
        stratum_summaries.append({"stratum": stratum, "repositories": repos,
                                  "repository_count": len(repos), "included_files": len(group),
                                  "included_bytes": sum(r["bytes"] for r in group),
                                  "token_count": sum(r["token_count"] for r in group),
                                  "vocabulary_size": len(terms),
                                  "uncertainty": "na: only one repository snapshot per repository; pooled file bootstrap would not estimate between-repository variation"})
    evaluator_commit = git(pathlib.Path(__file__).resolve().parent.parent, "rev-parse", "HEAD").decode().strip()
    evaluator_sha256 = digest(pathlib.Path(__file__).read_bytes())
    run_hash = hashlib.sha256((digest(protocol_bytes) + digest(manifest_bytes) + evaluator_commit + evaluator_sha256).encode()).hexdigest()
    summary = {
        "schema": SCHEMA,
        "run_id": run_hash,
        "provenance": {"corpus_manifest_sha256": digest(manifest_bytes), "protocol_sha256": digest(protocol_bytes),
                       "evaluator_commit": evaluator_commit, "evaluator_sha256": evaluator_sha256,
                       "repositories": [{"repository": c["candidate_id"], "commit": c.get("commit") or c.get("snapshot", {}).get("commit"),
                                         "path": str(pathlib.Path(c["repo_path"]).resolve())} for c in resolved]},
        "denominators": {"repositories": len(resolved), "candidate_files": len(all_rows),
                         "included_files": sum(r["status"] == "included" for r in all_rows),
                         "excluded_files": sum(r["status"] == "excluded" for r in all_rows),
                         "excluded_by_reason": dict(sorted(collections.Counter(r["reason"] for r in all_rows if r["status"] == "excluded").items())),
                         "files_missing_parser": sum(r["parse_status"] == "na" for r in all_rows if r["status"] == "included")},
        "metrics": {"repository_structural_lexical": repo_summaries,
                    "repository_language_strata": repository_language_summaries,
                    "stratum_structural_lexical": stratum_summaries,
                    "paired_snapshot_change": {"status": "na", "reason": "corpus lock supplies one immutable snapshot per resolved repository"},
                    "paired_lexical_change": {"js_divergence": "na", "new_vocabulary": "na", "gone_vocabulary": "na", "reason": "no paired immutable snapshots in the corpus lock"},
                    "repository_architecture": {"status": "na", "reason": "no pinned cross-language package/import graph resolver in this measurement pass"},
                    "architecture_submeasures": {"dependency_graph": "na", "package_graph": "na", "API_matching_across_paths": "na", "component_churn": "na", "reason": "no cross-language graph or declaration matcher supplied"},
                    "ast_parse_features": {"status": "partial", "measured": "Python AST node counts and parse status", "other_languages": "na: parser not supplied"},
                    "lora_qlora": {"status": "blocked", "reason": "this task measures static source features; no genuine adapter/run evidence supplied"}},
        "uncertainty": {"status": "within_repository_only", "method": "deterministic percentile bootstrap over included files",
                        "not_estimated": ["temporal change", "between-repository population uncertainty", "model/seed variability"]},
        "filter": {"extensions": sorted(TEXT_EXTENSIONS), "generated_vendor_parts": sorted(GENERATED_PARTS),
                   "lockfiles": sorted(LOCK_NAMES), "maximum_file_bytes": MAX_BYTES,
                   "normalization": "UTF-8 decode; no Unicode normalization; case-fold-like lowercase lexical tokens",
                   "token_pattern": TOKEN.pattern},
    }
    columns = ["repository", "stratum", "commit", "path", "status", "reason", "bytes", "sha256", "extension", "language",
               "line_count", "token_count", "identifier_count", "vocabulary_size", "comment_line_count", "import_count",
               "declaration_count", "test_marker_line_count", "error_handling_line_count", "parse_status", "parse_node_count", "parse_error"]
    tsv(output / "file-rows.tsv", columns, all_rows)
    tsv(output / "term-counts.tsv", ["repository", "stratum", "term", "count"], term_rows)
    tsv(output / "repository-summaries.tsv", ["repository", "stratum", "commit", "candidate_files", "included_files",
        "excluded_files", "included_bytes", "line_count", "token_count", "identifier_count", "vocabulary_size",
        "comment_line_count", "test_marker_line_count", "error_handling_line_count", "parse_files", "parse_errors", "python_files", "parse_node_count",
        "import_count", "import_count_missing_files", "declaration_count", "declaration_count_missing_files"],
        [{k: v for k, v in row.items() if k != "uncertainty" and k != "extension_file_counts" and k != "language_file_counts" and k != "top_terms"} for row in repo_summaries])
    tsv(output / "repository-language-strata.tsv", ["repository", "stratum", "included_files", "included_bytes", "line_count",
        "token_count", "vocabulary_size", "mean_tokens_per_file_ci", "uncertainty_scope"], repository_language_summaries)
    tsv(output / "stratum-summaries.tsv", ["stratum", "repositories", "repository_count", "included_files",
        "included_bytes", "token_count", "vocabulary_size", "uncertainty"], stratum_summaries)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": run_hash, "output_dir": str(output), "repositories": len(resolved),
                      "candidate_files": len(all_rows), "included_files": summary["denominators"]["included_files"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
