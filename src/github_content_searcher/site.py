from html import escape

from github_content_searcher.reports import short_date


def render_catalog_html(catalog):
    topic_sections = []

    for topic in catalog.get("topics", []):
        cards = []

        for project in topic.get("projects", []):
            cards.append(
                """
        <article class="project-card">
          <h3><a href="{url}">{name}</a></h3>
          <p class="meta">Stars {stars} · Updated {updated}</p>
          <p><strong>推荐理由：</strong>{reason}</p>
          <p><strong>README 分析：</strong>{readme}</p>
          <p><strong>适合谁：</strong>{suitable_for}</p>
        </article>
                """.format(
                    url=escape(project.get("html_url", "")),
                    name=escape(project.get("full_name", "Unknown")),
                    stars=escape(str(project.get("stars", 0))),
                    updated=escape(short_date(project.get("updated_at"))),
                    reason=escape(project.get("recommendation_reason", "")),
                    readme=escape(project.get("readme_excerpt") or project.get("readme_analysis", "")),
                    suitable_for=escape(project.get("suitable_for", "")),
                )
            )

        topic_sections.append(
            """
      <section>
        <h2>{title}</h2>
        {cards}
      </section>
            """.format(
                title=escape(topic.get("title", topic.get("name", "Untitled"))),
                cards="\n".join(cards),
            )
        )

    return """<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GitHub Content Searcher Catalog</title>
    <style>
      body {{ font-family: system-ui, sans-serif; margin: 0; color: #17202a; background: #f7f8fa; }}
      main {{ max-width: 960px; margin: 0 auto; padding: 32px 20px; }}
      h1 {{ margin-bottom: 4px; }}
      section {{ margin-top: 32px; }}
      .project-card {{ background: white; border: 1px solid #d9dee7; border-radius: 8px; padding: 16px; margin: 12px 0; }}
      .meta {{ color: #5b6675; }}
      a {{ color: #1f5fbf; }}
    </style>
  </head>
  <body>
    <main>
      <h1>GitHub Content Searcher Catalog</h1>
      <p>Generated at {generated_at}</p>
      {topics}
    </main>
  </body>
</html>
""".format(
        generated_at=escape(catalog.get("generated_at", "Unknown")),
        topics="\n".join(topic_sections),
    )
