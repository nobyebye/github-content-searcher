import argparse
import os
import platform
import sys

from github_content_searcher import __version__
from github_content_searcher.api import GitHubAPIError, search_github
from github_content_searcher.llm import load_candidates, rank_with_optional_llm
from github_content_searcher.reports import render_candidates_json


def configure_utf8_stdio():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be greater than or equal to 1")
    return number


def build_parser():
    parser = argparse.ArgumentParser(
        prog="github-content-searcher",
        description="Find and rank AI engineering projects on GitHub.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"github-content-searcher {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search GitHub repositories.")
    search_parser.add_argument("query", help="Search query, for example: python ai agent")
    search_parser.add_argument("--language", help="Preferred programming language")
    search_parser.add_argument("--min-stars", type=positive_int, help="Minimum star count")
    search_parser.add_argument("--pushed-after", help="Minimum pushed date, for example: 2025-01-01")
    search_parser.add_argument("--limit", type=positive_int, default=5, help="Number of candidates")
    search_parser.add_argument("--output", help="Write candidate JSON to this path")

    rank_parser = subparsers.add_parser("rank", help="Rank candidate JSON.")
    rank_parser.add_argument("input", help="Candidate JSON from the search command")
    rank_parser.add_argument("--requirement", required=True, help="User engineering requirement")
    rank_parser.add_argument("--top", type=positive_int, default=5, help="Number of recommendations")
    rank_parser.add_argument("--output", help="Write Markdown recommendations to this path")

    subparsers.add_parser("doctor", help="Check local configuration.")

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


def run_doctor():
    checks = [
        ("Version", __version__),
        ("Python", platform.python_version()),
        ("GITHUB_TOKEN", "configured" if os.getenv("GITHUB_TOKEN") else "missing"),
        ("LOCAL_LLM_MODEL", os.getenv("LOCAL_LLM_MODEL") or "missing"),
        ("LOCAL_LLM_BASE_URL", os.getenv("LOCAL_LLM_BASE_URL") or "default local endpoints"),
    ]

    for name, value in checks:
        print(f"{name}: {value}")

    return 0


def main(argv=None):
    configure_utf8_stdio()
    args = build_parser().parse_args(argv)

    try:
        if args.command == "search":
            return run_search(args)
        if args.command == "rank":
            return run_rank(args)
        if args.command == "doctor":
            return run_doctor()
    except GitHubAPIError as error:
        print(str(error), file=sys.stderr)
        return 2

    return 1
