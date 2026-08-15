"""Agent-CLI introspection: `briefsnap introspect` and `briefsnap skill`.

Lets any AI agent discover how to drive this tool without a human in the loop.
"""
import json

from . import __version__


def get_introspect_json() -> str:
    return json.dumps(
        {
            "name": "briefsnap",
            "version": __version__,
            "description": (
                "Morning briefing aggregator — one command pulls HN, RSS, "
                "Bluesky, GitHub, and arXiv into a single digest"
            ),
            "commands": [
                {
                    "name": "briefsnap",
                    "usage": (
                        "briefsnap [--config FILE] [--hn N] [--rss URL...] "
                        "[--bsky HANDLE...] [--repo OWNER/REPO...] "
                        "[--arxiv QUERY...] [--output text|json]"
                    ),
                    "description": (
                        "Fetch multiple data sources in parallel and print a "
                        "combined morning digest. Pass --config for a repeatable "
                        "TOML-based briefing; use CLI flags for one-offs."
                    ),
                    "options": [
                        {"flag": "--config / -c", "type": "path", "description": "Path to TOML config file"},
                        {"flag": "--hn", "type": "int", "description": "Number of HN top stories to include"},
                        {"flag": "--rss", "type": "str (multiple)", "description": "RSS feed URL(s)"},
                        {"flag": "--bsky", "type": "str (multiple)", "description": "Bluesky handle(s)"},
                        {"flag": "--repo", "type": "str (multiple)", "description": "GitHub repo(s) as owner/name"},
                        {"flag": "--arxiv", "type": "str (multiple)", "description": "arXiv search query/queries"},
                        {"flag": "--output / -o", "type": "choice", "choices": ["text", "json"], "default": "text"},
                    ],
                },
                {
                    "name": "briefsnap introspect",
                    "usage": "briefsnap introspect",
                    "description": "Print this ACLI-compliant JSON description.",
                },
                {
                    "name": "briefsnap skill",
                    "usage": "briefsnap skill",
                    "description": "Print an agentskills.io-compliant SKILL.md.",
                },
            ],
        },
        indent=2,
    )


def get_skill_md() -> str:
    return (
        "---\n"
        "name: briefsnap\n"
        f"description: Morning briefing aggregator — one command pulls HN, RSS, Bluesky, GitHub, and arXiv into a single digest\n"
        "license: MIT\n"
        "metadata:\n"
        "  author: rook-builds\n"
        f"  version: {__version__}\n"
        "---\n\n"
        "# briefsnap\n\n"
        "Fetch HN, RSS feeds, Bluesky handles, GitHub repos, and arXiv papers "
        "in parallel and print a combined morning digest.\n\n"
        "## Core usage\n\n"
        "```\n"
        "briefsnap                          # HN top 5 (default)\n"
        "briefsnap --hn 10                  # HN top 10\n"
        "briefsnap --rss URL                # Add RSS feed\n"
        "briefsnap --bsky handle            # Bluesky profile\n"
        "briefsnap --repo owner/repo        # GitHub repo\n"
        "briefsnap --arxiv 'LLM agents'     # arXiv search\n"
        "briefsnap --config briefsnap.toml  # TOML config file\n"
        "```\n\n"
        "## Output modes\n\n"
        "- `--output text` — markdown digest (default)\n"
        "- `--output json` — structured JSON with date envelope\n\n"
        "## Exit codes\n\n"
        "- `0` — success\n"
        "- `1` — fatal error (bad config, etc.)\n\n"
        "## Agent discovery\n\n"
        "- `briefsnap introspect` — ACLI-compliant JSON\n"
        "- `briefsnap skill` — this document\n"
    )
