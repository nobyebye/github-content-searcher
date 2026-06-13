from pathlib import Path
import tomllib

from github_content_searcher import __version__


def test_package_version_matches_pyproject():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert __version__ == pyproject["project"]["version"]


def test_changelog_contains_current_version():
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")

    assert f"## {__version__}" in changelog
