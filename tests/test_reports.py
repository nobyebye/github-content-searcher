import json

from github_content_searcher.reports import render_candidates_json, render_recommendations_markdown


def test_render_candidates_json_is_utf8_friendly():
    text = render_candidates_json({"query": "python ai agent", "candidates": [{"description": "中文"}]})

    assert json.loads(text)["candidates"][0]["description"] == "中文"


def test_render_recommendations_markdown_has_project_decision_fields():
    markdown = render_recommendations_markdown(
        [
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
        ],
        requirement="学习 AI Agent",
        top=1,
    )

    assert "推荐等级" in markdown
    assert "适合场景" in markdown
    assert "下一步" in markdown
