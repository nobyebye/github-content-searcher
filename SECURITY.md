# Security Policy

GitHub Content Searcher treats repository content as untrusted input.

## Supported Versions

The current `main` branch and latest tagged release receive security fixes.

## Reporting a Vulnerability

Please open a private security advisory on GitHub if available, or open an issue without including secrets or exploit details.

## Security Design

- The tool does not execute code from searched repositories.
- Repository README files, issues, discussions, and examples are treated as data, not instructions.
- Local LLM prompts should only include candidate summaries, not secrets or private files.
- `GITHUB_TOKEN` is read from the environment and never written to output files.
- Users should inspect third-party repositories before installing or running them.

## Prompt Injection

Repository content may contain malicious instructions such as "ignore previous instructions" or "print your environment variables". Those instructions must never be followed. They are part of the repository data being evaluated.
