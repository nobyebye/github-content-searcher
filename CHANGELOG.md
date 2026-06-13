# Changelog

## 0.2.1 - 2026-06-13

- Standardize recommendation output as overview table first, then Top 5 detailed analysis.
- Add README-oriented Chinese project analysis fields: `README 分析`, `适合谁`, `怎么上手`, and `风险是什么`.
- Update local LLM prompt and bundled Skills to keep response formatting consistent.

## 0.2.0 - 2026-06-13

- Add Claude Code plugin compatibility under `claude-code/github-content-searcher`.
- Add Claude Code install and validation documentation.
- Keep the Codex Skill package while adding a namespaced Claude Code skill command.

## 0.1.1 - 2026-06-13

- Add user-language project summaries to recommendation output.
- Add three required summary fields for each repository: `主要是什么东西`, `解决了什么问题`, and `主要的结论`.
- Improve crawler-related summaries by focusing on web scraping and adjacent capabilities.

## 0.1.0 - 2026-06-12

- Add GitHub repository search for AI engineering projects.
- Add deterministic scoring by relevance, stars, activity, language, license, and risk.
- Add optional local OpenAI-compatible LLM ranking.
- Add Markdown and JSON output.
- Add bundled Codex Skill.
- Add tests, examples, GitHub Actions, and project documentation.
