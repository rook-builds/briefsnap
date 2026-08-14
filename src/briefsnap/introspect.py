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
            "description": "Morning briefing aggregator — one command pulls HN, RSS, Bluesky, GitHub, and arXiv into a single digest",
            "commands": [
                {
                    "usage": "briefsnap [TARGET] --limit N --output text|json|table|csv",
                    "description": "Morning briefing aggregator — one command pulls HN, RSS, Bluesky, GitHub, and arXiv into a single digest",
                }
            ],
        },
        indent=2,
    )


def get_skill_md() -> str:
    return (
        "# briefsnap\n\n"
        "Morning briefing aggregator — one command pulls HN, RSS, Bluesky, GitHub, and arXiv into a single digest\n\n"
        "## Usage\n\n"
        "```\n"
        "briefsnap [TARGET] --limit 10 --output json\n"
        "```\n\n"
        "Outputs: text (default), json, table, csv.\n"
    )
