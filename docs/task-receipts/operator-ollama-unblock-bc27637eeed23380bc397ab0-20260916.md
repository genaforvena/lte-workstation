# Ollama unblock — `tg-bc27637eeed23380bc397ab0`

- Before: `ollama ps` showed `qwen3-vl:4b-instruct` (`ee4b975b58c1`), 4.2 GB, 100% GPU.
- Action: `ollama stop qwen3-vl:4b-instruct`.
- After: `ollama ps` returned an empty model table.
- Result: the shared Ollama provider is currently free for the blocked exclusive-consumer retry.
- No model was deleted; only the resident runtime was stopped.
