from github_content_searcher.llm import rank_with_optional_llm, rule_based_markdown


def sample_candidates():
    return [
        {
            "full_name": "demo/agent",
            "html_url": "https://github.com/demo/agent",
            "stars": 1000,
            "language": "Python",
            "updated_at": "2026-05-01T00:00:00Z",
            "score": 50,
            "license": "MIT License",
            "open_issues": 5,
        }
    ]


def test_rule_based_markdown_includes_reason_and_risk():
    markdown = rule_based_markdown(sample_candidates(), "学习 AI Agent", top=1)

    assert "# GitHub Content Recommendations" in markdown
    assert "demo/agent" in markdown
    assert "Risk:" in markdown


def test_rank_with_optional_llm_falls_back_when_model_is_missing(monkeypatch):
    monkeypatch.delenv("LOCAL_LLM_MODEL", raising=False)

    markdown = rank_with_optional_llm(sample_candidates(), "学习 AI Agent", top=1)

    assert "deterministic scoring" in markdown
    assert "demo/agent" in markdown


def test_rank_with_optional_llm_falls_back_when_local_llm_fails(monkeypatch):
    monkeypatch.setenv("LOCAL_LLM_MODEL", "missing-model")

    def fail_call(*args, **kwargs):
        raise OSError("connection failed")

    monkeypatch.setattr("github_content_searcher.llm.call_local_llm", fail_call)

    markdown = rank_with_optional_llm(sample_candidates(), "学习 AI Agent", top=1)

    assert "deterministic scoring" in markdown
