# Versioning

GitHub Content Searcher uses semantic versioning:

```text
MAJOR.MINOR.PATCH
```

## Current Release

```text
0.2.1
```

## Version Sources

Keep these files in sync:

- `pyproject.toml`
- `src/github_content_searcher/__init__.py`
- `CHANGELOG.md`
- Git tag, for example `v0.2.1`

The test suite checks that the package version matches `pyproject.toml` and appears in `CHANGELOG.md`.

## Release Checklist

Before tagging a release:

```powershell
python -m pytest
python -m github_content_searcher doctor
python -m github_content_searcher --version
quick_validate.py .\skills\github-content-searcher
```

Create the release tag:

```powershell
git tag -a v0.2.1 -m "Release v0.2.1"
```

Push code and tags:

```powershell
git push -u origin main
git push origin v0.2.1
```
