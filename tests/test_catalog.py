import json

from github_content_searcher.catalog import (
    build_catalog,
    render_catalog_markdown,
    write_catalog_outputs,
)


def fake_search_github(query, language=None, min_stars=None, pushed_after=None, limit=5):
    return {
        "query": query,
        "total_count": 1,
        "candidates": [
            {
                "full_name": "demo/crawler",
                "html_url": "https://github.com/demo/crawler",
                "description": "A Python crawler framework.",
                "stars": 1000,
                "language": language or "Python",
                "updated_at": "2026-05-01T00:00:00Z",
                "score": 60,
                "license": "MIT License",
                "open_issues": 5,
            }
        ],
    }


def test_build_catalog_collects_topics_and_readme_excerpts():
    catalog = build_catalog(
        topics=[{"name": "crawler", "title": "爬虫", "query": "python crawler"}],
        search=fake_search_github,
        readme_fetcher=lambda full_name: "# Demo\n\nREADME says this is a crawler.",
        limit=1,
    )

    topic = catalog["topics"][0]

    assert topic["name"] == "crawler"
    assert topic["title"] == "爬虫"
    assert topic["projects"][0]["readme_excerpt"] == "README says this is a crawler."


def test_render_catalog_markdown_contains_project_cards():
    catalog = build_catalog(
        topics=[{"name": "crawler", "title": "爬虫", "query": "python crawler"}],
        search=fake_search_github,
        readme_fetcher=lambda full_name: "# Demo\n\nREADME says this is a crawler.",
        limit=1,
    )

    markdown = render_catalog_markdown(catalog)

    assert "# GitHub Content Searcher Catalog" in markdown
    assert "## 爬虫" in markdown
    assert "| 排名 | 项目 | Stars | 最近推送 | 推荐理由 |" in markdown
    assert "README 分析" in markdown
    assert "适合谁" in markdown


def test_write_catalog_outputs_writes_json_markdown_and_html(tmp_path):
    catalog = build_catalog(
        topics=[{"name": "crawler", "title": "爬虫", "query": "python crawler"}],
        search=fake_search_github,
        readme_fetcher=lambda full_name: "# Demo\n\nREADME says this is a crawler.",
        limit=1,
    )

    json_path = tmp_path / "catalog.json"
    markdown_path = tmp_path / "catalog.md"
    html_path = tmp_path / "index.html"

    write_catalog_outputs(catalog, json_path, markdown_path, html_path)

    assert json.loads(json_path.read_text(encoding="utf-8"))["topics"][0]["name"] == "crawler"
    assert "README 分析" in markdown_path.read_text(encoding="utf-8")
    assert "<!doctype html>" in html_path.read_text(encoding="utf-8").lower()
