import json
import urllib.error

import pytest

from github_content_searcher.api import (
    GitHubAPIError,
    build_headers,
    build_query,
    search_github,
)


def test_build_query_adds_github_qualifiers():
    query = build_query(
        "python ai agent",
        language="Python",
        min_stars=100,
        pushed_after="2025-01-01",
    )

    assert query == "python ai agent language:Python stars:>100 pushed:>2025-01-01"


def test_build_headers_uses_token_when_available(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_demo")

    headers = build_headers()

    assert headers["Accept"] == "application/vnd.github+json"
    assert headers["User-Agent"] == "github-content-searcher"
    assert headers["Authorization"] == "Bearer ghp_demo"


def test_search_github_returns_ranked_candidates(monkeypatch):
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self):
            return json.dumps(
                {
                    "total_count": 2,
                    "items": [
                        {
                            "full_name": "small/project",
                            "html_url": "https://github.com/small/project",
                            "description": "small project",
                            "language": "Python",
                            "stargazers_count": 20,
                            "forks_count": 1,
                            "open_issues_count": 0,
                            "updated_at": "2026-01-01T00:00:00Z",
                            "pushed_at": "2026-01-01T00:00:00Z",
                            "topics": [],
                            "license": None,
                            "archived": False,
                            "disabled": False,
                        },
                        {
                            "full_name": "strong/agent",
                            "html_url": "https://github.com/strong/agent",
                            "description": "python ai agent framework",
                            "language": "Python",
                            "stargazers_count": 5000,
                            "forks_count": 300,
                            "open_issues_count": 12,
                            "updated_at": "2026-05-01T00:00:00Z",
                            "pushed_at": "2026-05-01T00:00:00Z",
                            "topics": ["ai-agent"],
                            "license": {"name": "MIT License"},
                            "archived": False,
                            "disabled": False,
                        },
                    ],
                }
            ).encode("utf-8")

    def fake_urlopen(request, timeout):
        return FakeResponse()

    monkeypatch.setattr("github_content_searcher.api.urllib.request.urlopen", fake_urlopen)

    result = search_github("python ai agent", language="Python", limit=2)

    assert result["total_count"] == 2
    assert result["candidates"][0]["full_name"] == "strong/agent"


def test_search_github_turns_rate_limit_into_helpful_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(
            url="https://api.github.com/search/repositories",
            code=403,
            msg="Forbidden",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr("github_content_searcher.api.urllib.request.urlopen", fake_urlopen)

    with pytest.raises(GitHubAPIError, match="GITHUB_TOKEN"):
        search_github("python ai agent")
