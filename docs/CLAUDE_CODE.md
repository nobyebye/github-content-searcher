# Claude Code Integration

This project supports Claude Code in two ways:

1. A shareable Claude Code plugin.
2. A standalone personal skill copy.

Claude Code skills use `SKILL.md` files. For public distribution, plugins add a manifest, versioning, and namespaced skill commands.

## Plugin Layout

```text
claude-code/github-content-searcher/
  .claude-plugin/plugin.json
  skills/search/SKILL.md
```

The plugin skill is invoked as:

```text
/github-content-searcher:search 找一些关于爬虫的项目
```

## Test The Plugin Locally

From the repository root:

```powershell
claude --plugin-dir .\claude-code\github-content-searcher
```

Then invoke:

```text
/github-content-searcher:search 找一些关于爬虫的项目
```

Claude Code should use the CLI to search, rank, and summarize GitHub repositories in the user's language.

## Validate The Plugin

If your Claude Code version includes plugin validation, run:

```powershell
claude plugin validate .\claude-code\github-content-searcher
```

## Standalone Personal Skill Install

For a personal skill, copy the skill folder into `~/.claude/skills`.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\github-content-searcher"
Copy-Item -Force .\claude-code\github-content-searcher\skills\search\SKILL.md "$env:USERPROFILE\.claude\skills\github-content-searcher\SKILL.md"
```

macOS, Linux, or WSL:

```bash
mkdir -p ~/.claude/skills/github-content-searcher
cp ./claude-code/github-content-searcher/skills/search/SKILL.md ~/.claude/skills/github-content-searcher/SKILL.md
```

After installation, open Claude Code and try:

```text
/github-content-searcher 找一些关于爬虫的项目
```

## Expected Behavior

Claude Code should:

- search GitHub candidates with the local CLI,
- rank by relevance, stars, activity, language, license, and risk,
- summarize each project in the user's language,
- include `what it is`, `what problem it solves`, and `main conclusion`,
- avoid executing untrusted repository code.

## Troubleshooting

- If the skill is not listed, restart Claude Code or run `/reload-plugins`.
- If GitHub returns 403, configure `GITHUB_TOKEN`.
- If no local LLM is running, the CLI should still work with rule-based scoring.
- If the CLI command is missing, install the package with `python -m pip install -e .`.
