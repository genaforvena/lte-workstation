#!/usr/bin/env python3
"""Leakage-safe, small TimesFM 3.0 benchmark for wake's rolling fixtures."""
import argparse, json, os, re, resource, subprocess, time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

UTC = timezone.utc
MARKERS = ("task", "taking", "done", "fyi", "alert", "idle", "dispatch")
TS = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z)")

def dt(s): return datetime.fromisoformat(s.replace("Z", "+00:00"))
def iso(x): return x.astimezone(UTC).isoformat().replace("+00:00", "Z")

def hourly(path, value_re, transform=lambda m: float(m.group(1))):
    bins = defaultdict(list)
    for line in Path(path).open(errors="replace"):
        m = TS.search(line)
        v = value_re.search(line) if m else None
        if not (m and v): continue
        t = dt(m.group(1)).replace(minute=0, second=0, microsecond=0)
        try: bins[t].append(transform(v))
        except (TypeError, ValueError): pass
    return {t: float(np.mean(v)) for t, v in bins.items() if v}

def chat_hourly(path):
    bins = defaultdict(Counter)
    for line in Path(path).open(errors="replace"):
        m = TS.search(line)
        if not m: continue
        t = dt(m.group(1)).replace(minute=0, second=0, microsecond=0)
        bins[t]["all_rows"] += 1
        for marker in MARKERS:
            if f"[{marker}]" in line: bins[t][marker] += 1
    return {k: float(v["all_rows"]) for k, v in bins.items()}

def aligned(series, start, end):
    hours = []
    vals = []
    t = start
    while t < end:
        hours.append(t); vals.append(series.get(t, np.nan)); t += timedelta(hours=1)
    return np.asarray(hours), np.asarray(vals, dtype=float)

def metrics(y, pred):
    e = pred - y
    return {"mae": float(np.mean(np.abs(e))), "rmse": float(np.sqrt(np.mean(e * e))), "n": int(y.size)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("/home/mesh-home/.mesh"))
    ap.add_argument("--fixture", type=Path, default=Path("docs/wake-model-eval-fixtures-20260909.json"))
    ap.add_argument("--out", type=Path, default=Path("docs/wake-timesfm-bench-20260909.json"))
    ap.add_argument("--model", default="google/timesfm-3.0-pytorch")
    args = ap.parse_args()
    fixture = json.loads(args.fixture.read_text())
    split = fixture["splits"]
    train_end, val_start, val_end, test_start, test_end = map(dt, [split["train"]["end_exclusive"], split["validation"]["start"], split["validation"]["end_exclusive"], split["test"]["start"], split["test"]["end_exclusive"]])
    start = dt(split["train"]["start"]).replace(minute=0, second=0, microsecond=0)
    test_end = dt(split["test"]["end_exclusive"])
    test_end = (test_end + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    series = {
        "chat_all_rows": chat_hourly(args.root / "chat.log"),
        "power_watts": hourly(args.root / "power.log", re.compile(r"\s([0-9]+(?:\.[0-9]+)?)\s+")),
        "package_power_watts": hourly(args.root / "package-power.log", re.compile(r"\]\s+[^—]+—\s*([0-9]+(?:\.[0-9]+)?)\s+W")),
    }
    # Load only after parsing, so a model failure still leaves input inventory in the artifact.
    result = {"schema": "wake-timesfm-bench/v1", "created_at": iso(datetime.now(UTC)), "model": args.model,
              "fixture": str(args.fixture), "split": split, "series": {}, "status": "MEASURED", "failures": []}
    try:
        import torch, timesfm
        t0 = time.perf_counter()
        forecaster = timesfm.TimesFM3Forecaster.from_pretrained(args.model, device="cuda" if torch.cuda.is_available() else "cpu")
        load_s = time.perf_counter() - t0
        device = "cuda" if torch.cuda.is_available() else "cpu"
    except Exception as exc:
        result["status"] = "UNMEASURED"; result["failures"].append({"phase":"load", "type":type(exc).__name__, "message":str(exc)})
        args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n"); print(json.dumps(result)); return 2
    for name, values in series.items():
        hours, vals = aligned(values, start, test_end)
        # only score regular observations with six hours of history and a complete six-hour target.
        rows = {"source_rows": len(values), "observed_hours": int(np.isfinite(vals).sum()), "horizon_hours": 6, "baselines": {}, "timesfm": {}}
        for label, lo, hi in (("validation", val_start, val_end), ("test", test_start, test_end)):
            idx = np.where((hours >= lo) & (hours < hi))[0]
            candidates = [i for i in idx if i >= 32 and i + 6 <= len(vals) and np.isfinite(vals[i-32:i]).all() and np.isfinite(vals[i:i+6]).all()]
            if not candidates:
                rows[label] = {"valid_windows": 0, "status":"UNMEASURED"}; continue
            # Freeze selection on validation; report validation and untouched test separately.
            out = {"valid_windows": len(candidates)}
            for baseline in ("persistence", "seasonal-24", "drift"):
                ys=[]; ps=[]
                for i in candidates:
                    if baseline == "persistence": p = np.repeat(vals[i-1], 6)
                    elif baseline == "seasonal-24" and i >= 24: p = vals[i-24:i-18]
                    elif baseline == "drift": p = vals[i-1] + (vals[i-1] - vals[i-2]) * np.arange(1,7)
                    else: continue
                    ys.extend(vals[i:i+6]); ps.extend(p)
                out[baseline] = metrics(np.asarray(ys), np.asarray(ps)) if ys else {"status":"UNMEASURED"}
            ys=[]; ps=[]; lows=[]; highs=[]; lat=[]
            for i in candidates:
                t1=time.perf_counter(); fo=forecaster.predict(vals[i-32:i], horizon=6, return_quantiles=True); lat.append(time.perf_counter()-t1)
                p=np.asarray(fo.forecast).reshape(-1)[:6]; ys.extend(vals[i:i+6]); ps.extend(p)
                q=np.asarray(fo.quantiles)
                if q.ndim == 2 and q.shape[1] >= 9:
                    lows.extend(q[:6, 0]); highs.extend(q[:6, 8])
            tm = {**metrics(np.asarray(ys), np.asarray(ps)), "mean_latency_s":float(np.mean(lat)), "p95_latency_s":float(np.percentile(lat,95))}
            if lows:
                yy=np.asarray(ys); lo=np.asarray(lows); hi=np.asarray(highs)
                tm.update({"p10_p90_coverage":float(np.mean((yy >= lo) & (yy <= hi))), "p10_p90_mean_width":float(np.mean(hi-lo))})
            out["timesfm"] = tm
            rows[label]=out
        rows["load_seconds"] = load_s if name == next(iter(series)) else None
        rows["device"] = device
        result["series"][name] = rows
    if torch.cuda.is_available(): result["gpu_peak_allocated_mb"] = round(torch.cuda.max_memory_allocated()/1024**2, 1)
    result["max_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)
    result["git_revision"] = subprocess.check_output(["git","-C","/home/mesh-home/finnegans-fake","rev-parse","HEAD"], text=True).strip()
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out":str(args.out),"status":result["status"],"device":device,"load_seconds":load_s}))

if __name__ == "__main__": main()
