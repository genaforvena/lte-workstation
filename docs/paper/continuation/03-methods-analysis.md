# Methods and analysis contract

## Study design

This is a bounded mixed-method case study. First, the manuscript defines each failure class as a
decision procedure over source or runtime evidence. Second, it records one live incident and its
commit or measurement artifact. Third, detectors are exercised against the studied repository and
a bounded comparison corpus where the procedure is decidable. Undecidable and unrun cases remain
separate categories.

## Units and denominators

- D1 denominator: decidable boolean self-source-grep gates, with undecidable pattern sites shown
  separately; comparison files are a bounded convenience sample, not a population.
- D2 denominator: detected fallback sites with a decidable failure substitute; numeric domains
  whose success meaning cannot be inferred statically stay undecidable or explicitly qualified.
- D3 denominator: tools carrying a cadence header and having enough evidence to grade interval
  coverage; the ungraded bucket is reported, not silently excluded.

## Analysis rules

1. A detector must have a self-test and mutation/control evidence before its output is treated as
   a measurement.
2. A source-text match is not execution evidence; source-only and runtime cases are labelled
   separately.
3. Rates use the detector's actual eligible denominator; `0/0` is undefined.
4. A sample narrower than its cadence is reported with `coverage = window / cadence`; it is not
   promoted to a state estimate.
5. The tiny-fleet pilot's bootstrap intervals are file-level uncertainty only. Leakage failure,
   blocked training, and missing behavioural evidence prevent generalization claims.

## Reproduction commands

```sh
docs/paper/detectors/d1_self_grepping_gate.py --selftest
docs/paper/detectors/d1_self_grepping_gate.py scripts
docs/paper/detectors/d2_silent_fallback.py --selftest
docs/paper/detectors/d2_silent_fallback.py scripts
docs/paper/detectors/d3_window_under_cadence.py --selftest
docs/paper/detectors/d3_window_under_cadence.py scripts
bash tests/test-mesh-tiny-fleet-evaluator.sh
bash tests/test-mesh-tiny-fleet-validation.sh
```

The final review artifact must capture each command's individual stdout and exit status.
