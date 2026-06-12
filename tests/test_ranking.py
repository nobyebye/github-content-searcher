from github_content_searcher.ranking import score_repository, summarize_repository


def make_repo(**overrides):
    repo = {
        "full_name": "demo/agent",
        "html_url": "https://github.com/demo/agent",
        "description": "python ai agent framework",
        "language": "Python",
        "stargazers_count": 1200,
        "forks_count": 100,
        "open_issues_count": 8,
        "updated_at": "2026-05-01T00:00:00Z",
        "pushed_at": "2026-05-01T00:00:00Z",
        "topics": ["ai-agent", "llm"],
        "license": {"name": "MIT License"},
        "archived": False,
        "disabled": False,
    }
    repo.update(overrides)
    return repo


def test_score_repository_rewards_relevance_popularity_activity_and_license():
    repo = make_repo()

    score = score_repository(repo, "python ai agent", language="Python")

    assert score >= 50


def test_score_repository_penalizes_archived_projects():
    active = make_repo()
    archived = make_repo(archived=True)

    assert score_repository(active, "python ai agent") > score_repository(archived, "python ai agent")


def test_summarize_repository_produces_stable_candidate_shape():
    summary = summarize_repository(make_repo(), "python ai agent", language="Python")

    assert summary["full_name"] == "demo/agent"
    assert summary["stars"] == 1200
    assert summary["license"] == "MIT License"
    assert isinstance(summary["score"], int)
