"""briefsnap config — load from TOML file with CLI overrides.

Default (no config file, no flags): HN top-5 only.
"""
from __future__ import annotations

import sys
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[no-redef]


def load_config(
    config_path: Optional[str] = None,
    hn_limit: Optional[int] = None,
    rss_urls: tuple = (),
    bsky_handles: tuple = (),
    repos: tuple = (),
    arxiv_queries: tuple = (),
) -> dict:
    """Load config from a TOML file (if given), then apply CLI overrides.

    Returns a normalised config dict consumed by core.run_digest().
    """
    cfg: dict = {
        "hackersnap": {"enabled": True, "limit": 5, "type": "top"},
        "feedsnap":   {"enabled": False, "feeds": []},
        "bskysnap":   {"enabled": False, "handles": []},
        "reposnap":   {"enabled": False, "repos": []},
        "arxivsnap":  {"enabled": False, "queries": []},
    }

    if config_path:
        with open(config_path, "rb") as f:
            file_cfg = tomllib.load(f)
        for section, values in file_cfg.items():
            if section in cfg and isinstance(values, dict):
                cfg[section].update(values)
                # Any non-hackersnap section present in the file is opt-in
                if section != "hackersnap" and values:
                    cfg[section]["enabled"] = True

    # CLI flags take precedence over file
    if hn_limit is not None:
        cfg["hackersnap"]["limit"] = hn_limit
        cfg["hackersnap"]["enabled"] = True
    if rss_urls:
        cfg["feedsnap"]["enabled"] = True
        cfg["feedsnap"]["feeds"] = [{"url": u, "limit": 5} for u in rss_urls]
    if bsky_handles:
        cfg["bskysnap"]["enabled"] = True
        cfg["bskysnap"]["handles"] = [{"handle": h, "limit": 5} for h in bsky_handles]
    if repos:
        cfg["reposnap"]["enabled"] = True
        cfg["reposnap"]["repos"] = [{"repo": r, "limit": 5} for r in repos]
    if arxiv_queries:
        cfg["arxivsnap"]["enabled"] = True
        cfg["arxivsnap"]["queries"] = [{"query": q, "limit": 3} for q in arxiv_queries]

    return cfg
