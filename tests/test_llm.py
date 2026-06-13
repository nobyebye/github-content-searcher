from github_content_searcher.llm import build_prompt, rank_with_optional_llm, rule_based_markdown


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
    assert "风险是什么" in markdown


def test_llm_prompt_requires_consistent_chinese_output_structure():
    prompt = build_prompt(sample_candidates(), "找一些关于 GitHub 搜索的 skill", top=1)

    assert "排名 | 项目 | Stars | 最近推送 | 推荐理由" in prompt
    assert "README" in prompt
    assert "主要是什么东西" in prompt
    assert "适合谁" in prompt
    assert "怎么上手" in prompt
    assert "风险是什么" in prompt


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
