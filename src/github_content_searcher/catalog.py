import json
from datetime import datetime, timezone
from pathlib import Path

from github_content_searcher.api import search_github
from github_content_searcher.readme import attach_readmes, fetch_repository_readme
from github_content_searcher.reports import (
    getting_started,
    project_summary_points,
    readme_analysis,
    recommendation_reason,
    render_recommendations_markdown,
    risk_summary,
    suitable_users,
)
from github_content_searcher.site import render_catalog_html


DEFAULT_TOPICS = [
    {"name": "ai-agent", "title": "AI Agent", "query": "python ai agent"},
    {"name": "rag", "title": "RAG", "query": "python rag framework"},
    {"name": "mcp", "title": "MCP", "query": "python mcp server model context protocol"},
    {"name": "crawler", "title": "爬虫", "query": "python crawler web scraping"},
    {"name": "browser-automation", "title": "浏览器自动化", "query": "python browser automation agent"},
]


def build_catalog(
    topics=None,
    search=search_github,
    readme_fetcher=fetch_repository_readme,
    limit=5,
    language="Python",
    min_stars=None,
    pushed_after=None,
):
    selected_topics = topics or DEFAULT_TOPICS
    catalog_topics = []

    for topic in selected_topics:
        result = search(
            query=topic["query"],
            language=topic.get("language", language),
            min_stars=topic.get("min_stars", min_stars),
            pushed_after=topic.get("pushed_after", pushed_after),
            limit=topic.get("limit", limit),
        )
        projects = attach_readmes(
            result.get("candidates", []),
            top=topic.get("limit", limit),
            fetcher=readme_fetcher,
        )

        enriched_projects = [
            enrich_catalog_project(project, topic["title"])
            for project in projects
        ]

        catalog_topics.append(
            {
                "name": topic["name"],
                "title": topic["title"],
                "query": result.get("query", topic["query"]),
                "total_count": result.get("total_count", 0),
                "projects": enriched_projects,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "topics": catalog_topics,
    }


def enrich_catalog_project(project, requirement):
    enriched = dict(project)
    what_it_is, problem_solved, conclusion = project_summary_points(enriched, requirement)

    enriched["recommendation_reason"] = recommendation_reason(enriched, requirement)
    enriched["readme_analysis"] = readme_analysis(enriched, requirement)
    enriched["what_it_is"] = what_it_is
    enriched["problem_solved"] = problem_solved
    enriched["main_conclusion"] = conclusion
    enriched["suitable_for"] = suitable_users(enriched, requirement)
    enriched["getting_started"] = getting_started(enriched)
    enriched["risk_summary"] = risk_summary(enriched)

    return enriched


def render_catalog_markdown(catalog):
    lines = [
        "# GitHub Content Searcher Catalog",
        "",
        f"生成时间：{catalog.get('generated_at', 'Unknown')}",
        "",
    ]

    for topic in catalog.get("topics", []):
        lines.extend(
            [
                f"## {topic['title']}",
                "",
                f"查询：`{topic.get('query', '')}`",
                "",
                render_recommendations_markdown(
                    topic.get("projects", []),
                    requirement=topic["title"],
                    top=len(topic.get("projects", [])) or 5,
                ),
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def write_catalog_outputs(catalog, json_path, markdown_path, html_path):
    json_path = Path(json_path)
    markdown_path = Path(markdown_path)
    html_path = Path(html_path)

    for path in (json_path, markdown_path, html_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_catalog_markdown(catalog), encoding="utf-8")
    html_path.write_text(render_catalog_html(catalog), encoding="utf-8")
