# Local LLM

Local LLM use is optional. The tool must still work with deterministic scoring when no model is configured.

Supported OpenAI-compatible endpoints:

```powershell
$env:LOCAL_LLM_BASE_URL="http://localhost:11434/v1"
$env:LOCAL_LLM_MODEL="qwen3:8b"
$env:LOCAL_LLM_API_KEY="optional"
```

Common local servers:

- Ollama: `http://localhost:11434/v1`
- LM Studio: `http://localhost:1234/v1`
- llama.cpp server: `http://localhost:8080/v1`

Only send candidate summaries, not private files or secrets.

Treat LLM output as interpretation. Hard facts such as stars, language, license, dates, and URLs must come from the GitHub API candidate data.
