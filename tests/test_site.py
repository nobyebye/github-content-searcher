from github_content_searcher.site import render_catalog_html


def test_render_catalog_html_contains_static_catalog_page():
    catalog = {
        "generated_at": "2026-06-13T00:00:00Z",
        "topics": [
            {
                "title": "爬虫",
                "projects": [
                    {
                        "full_name": "demo/crawler",
                        "html_url": "https://github.com/demo/crawler",
                        "stars": 1000,
                        "updated_at": "2026-05-01T00:00:00Z",
                        "recommendation_reason": "Python 项目，匹配网页抓取和爬虫",
                        "readme_excerpt": "README says this is a crawler.",
                        "suitable_for": "适合 Python 学习者。",
                    }
                ],
            }
        ],
    }

    html = render_catalog_html(catalog)

    assert "<!doctype html>" in html.lower()
    assert "GitHub Content Searcher Catalog" in html
    assert "demo/crawler" in html
    assert "README says this is a crawler." in html
