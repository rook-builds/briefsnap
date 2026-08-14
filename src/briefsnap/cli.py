"""briefsnap CLI — morning briefing aggregator."""
from __future__ import annotations

import sys

import click

from .config import load_config
from .core import run_digest, to_json, to_text
from .introspect import get_introspect_json, get_skill_md

_ACLI_COMMANDS = {"introspect", "skill"}


@click.command()
@click.argument("cmd", required=False, default=None)
@click.option("--config", "-c", "config_path", default=None, help="Path to TOML config file.")
@click.option("--hn", default=None, type=int, help="Include N Hacker News top stories.")
@click.option("--rss", multiple=True, help="RSS feed URL(s) to include.")
@click.option("--bsky", multiple=True, help="Bluesky handle(s) to include.")
@click.option("--repo", multiple=True, help="GitHub repo(s) to include (owner/name).")
@click.option("--arxiv", multiple=True, help="arXiv search query/queries.")
@click.option(
    "--output", "-o",
    default="text",
    show_default=True,
    type=click.Choice(["text", "json"]),
    help="Output format.",
)
def main(cmd, config_path, hn, rss, bsky, repo, arxiv, output):
    """Morning briefing aggregator — HN + RSS + Bluesky + GitHub + arXiv in one digest.

    Run with no args for a default HN top-5 digest.
    Pass --config briefsnap.toml for a full configured digest.

    \b
    Special commands:
      briefsnap introspect   ACLI-compliant JSON description
      briefsnap skill        agentskills.io SKILL.md
    """
    if cmd in _ACLI_COMMANDS:
        if cmd == "introspect":
            print(get_introspect_json())
        else:
            print(get_skill_md())
        sys.exit(0)

    cfg = load_config(
        config_path=config_path,
        hn_limit=hn,
        rss_urls=rss,
        bsky_handles=bsky,
        repos=repo,
        arxiv_queries=arxiv,
    )

    results = run_digest(cfg)

    if output == "json":
        click.echo(to_json(results, cfg))
    else:
        click.echo(to_text(results, cfg))


if __name__ == "__main__":
    main()
