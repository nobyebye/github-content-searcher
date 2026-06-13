# GitHub Content Searcher

[![Tests](https://github.com/nobyebye/github-content-searcher/actions/workflows/test.yml/badge.svg)](https://github.com/nobyebye/github-content-searcher/actions/workflows/test.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Find the right AI engineering project before you waste a weekend on the wrong GitHub repository.

`github-content-searcher` is a CLI, Codex Skill, and Claude Code plugin for discovering, scoring, and recommending GitHub projects in AI engineering areas such as AI Agents, RAG, MCP, Codex Skills, Claude Skills, browser automation, and LLM app frameworks.

It is not a generic GitHub search clone. It helps answer the decision question:

> Which project should I actually study, install, or build on?

Each recommended project includes a short user-language summary:

- 主要是什么东西
- 解决了什么问题
- 主要的结论

## Why This Exists

GitHub stars are useful, but they are not enough. A good engineering choice also depends on relevance, recent activity, language fit, license clarity, risk signals, and whether the project matches your learning or production goal.

This tool combines:

- GitHub API search
- README fetching for top recommendations
- deterministic scoring
- optional local OpenAI-compatible LLM ranking
- Markdown and JSON output
- reusable JSON / Markdown / HTML catalogs
- bundled Codex Skill and Claude Code plugin packages for agent workflows

## Quick Start

Install from source:

```powershell
git clone https://github.com/nobyebye/github-content-searcher.git
cd github-content-searcher
python -m pip install -e ".[dev]"
```

Check your local setup:

```powershell
github-content-searcher doctor
github-content-searcher --version
```

Search and rank in one command:

```powershell
github-content-searcher recommend "python ai agent" --requirement "I want Python projects for learning AI Agents" --language Python --min-stars 100 --limit 5
```

Search for candidates:

```powershell
github-content-searcher search "python ai agent" --language Python --min-stars 100 --limit 5 --output candidates.json
```

Rank candidates for your requirement:

```powershell
github-content-searcher rank candidates.json --requirement "I want Python projects for learning AI Agents" --top 5 --output recommendations.md
```

Build a reusable catalog and static page:

```powershell
github-content-searcher catalog --limit 5 --output-json data\catalog.json --output-md data\catalog.md --output-html docs\index.html
```

You can also run it as a module:

```powershell
python -m github_content_searcher search "rag framework" --language Python --limit 5
```

If you are in a restricted or offline environment, install `setuptools` in your virtual environment first or run the project with `PYTHONPATH=src` for local development:

```powershell
$env:PYTHONPATH="src"
python -m github_content_searcher rank examples\candidates.json --requirement "learning AI Agent"
```

## Example Output

```markdown
# GitHub Content Recommendations

需求：找一些关于爬虫的项目

## Top 项目总览

| 排名 | 项目 | Stars | 最近推送 | 推荐理由 |
|---:|---|---:|---|---|
| 1 | [demo/agent](https://github.com/demo/agent) | 1000 | 2026-05-01 | Python 项目，匹配网页抓取和爬虫，评分 50，Stars 1000 |

## Top 5 深度分析

## Top 1: demo/agent

- URL: https://github.com/demo/agent
- 推荐等级：强烈推荐
- Stars: 1000
- Language: Python
- Updated: 2026-05-01T00:00:00Z
- Score: 50
- README 分析：README 应优先确认它是否提供安装、示例和核心能力说明。从仓库描述看，它当前更像是网页抓取和爬虫方向的项目。
- 主要是什么东西：这是一个面向网页抓取和爬虫的 Python 项目。
- 解决了什么问题：它主要解决网页抓取和爬虫场景下的学习参考、方案选型和二次开发起点问题。
- 主要的结论：综合评分 50，Stars 1000，许可证 MIT License；建议继续查看 README、examples 和 issues。
- 适合谁：适合想用 Python 学习、对比或二次开发网页抓取和爬虫项目的人。
- 怎么上手：先看 README 的安装命令和 Quick Start，再找 examples、docs 或 demo。
- 风险是什么：许可证 MIT License；开放 issue 5；还要检查 README 是否过时、示例是否能跑通。
```

## Recommended Workflow

Use `recommend` when you want a quick decision:

```powershell
github-content-searcher recommend "browser automation agent" --requirement "I need an active Python project for browser automation agents" --language Python --min-stars 100
```

Use `search` and `rank` separately when you want to save candidate JSON and inspect it later.

Use `catalog` when you want to build a reusable project directory for AI Agent, RAG, MCP, crawler, and browser automation topics.

## Catalog And Static Page

The catalog command creates three outputs:

```text
data/catalog.json
data/catalog.md
docs/index.html
```

The default catalog topics are:

- AI Agent
- RAG
- MCP
- 爬虫
- 浏览器自动化

The generated project cards include README analysis when the README is available. If a README cannot be fetched, the card falls back to repository description and metadata.

The repository also includes a daily GitHub Actions workflow:

```text
.github/workflows/update-catalog.yml
```

It builds the catalog and uploads it as a workflow artifact.

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

## Claude Code Plugin

This repository also includes a Claude Code plugin:

```text
claude-code/github-content-searcher/
```

Test it locally from the repository root:

```powershell
claude --plugin-dir .\claude-code\github-content-searcher
```

Then invoke the namespaced skill:

```text
/github-content-searcher:search 找一些关于爬虫的项目
```

Standalone install and validation notes are in [docs/CLAUDE_CODE.md](docs/CLAUDE_CODE.md).

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

Run the CLI locally:

```powershell
github-content-searcher doctor
github-content-searcher rank examples\candidates.json --requirement "I want Python projects for learning AI Agents"
github-content-searcher catalog --limit 2
```

Validate the bundled Skill:

```powershell
quick_validate.py .\skills\github-content-searcher
```

Publishing notes are in [docs/PUBLISHING.md](docs/PUBLISHING.md).
Versioning notes are in [docs/VERSIONING.md](docs/VERSIONING.md).

## Roadmap

- Curated AI engineering repository lists
- More scoring signals for maintenance and adoption
- Better local LLM structured output
- Markdown comparison tables
- Optional richer Web UI after the generated static catalog is stable

See [CHANGELOG.md](CHANGELOG.md) for release history.

## For Chinese Learners

这个项目也适合用来学习标准 Python 工程结构：

- `src/` package 布局
- CLI 参数设计
- GitHub API 请求
- JSON / Markdown 输出
- 本地 LLM 降级策略
- pytest 单元测试
- GitHub Actions CI
- Codex Skill 打包方式
- Claude Code Plugin 打包方式

## License

MIT
