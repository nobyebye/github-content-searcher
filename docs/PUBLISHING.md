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
```

Validate the bundled Skill:

```powershell
quick_validate.py .\skills\github-content-searcher
```
