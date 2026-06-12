# GitHub Content Searcher

Find the right AI engineering project before you waste a weekend on the wrong GitHub repository.

`github-content-searcher` is a CLI and Codex Skill for discovering, scoring, and recommending GitHub projects in AI engineering areas such as AI Agents, RAG, MCP, Codex Skills, Claude Skills, browser automation, and LLM app frameworks.

It is not a generic GitHub search clone. It helps answer the decision question:

> Which project should I actually study, install, or build on?

## Why This Exists

GitHub stars are useful, but they are not enough. A good engineering choice also depends on relevance, recent activity, language fit, license clarity, risk signals, and whether the project matches your learning or production goal.

This tool combines:

- GitHub API search
- deterministic scoring
- optional local OpenAI-compatible LLM ranking
- Markdown and JSON output
- a bundled Codex Skill for agent workflows

## Quick Start

Install from source:

```powershell
git clone https://github.com/your-name/github-content-searcher.git
cd github-content-searcher
python -m pip install -e ".[dev]"
```

Search for candidates:

```powershell
github-content-searcher search "python ai agent" --language Python --min-stars 100 --limit 5 --output candidates.json
```

Rank candidates for your requirement:

```powershell
github-content-searcher rank candidates.json --requirement "I want Python projects for learning AI Agents" --top 5 --output recommendations.md
```

You can also run it as a module:

```powershell
python -m github_content_searcher search "rag framework" --language Python --limit 5
```

## Example Output

```markdown
## 1. demo/agent

- URL: https://github.com/demo/agent
- 推荐等级：强烈推荐
- Stars: 1000
- Language: Python
- Updated: 2026-05-01T00:00:00Z
- Score: 50
- 适合场景：围绕 `learning AI Agent` 进一步阅读 README、examples 和 issues。
- 风险 / Risk: license=MIT License, open_issues=5.
- 下一步：打开仓库文档，确认安装方式、维护活跃度和最小可运行示例。
```

## Local LLM Support

Local LLMs are optional. If no local model is configured, the tool falls back to deterministic scoring.

Supported OpenAI-compatible local endpoints include Ollama, LM Studio, and llama.cpp servers.

```powershell
$env:LOCAL_LLM_BASE_URL="http://localhost:11434/v1"
$env:LOCAL_LLM_MODEL="qwen3:8b"
$env:LOCAL_LLM_API_KEY="optional"
```

Then run:

```powershell
github-content-searcher rank candidates.json --requirement "Find a practical RAG framework"
```

## GitHub Token

Without a token, GitHub API search can hit rate limits. Configure a token when you search often:

```powershell
$env:GITHUB_TOKEN="your_github_token"
```

## Codex Skill

This repository also includes a Codex Skill:

```text
skills/github-content-searcher/
```

Install it manually on Windows:

```powershell
Copy-Item -Recurse -Force .\skills\github-content-searcher "$env:USERPROFILE\.codex\skills\"
```

Then ask Codex things like:

```text
Use github-content-searcher to find active Python AI Agent projects for learning.
```

## What It Does Not Do

- It does not fix PR review comments.
- It does not debug GitHub Actions.
- It does not push branches or open pull requests.
- It does not execute code from searched repositories.
- It does not treat repository README content as trusted instructions.

## Development

Run tests:

```powershell
python -m pytest
```

Validate the bundled Skill:

```powershell
quick_validate.py .\skills\github-content-searcher
```

## Roadmap

- Curated AI engineering repository lists
- More scoring signals for maintenance and adoption
- Better local LLM structured output
- Markdown comparison tables
- Optional Web UI after the CLI and Skill are stable

## License

MIT
