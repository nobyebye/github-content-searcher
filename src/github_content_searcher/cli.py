import argparse
import sys

from github_content_searcher.api import GitHubAPIError, search_github
from github_content_searcher.llm import load_candidates, rank_with_optional_llm
from github_content_searcher.reports import render_candidates_json


def configure_utf8_stdio():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="github-content-searcher",
        description="Find and rank AI engineering projects on GitHub.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search GitHub repositories.")
    search_parser.add_argument("query", help="Search query, for example: python ai agent")
    search_parser.add_argument("--language", help="Preferred programming language")
    search_parser.add_argument("--min-stars", type=int, help="Minimum star count")
    search_parser.add_argument("--pushed-after", help="Minimum pushed date, for example: 2025-01-01")
    search_parser.add_argument("--limit", type=int, default=5, help="Number of candidates")
    search_parser.add_argument("--output", help="Write candidate JSON to this path")

    rank_parser = subparsers.add_parser("rank", help="Rank candidate JSON.")
    rank_parser.add_argument("input", help="Candidate JSON from the search command")
    rank_parser.add_argument("--requirement", required=True, help="User engineering requirement")
    rank_parser.add_argument("--top", type=int, default=5, help="Number of recommendations")
    rank_parser.add_argument("--output", help="Write Markdown recommendations to this path")

    return parser


def run_search(args):
    result = search_github(
        query=args.query,
        language=args.language,
        min_stars=args.min_stars,
        pushed_after=args.pushed_after,
        limit=args.limit,
    )
    text = render_candidates_json(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Wrote candidates to {args.output}")
    else:
        print(text, end="")

    return 0


def run_rank(args):
    candidates = load_candidates(args.input)
    markdown = rank_with_optional_llm(candidates, args.requirement, args.top)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(markdown)
            if not markdown.endswith("\n"):
                file.write("\n")
        print(f"Wrote recommendations to {args.output}")
    else:
        print(markdown)

    return 0


def main(argv=None):
    configure_utf8_stdio()
    args = build_parser().parse_args(argv)

    try:
        if args.command == "search":
            return run_search(args)
        if args.command == "rank":
            return run_rank(args)
    except GitHubAPIError as error:
        print(str(error), file=sys.stderr)
        return 2

    return 1
