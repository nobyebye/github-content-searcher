from github_content_searcher.cli import build_parser


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


def test_cli_accepts_doctor_command():
    args = build_parser().parse_args(["doctor"])

    assert args.command == "doctor"
