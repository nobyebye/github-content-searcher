# Contributing

Thank you for improving GitHub Content Searcher.

This project is intentionally focused: help engineers discover and evaluate GitHub projects for AI engineering work.

## Good Contributions

- Better scoring rules for relevance, activity, license clarity, and risk.
- New tests for edge cases and failure modes.
- Realistic examples for AI Agent, RAG, MCP, browser automation, and Skill discovery.
- Improvements to the bundled Codex Skill.
- Documentation that helps users decide which project to study or adopt.

## Out of Scope

- PR review automation.
- GitHub Actions debugging.
- Branch publishing or pull request creation.
- Generic web search.
- Running untrusted repository code automatically.

## Development Setup

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

## Pull Request Checklist

- Tests pass with `python -m pytest`.
- New behavior has tests.
- README examples still match the CLI.
- Skill changes pass `quick_validate.py skills/github-content-searcher`.
- No secrets, tokens, or private repository data are committed.

## Scoring Changes

When changing scoring, explain the user decision it improves. Good scoring should help answer:

> Should I learn, install, compare, or avoid this repository?

Do not rank by stars alone.
