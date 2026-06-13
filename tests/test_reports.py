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
    assert "适合谁" in markdown
    assert "怎么上手" in markdown


def test_render_recommendations_markdown_starts_with_ranked_overview_table():
    markdown = render_recommendations_markdown(
        [
            {
                "full_name": "demo/agent",
                "html_url": "https://github.com/demo/agent",
                "description": "A Python LLM agent framework with RAG and MCP support.",
                "stars": 1000,
                "language": "Python",
                "updated_at": "2026-05-01T00:00:00Z",
                "score": 60,
                "license": "MIT License",
                "open_issues": 5,
            }
        ],
        requirement="需要 Python LLM 项目，兼顾 MCP 和 RAG",
        top=1,
    )

    assert "| 排名 | 项目 | Stars | 最近推送 | 推荐理由 |" in markdown
    assert "| 1 | [demo/agent](https://github.com/demo/agent) | 1000 | 2026-05-01 |" in markdown
    assert markdown.index("| 排名 | 项目 | Stars | 最近推送 | 推荐理由 |") < markdown.index("## Top 1: demo/agent")


def test_render_recommendations_markdown_has_readme_oriented_chinese_analysis():
    markdown = render_recommendations_markdown(
        [
            {
                "full_name": "demo/crawler",
                "html_url": "https://github.com/demo/crawler",
                "description": "A Python web crawler framework for scraping websites.",
                "stars": 1000,
                "language": "Python",
                "updated_at": "2026-05-01T00:00:00Z",
                "score": 60,
                "license": "MIT License",
                "open_issues": 5,
            }
        ],
        requirement="找一些关于爬虫的项目",
        top=1,
    )

    assert "README 分析" in markdown
    assert "适合谁" in markdown
    assert "怎么上手" in markdown
    assert "风险是什么" in markdown


def test_render_recommendations_markdown_summarizes_each_project_in_user_language():
    markdown = render_recommendations_markdown(
        [
            {
                "full_name": "demo/crawler",
                "html_url": "https://github.com/demo/crawler",
                "description": "A Python web crawler framework for scraping websites.",
                "stars": 1000,
                "language": "Python",
                "updated_at": "2026-05-01T00:00:00Z",
                "score": 60,
                "license": "MIT License",
                "open_issues": 5,
            }
        ],
        requirement="找一些关于爬虫的项目",
        top=1,
    )

    assert "主要是什么东西" in markdown
    assert "解决了什么问题" in markdown
    assert "主要的结论" in markdown
    assert "爬虫" in markdown


def test_chinese_project_summary_translates_common_crawler_terms():
    markdown = render_recommendations_markdown(
        [
            {
                "full_name": "demo/crawler",
                "html_url": "https://github.com/demo/crawler",
                "description": "A web scraping and browser automation library for Python crawlers.",
                "stars": 1000,
                "language": "Python",
                "updated_at": "2026-05-01T00:00:00Z",
                "score": 60,
                "license": "MIT License",
                "open_issues": 5,
            }
        ],
        requirement="找一些关于爬虫的项目",
        top=1,
    )

    assert "网页抓取" in markdown
    assert "浏览器自动化" in markdown


def test_project_summary_prioritizes_user_requirement_domain():
    markdown = render_recommendations_markdown(
        [
            {
                "full_name": "demo/crawler",
                "html_url": "https://github.com/demo/crawler",
                "description": "A web scraping library that also mentions RAG, MCP, and browser automation.",
                "stars": 1000,
                "language": "Python",
                "updated_at": "2026-05-01T00:00:00Z",
                "score": 60,
                "license": "MIT License",
                "open_issues": 5,
            }
        ],
        requirement="找一些关于爬虫的项目",
        top=1,
    )

    assert "面向网页抓取和爬虫的 Python 项目" in markdown
    assert "面向网页抓取和爬虫、" not in markdown
    assert "RAG 和知识检索" not in markdown
    assert "MCP 工具和上下文协议" not in markdown
