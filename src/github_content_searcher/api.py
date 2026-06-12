import json
import os
import urllib.error
import urllib.parse
import urllib.request

from github_content_searcher.ranking import summarize_repository


GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


class GitHubAPIError(RuntimeError):
    """Raised when GitHub API access fails in a user-actionable way."""


def build_query(query, language=None, min_stars=None, pushed_after=None):
    parts = [query.strip()]

    if language:
        parts.append(f"language:{language}")

    if min_stars:
        parts.append(f"stars:>{min_stars}")

    if pushed_after:
        parts.append(f"pushed:>{pushed_after}")

    return " ".join(part for part in parts if part)


def build_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-content-searcher",
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def search_github(query, language=None, min_stars=None, pushed_after=None, limit=5):
    github_query = build_query(query, language, min_stars, pushed_after)
    params = {
        "q": github_query,
        "sort": "stars",
        "order": "desc",
        "per_page": str(limit),
    }
    url = f"{GITHUB_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers=build_headers())

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = ""
        if error.fp:
            body = error.read().decode("utf-8", errors="replace")
        if error.code == 403:
            raise GitHubAPIError(
                "GitHub search was rate-limited or forbidden. Configure GITHUB_TOKEN and try again."
            ) from error
        raise GitHubAPIError(f"GitHub API error {error.code}: {body}") from error
    except urllib.error.URLError as error:
        raise GitHubAPIError(f"Could not reach GitHub API: {error}") from error

    candidates = [
        summarize_repository(repo, query, language)
        for repo in data.get("items", [])
    ]
    candidates.sort(key=lambda item: item["score"], reverse=True)

    return {
        "query": github_query,
        "total_count": data.get("total_count", 0),
        "candidates": candidates,
    }
