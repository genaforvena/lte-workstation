# Witness chat review — swap-drain concurrency race

Observed 2026-09-09: the board tail contains four `swap-drain` actuator lines between
06:24:57Z and 06:25:21Z on `mesh-home`, including repeated `swapoff -a && swapon -a`.

Current source check:

- `scripts/mesh-swap-drain:278-304` evaluates the DRAIN/treadmill gate and may return before
  the lock is considered.
- `scripts/mesh-swap-drain:315-317` acquires the non-blocking flock only afterward.

Therefore concurrent `--drain`/`--sweep` processes can all observe the same pre-drain state,
pass the treadmill gate, then serialize through the lock and each actuate. The lock prevents
interleaving but does not make the gate-and-actuation decision atomic. Fix by acquiring the
lock before the final live verdict/treadmill decision (or re-checking the verdict and treadmill
state after the lock), then verify with a concurrent fixture that one invocation actuates and
the others skip, while a real pressure emergency remains permitted.

Verification: `mesh-task audit` had no existing open task for this exact race; the source lines
above were inspected directly. Existing swap-drain dedup work at `chat-review/swap-drain-
dedup-key-drifts-with-memtotal` is a different structural-warning marker issue.
