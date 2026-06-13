import urllib.error

from github_content_searcher.readme import attach_readmes, fetch_repository_readme, readme_excerpt


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


def test_fetch_repository_readme_uses_github_raw_readme_endpoint():
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["accept"] = request.headers["Accept"]
        captured["timeout"] = timeout
        return FakeResponse(b"# Demo\n\nQuick start for a crawler project.")

    text = fetch_repository_readme("demo/crawler", opener=fake_urlopen)

    assert captured["url"] == "https://api.github.com/repos/demo/crawler/readme"
    assert captured["accept"] == "application/vnd.github.raw"
    assert captured["timeout"] == 20
    assert "Quick start" in text


def test_fetch_repository_readme_returns_none_when_missing():
    def fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 404, "not found", None, None)

    assert fetch_repository_readme("demo/missing", opener=fake_urlopen) is None


def test_readme_excerpt_skips_badges_and_keeps_useful_text():
    text = """
# demo

[![Build](https://example.com/badge.svg)](https://example.com)

Demo is a Python crawler framework.

## Install
"""

    assert readme_excerpt(text) == "Demo is a Python crawler framework."


def test_attach_readmes_only_enriches_top_candidates():
    candidates = [
        {"full_name": "demo/one"},
        {"full_name": "demo/two"},
        {"full_name": "demo/three"},
    ]

    enriched = attach_readmes(candidates, top=2, fetcher=lambda name: f"# {name}\n\nREADME for {name}")

    assert enriched[0]["readme_excerpt"] == "README for demo/one"
    assert enriched[1]["readme_excerpt"] == "README for demo/two"
    assert "readme_excerpt" not in enriched[2]
