"""briefsnap core — parallel compositor of all five snap tools.

Fetches HN, RSS feeds, Bluesky handles, GitHub repos, and arXiv papers
in parallel (ThreadPoolExecutor) and formats a combined morning digest.
"""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import date
from typing import Any

import hackersnap.core as hn_core
import feedsnap.core as feed_core
import bskysnap.core as bsky_core
import reposnap.core as repo_core
import arxivsnap.core as arxiv_core


def run_digest(cfg: dict) -> dict[str, Any]:
    """Fetch all enabled sources in parallel.

    Returns dict mapping source key -> results (list[Item] or dict for reposnap).
    One failing source does NOT kill the digest — it falls back to [].
    """
    tasks: list[tuple] = []

    if cfg.get("hackersnap", {}).get("enabled"):
        hn = cfg["hackersnap"]
        tasks.append(
            ("hn", hn_core.fetch, [hn.get("type", "top")], {"limit": hn.get("limit", 5)})
        )

    for feed_cfg in cfg.get("feedsnap", {}).get("feeds", []):
        url   = feed_cfg["url"]   if isinstance(feed_cfg, dict) else feed_cfg
        limit = feed_cfg.get("limit", 5) if isinstance(feed_cfg, dict) else 5
        tasks.append((f"feed:{url}", feed_core.fetch, [url], {"limit": limit}))

    for h_cfg in cfg.get("bskysnap", {}).get("handles", []):
        handle = h_cfg["handle"] if isinstance(h_cfg, dict) else h_cfg
        limit  = h_cfg.get("limit", 5) if isinstance(h_cfg, dict) else 5
        tasks.append((f"bsky:{handle}", bsky_core.fetch, [handle], {"limit": limit}))

    for r_cfg in cfg.get("reposnap", {}).get("repos", []):
        repo  = r_cfg["repo"]  if isinstance(r_cfg, dict) else r_cfg
        limit = r_cfg.get("limit", 5) if isinstance(r_cfg, dict) else 5
        tasks.append((f"repo:{repo}", repo_core.fetch, [repo], {"limit": limit}))

    for q_cfg in cfg.get("arxivsnap", {}).get("queries", []):
        query = q_cfg["query"] if isinstance(q_cfg, dict) else q_cfg
        limit = q_cfg.get("limit", 3) if isinstance(q_cfg, dict) else 3
        tasks.append((f"arxiv:{query}", arxiv_core.fetch, [query], {"limit": limit}))

    if not tasks:
        return {}

    results: dict[str, Any] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(fn, *args, **kwargs): key
            for key, fn, args, kwargs in tasks
        }
        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception:
                results[key] = []  # graceful degradation

    return results


def to_text(results: dict, cfg: dict) -> str:  # noqa: ARG001
    """Format all results as a combined markdown morning briefing."""
    today = date.today().strftime("%B %d, %Y")
    sections = [f"# Morning Briefing — {today}", ""]

    for key, items in results.items():
        if not items:
            continue
        if key == "hn":
            sections.append("## Hacker News\n")
            sections.append(hn_core.to_text(items))
        elif key.startswith("feed:"):
            sections.append("## RSS Feed\n")
            sections.append(feed_core.to_text(items))
        elif key.startswith("bsky:"):
            handle = key[5:]
            sections.append(f"## Bluesky @{handle}\n")
            sections.append(bsky_core.to_text(items))
        elif key.startswith("repo:"):
            repo_name = key[5:]
            sections.append(f"## GitHub: {repo_name}\n")
            sections.append(repo_core.to_text(items))
        elif key.startswith("arxiv:"):
            query = key[6:]
            sections.append(f"## arXiv: {query}\n")
            sections.append(arxiv_core.to_text(items))
        sections.append("")

    return "\n".join(sections)


def to_json(results: dict, cfg: dict) -> str:  # noqa: ARG001
    """Format all results as JSON with a date envelope."""
    today = date.today().isoformat()
    output: dict = {"date": today, "sources": {}}

    for key, items in results.items():
        if isinstance(items, list):
            serialized = []
            for it in items:
                try:
                    serialized.append(asdict(it))
                except Exception:
                    serialized.append(str(it))
            output["sources"][key] = serialized
        elif isinstance(items, dict):
            output["sources"][key] = items
        else:
            output["sources"][key] = str(items)

    return json.dumps(output, indent=2, default=str, ensure_ascii=False)
