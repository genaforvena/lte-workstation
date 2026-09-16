# Unblock receipt: Hugging Face credential for public release

Date: 2026-09-16
Owner: adint
Task: unblock/adint/d54ae4cc63330486/resolve
Parent blocker: unblock/wake/9f133171cd8fe894/resolve

## Diagnosis

The parent wake is blocked on a write-capable Hugging Face authentication for owner
`genaforvena`. This resolver cannot create or receive that credential. No token file was
present at `/home/mesh-home/.cache/huggingface/token`, and the isolated CLI check returned
`Error: Not logged in` with exit code 1:

```text
/home/mesh-home/.venv-ai/bin/hf auth whoami
hf_auth_whoami_rc=1
```

`/usr/bin/google-chrome` is present, but browser availability does not itself establish an
authenticated HF session or provide a write-scoped token.

## Exact operator action packet

1. In the authorized HF account context, run:

   ```bash
   /home/mesh-home/.venv-ai/bin/hf auth login
   ```

2. Supply a write-scoped User Access Token through the CLI prompt; do not place the token in
   chat, a receipt, or the repository.
3. Verify authentication:

   ```bash
   /home/mesh-home/.venv-ai/bin/hf auth whoami
   ```

4. Retry the blocked release command and capture its four successful public URLs plus the local
   fold refusal:

   ```bash
   /home/mesh-home/.venv-ai/bin/python wake/push_release.py --owner genaforvena
   ```

## Retry edge

After `hf auth whoami` exits 0, rerun the release command above and resume
`wake-public-release-20260916/publish-public-release-20260916`. Until then the wake remains
blocked on the concrete external credential, not on approval or an unattempted mesh-internal
step.
