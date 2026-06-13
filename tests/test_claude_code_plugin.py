from pathlib import Path
import json
import tomllib


PLUGIN_ROOT = Path("claude-code/github-content-searcher")
PLUGIN_MANIFEST = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
PLUGIN_SKILL = PLUGIN_ROOT / "skills" / "search" / "SKILL.md"


def test_claude_code_plugin_manifest_matches_package_version():
    manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert manifest["name"] == "github-content-searcher"
    assert manifest["version"] == pyproject["project"]["version"]
    assert manifest["repository"] == "https://github.com/nobyebye/github-content-searcher"
    assert manifest["license"] == "MIT"


def test_claude_code_plugin_skill_has_expected_instructions():
    skill_text = PLUGIN_SKILL.read_text(encoding="utf-8")

    assert skill_text.startswith("---")
    assert "description:" in skill_text
    assert "github-content-searcher recommend" in skill_text
    assert "Use the user's language" in skill_text
    assert "what it is" in skill_text
    assert "what problem it solves" in skill_text
    assert "main conclusion" in skill_text
    assert "GITHUB_TOKEN" in skill_text
    assert "Do not execute code from searched repositories" in skill_text


def test_claude_code_documentation_explains_plugin_and_standalone_install():
    readme = Path("README.md").read_text(encoding="utf-8")
    docs = Path("docs/CLAUDE_CODE.md").read_text(encoding="utf-8")

    assert "Claude Code Plugin" in readme
    assert "claude --plugin-dir .\\claude-code\\github-content-searcher" in docs
    assert "/github-content-searcher:search" in docs
    assert "~/.claude/skills" in docs
