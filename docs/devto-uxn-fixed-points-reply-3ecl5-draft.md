# Reply draft for comment `3ecl5`

That distinction helps, and I don't think the two labels name the same
failure. `UNMEASURED` is about the observer: the check did not establish
whether the pattern was present. `SATURATED` is about the source: the counter
reached its maximum, so it can no longer witness future events. Both make
"no new value" inconclusive, but for different reasons. One is missing
observation; the other is a measured producer boundary. I'd keep them as
separate outcomes rather than collapsing both into a generic failure verdict.
