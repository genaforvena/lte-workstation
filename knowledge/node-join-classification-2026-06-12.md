# node-join.sh classification

Date: 2026-06-12

## Verdict

`node-join.sh` -> `DEAD`

`node-join-android.sh` -> distinct tool, keep canon

## Evidence

1. `node-join.sh` is already removed from the tree.
   - `git log --oneline -- scripts/node-join.sh` shows:
     - `a0439e4 decay node-join.sh — superseded by bootstrap.sh (orphan-guard catch)`

2. The removal commit states the reason explicitly and the diff confirms it.
   - `node-join.sh` only handled Linux-node registration basics:
     - Tailscale presence check
     - Tailscale SSH enablement
     - `tag:lte-node` advertising
     - summary output
   - It did **not** do the broader node adoption work that `bootstrap.sh` does:
     - repo clone
     - tool deploy
     - tmux beachhead
     - restore/culture pull
     - reflex setup

3. Current onboarding doctrine points to `bootstrap.sh`, not `node-join.sh`.
   - `~/.mesh/knowledge/node-onboarding.md` defines the one-command front door as pinned `bootstrap.sh`.
   - `~/.mesh/PLAN.md` already records `node-join.sh DECAYED (a0439e4)` and says docs were re-pointed.

4. `node-join-android.sh` is not the same thing.
   - It is a remote-registration helper for Android/Termux phones.
   - It handles:
     - SSH to Termux on port `8022`
     - key install onto the phone
     - Tailscale tag assignment via API because Termux Android path differs
   - It is still canon-listed in `CLAUDE.md` as the phone onboarding path.
   - That is a distinct substrate-specific tool, not a generic-node onboarding duplicate.

## Conclusion

Do **not** merge `node-join.sh` into `node-join-android.sh`.

The generic Linux onboarding path is already `bootstrap.sh`. `node-join.sh` was a narrower, now-retired subset and should stay dead. `node-join-android.sh` remains the distinct Android helper.
