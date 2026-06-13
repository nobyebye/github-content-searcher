# Demo

## Search

Use the one-command workflow when you want a recommendation immediately:

```powershell
github-content-searcher recommend "python ai agent" --requirement "I want Python projects for learning AI Agents" --language Python --min-stars 100 --limit 3
```

## Search Then Rank

```powershell
github-content-searcher search "python ai agent" --language Python --min-stars 100 --limit 3 --output candidates.json
```

This writes GitHub repository candidates to `candidates.json`.

```powershell
github-content-searcher rank candidates.json --requirement "I want Python projects for learning AI Agents" --top 3 --output recommendations.md
```

If a local LLM is configured, it can explain the ranking. If not, deterministic scoring is used.

Each recommendation includes:

```text
主要是什么东西
解决了什么问题
主要的结论
```

## Diagnose

```powershell
github-content-searcher doctor
```

This prints the installed version, Python version, GitHub token status, and local LLM configuration.

## Install the Codex Skill

```powershell
Copy-Item -Recurse -Force .\skills\github-content-searcher "$env:USERPROFILE\.codex\skills\"
```

Then ask Codex:

```text
Use github-content-searcher to find active Python AI Agent projects for learning.
```
