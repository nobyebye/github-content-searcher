from pathlib import Path


def test_skill_metadata_has_required_trigger_terms():
    skill_text = Path("skills/github-content-searcher/SKILL.md").read_text(encoding="utf-8")

    assert "name: github-content-searcher" in skill_text
    assert "AI engineering" in skill_text
    assert "RAG" in skill_text
    assert "MCP" in skill_text
    assert "browser automation" in skill_text
    assert "ranked overview table" in skill_text
    assert "Analyze the README first" in skill_text
    assert "Do not use this skill for PR review" in skill_text
