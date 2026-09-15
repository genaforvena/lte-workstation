# Test-isolation repair verification — 2026-09-08

- Task: `recreated-rejected-20260908-05-corrected/test-isolation-repair`
- Current checkout: `ccc73714108fe68270f51a06d9155a923e546e98`
- Source: `scripts/mesh-promises`
- Canary: `tests/test-mesh-promises-isolation.py`
- Source SHA-256: `2df906059f3920340381702a1dcb4a99cf2842645241a510fc73c09c322f26f3`
- Canary SHA-256: `3c99fcaf59fc31dbdfcf7cc5b4e40d3f8af3f1a907d92c3f65fb1ecb30ef56ae`

## Verification

```text
python3 tests/test-mesh-promises-isolation.py
PASS: custom mesh feed leaves default HOME summary untouched

bash -n scripts/mesh-promises
PASS (exit 0)
```

The canary uses temporary `HOME/.mesh` and `MESH_DIR` trees, redirects the chat log,
promises directory, voice input, and TG marker into that fixture, and asserts that the
default summary remains unchanged while the custom summary and journal are created. No
historical live-tape variant was read or replayed.
