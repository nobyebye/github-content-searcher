import re
import urllib.error
import urllib.request

from github_content_searcher.api import build_headers


def fetch_repository_readme(full_name, opener=urllib.request.urlopen):
    url = f"https://api.github.com/repos/{full_name}/readme"
    headers = build_headers()
    headers["Accept"] = "application/vnd.github.raw"
    request = urllib.request.Request(url, headers=headers)

    try:
        with opener(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        if error.code == 403:
            return None
        raise
    except urllib.error.URLError:
        return None


def readme_excerpt(text, max_length=280):
    if not text:
        return ""

    lines = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue
        if line.startswith("#"):
            continue
        if re.match(r"^\[!\[.*\]\(.*\)\]\(.*\)$", line):
            continue
        if line.startswith("```"):
            continue

        lines.append(line)

        if len(" ".join(lines)) >= max_length:
            break

    excerpt = " ".join(lines)
    if len(excerpt) <= max_length:
        return excerpt

    return excerpt[: max_length - 1].rstrip() + "…"


def attach_readmes(candidates, top=5, fetcher=fetch_repository_readme):
    enriched = [dict(candidate) for candidate in candidates]

    for candidate in enriched[:top]:
        readme = fetcher(candidate["full_name"])
        excerpt = readme_excerpt(readme)

        if excerpt:
            candidate["readme_excerpt"] = excerpt

    return enriched
