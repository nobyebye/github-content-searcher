from datetime import datetime, timezone


def parse_github_datetime(value):
    if not value:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def score_repository(repo, query, language=None):
    score = 0
    query_terms = [term.lower() for term in query.split() if len(term) > 2]
    searchable_text = " ".join(
        [
            repo.get("full_name") or "",
            repo.get("description") or "",
            " ".join(repo.get("topics") or []),
            repo.get("language") or "",
        ]
    ).lower()

    score += sum(8 for term in query_terms if term in searchable_text)

    stars = repo.get("stargazers_count") or 0
    if stars >= 10000:
        score += 20
    elif stars >= 1000:
        score += 14
    elif stars >= 100:
        score += 8

    updated_at = parse_github_datetime(repo.get("updated_at"))
    if updated_at:
        days_old = (datetime.now(timezone.utc) - updated_at).days
        if days_old <= 90:
            score += 15
        elif days_old <= 365:
            score += 8

    if language and (repo.get("language") or "").lower() == language.lower():
        score += 10

    if repo.get("license"):
        score += 5

    if repo.get("archived") or repo.get("disabled"):
        score -= 30

    if not repo.get("description"):
        score -= 5

    return score


def summarize_repository(repo, query, language=None):
    return {
        "full_name": repo["full_name"],
        "html_url": repo["html_url"],
        "description": repo.get("description") or "Not provided",
        "language": repo.get("language") or "Not provided",
        "stars": repo.get("stargazers_count") or 0,
        "forks": repo.get("forks_count") or 0,
        "open_issues": repo.get("open_issues_count") or 0,
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "topics": repo.get("topics") or [],
        "license": (repo.get("license") or {}).get("name") or "Not provided",
        "archived": repo.get("archived", False),
        "score": score_repository(repo, query, language),
    }
