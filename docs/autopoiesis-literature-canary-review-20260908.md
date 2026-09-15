# Literature canary review

Date: 2026-09-08
Canary chain: `literature-canary-map-elites-20260908`
Source identifier: `review:map-elites-illumination-literature-lane-2026-07-28`

Source retained at `docs/reviews/map-elites-illumination-literature-lane-2026-07-28.md`.
That review cites Mouret & Clune, “Illuminating search spaces by mapping elites”,
arXiv:1504.04909 (2015), and maps its empty/least-covered-cell mechanism to the
mesh's 18-area × 6-angle literature descriptor grid (108 cells).

Hypothesis: in a bounded 40-emission literature sample, least-covered-cell
targeting should preserve the illumination invariant and avoid the concentration
expected from uniform redraw.

Bounded consumer predicate: `scripts/mesh-ideate --test`; acceptance requires
exit code 0 and every emitted assertion to pass. The pre-application material
price was one real invocation: 31 `ok:` assertions plus the final
`smoke-test: ok`, 32/32 passed (100%), exit 0. This is the intended consumer's
predicate, not a reachability check.

The review is an application candidate, not a claim that dispatch alone proves
the mechanism. The next step drives the real deployed tool and retains its
output.
