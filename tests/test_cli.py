from github_content_searcher.cli import build_parser, run_catalog, run_recommend


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
        "github_content_searcher.cli.attach_readmes",
        lambda candidates, top: candidates,
    )
    monkeypatch.setattr(
        "github_content_searcher.cli.rank_with_optional_llm",
        fake_rank_with_optional_llm,
    )

    assert run_recommend(args) == 0
    assert "# recommendations" in capsys.readouterr().out


def test_run_recommend_enriches_candidates_with_readmes(monkeypatch):
    args = build_parser().parse_args(
        ["recommend", "python crawler", "--requirement", "找爬虫项目", "--top", "3"]
    )

    monkeypatch.setattr(
        "github_content_searcher.cli.search_github",
        lambda **kwargs: {"candidates": [{"full_name": "demo/crawler"}]},
    )

    def fake_attach_readmes(candidates, top):
        assert candidates == [{"full_name": "demo/crawler"}]
        assert top == 3
        return [{"full_name": "demo/crawler", "readme_excerpt": "README summary"}]

    def fake_rank_with_optional_llm(candidates, requirement, top):
        assert candidates[0]["readme_excerpt"] == "README summary"
        return "# recommendations"

    monkeypatch.setattr("github_content_searcher.cli.attach_readmes", fake_attach_readmes)
    monkeypatch.setattr("github_content_searcher.cli.rank_with_optional_llm", fake_rank_with_optional_llm)

    assert run_recommend(args) == 0


def test_cli_accepts_catalog_command():
    args = build_parser().parse_args(
        [
            "catalog",
            "--limit",
            "3",
            "--output-json",
            "data/catalog.json",
            "--output-md",
            "data/catalog.md",
            "--output-html",
            "docs/index.html",
        ]
    )

    assert args.command == "catalog"
    assert args.limit == 3
    assert args.output_json == "data/catalog.json"
    assert args.output_md == "data/catalog.md"
    assert args.output_html == "docs/index.html"


def test_run_catalog_builds_and_writes_outputs(monkeypatch, tmp_path):
    args = build_parser().parse_args(
        [
            "catalog",
            "--limit",
            "2",
            "--output-json",
            str(tmp_path / "catalog.json"),
            "--output-md",
            str(tmp_path / "catalog.md"),
            "--output-html",
            str(tmp_path / "index.html"),
        ]
    )
    catalog = {"topics": []}

    def fake_build_catalog(limit, min_stars, pushed_after):
        assert limit == 2
        assert min_stars is None
        assert pushed_after is None
        return catalog

    def fake_write_catalog_outputs(received_catalog, json_path, markdown_path, html_path):
        assert received_catalog == catalog
        assert str(json_path).endswith("catalog.json")
        assert str(markdown_path).endswith("catalog.md")
        assert str(html_path).endswith("index.html")

    monkeypatch.setattr("github_content_searcher.cli.build_catalog", fake_build_catalog)
    monkeypatch.setattr("github_content_searcher.cli.write_catalog_outputs", fake_write_catalog_outputs)

    assert run_catalog(args) == 0


def test_cli_accepts_doctor_command():
    args = build_parser().parse_args(["doctor"])

    assert args.command == "doctor"
