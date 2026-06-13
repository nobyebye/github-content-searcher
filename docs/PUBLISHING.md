# Publishing

This project is ready to publish as a public GitHub repository.

## Option A: Create the Repository in GitHub Web UI

1. Open GitHub and create a new public repository:

   ```text
   nobyebye/github-content-searcher
   ```

2. Do not add a README, license, or `.gitignore` in the web UI. This repository already has them.

3. Add the remote and push:

   ```powershell
   git remote add origin https://github.com/nobyebye/github-content-searcher.git
   git push -u origin main
   ```

## Option B: Use GitHub CLI

Install GitHub CLI, then authenticate:

```powershell
gh auth login
```

Create and push the public repository:

```powershell
gh repo create nobyebye/github-content-searcher --public --source . --remote origin --push
```

## Pre-publish Checklist

Run these before publishing:

```powershell
python -m pytest
python -m github_content_searcher doctor
python -m github_content_searcher --version
python -m github_content_searcher rank examples\candidates.json --requirement "learning AI Agent"
python -m github_content_searcher catalog --limit 1 --output-json data\catalog.json --output-md data\catalog.md --output-html docs\index.html
```

Validate the bundled Skill:

```powershell
quick_validate.py .\skills\github-content-searcher
```

Validate the Claude Code plugin if your Claude Code version supports it:

```powershell
claude plugin validate .\claude-code\github-content-searcher
```

Tag the release after the checklist passes:

```powershell
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```
