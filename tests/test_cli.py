from github_content_searcher.cli import build_parser, run_recommend


def test_cli_accepts_search_command():
    args = build_parser().parse_args(
        ["search", "python ai agent", "--language", "Python", "--min-stars", "100"]
    )

    assert args.command == "search"
    assert args.query == "python ai agent"
    assert args.language == "Python"
    assert args.min_stars == 100


def test_cli_rejects_non_positive_limit():
    parser = build_parser()

    try:
        parser.parse_args(["search", "python ai agent", "--limit", "0"])
    except SystemExit as error:
        assert error.code == 2
    else:
        raise AssertionError("Expected parser to reject non-positive limit")


def test_cli_accepts_rank_command():
    args = build_parser().parse_args(
        ["rank", "candidates.json", "--requirement", "学习 AI Agent", "--top", "3"]
    )

    assert args.command == "rank"
    assert args.input == "candidates.json"
    assert args.requirement == "学习 AI Agent"
    assert args.top == 3


def test_cli_accepts_recommend_command():
    args = build_parser().parse_args(
        [
            "recommend",
            "python ai agent",
            "--requirement",
            "学习 AI Agent",
            "--language",
            "Python",
            "--min-stars",
            "100",
            "--limit",
            "5",
            "--top",
            "3",
        ]
    )

    assert args.command == "recommend"
    assert args.query == "python ai agent"
    assert args.requirement == "学习 AI Agent"
    assert args.language == "Python"
    assert args.min_stars == 100
    assert args.limit == 5
    assert args.top == 3


def test_run_recommend_searches_and_ranks(monkeypatch, capsys):
    args = build_parser().parse_args(
        ["recommend", "python ai agent", "--requirement", "学习 AI Agent"]
    )

    def fake_search_github(**kwargs):
        assert kwargs["query"] == "python ai agent"
        return {"candidates": [{"full_name": "demo/agent", "score": 50}]}

    def fake_rank_with_optional_llm(candidates, requirement, top):
        assert candidates == [{"full_name": "demo/agent", "score": 50}]
        assert requirement == "学习 AI Agent"
        assert top == 5
        return "# recommendations"

    monkeypatch.setattr("github_content_searcher.cli.search_github", fake_search_github)
    monkeypatch.setattr(
        "github_content_searcher.cli.rank_with_optional_llm",
        fake_rank_with_optional_llm,
    )

    assert run_recommend(args) == 0
    assert "# recommendations" in capsys.readouterr().out


def test_cli_accepts_doctor_command():
    args = build_parser().parse_args(["doctor"])

    assert args.command == "doctor"
