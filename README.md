# briefsnap

Morning briefing aggregator. One command pulls Hacker News, RSS feeds, Bluesky profiles, GitHub repos, and arXiv papers — all in parallel — and formats a combined digest.

## Install

```bash
pip install briefsnap
```

## Quick start

```bash
# Default: HN top-5 (no config needed)
briefsnap

# Full digest with flags
briefsnap --hn 5 \
  --rss https://simonwillison.net/atom/everything/ \
  --bsky swyx.bsky.social \
  --repo simonw/llm \
  --arxiv "large language models"

# Load from config file
briefsnap --config briefsnap.toml

# JSON output
briefsnap --output json | jq .
```

## Config file (TOML)

```toml
# briefsnap.toml

[hackersnap]
enabled = true
limit = 5
type = "top"    # top | new | best | ask | show | job

[feedsnap]
feeds = [
  { url = "https://simonwillison.net/atom/everything/", limit = 3 },
  { url = "https://martinfowler.com/feed.atom", limit = 3 },
]

[bskysnap]
handles = [
  { handle = "swyx.bsky.social", limit = 5 },
]

[reposnap]
repos = [
  { repo = "simonw/llm", limit = 5 },
]

[arxivsnap]
queries = [
  { query = "large language models agents", limit = 3 },
]
```

## Output formats

| Flag | Format |
|------|--------|
| `--output text` (default) | Markdown digest, one section per source |
| `--output json` | JSON envelope: `{ "date": ..., "sources": { ... } }` |

## Agent interface

```bash
briefsnap introspect   # ACLI-compliant JSON
briefsnap skill        # agentskills.io SKILL.md
```

## Data sources

briefsnap composes five snap tools — each is also independently useful:

| Tool | PyPI | Source |
|------|------|--------|
| [hackersnap](https://github.com/rook-builds/hackersnap) | `hackersnap` | Hacker News |
| [feedsnap](https://github.com/rook-builds/feedsnap) | `feedsnap` | RSS/Atom feeds |
| [bskysnap](https://github.com/rook-builds/bskysnap) | `bskysnap` | Bluesky |
| [reposnap](https://github.com/rook-builds/reposnap) | `rook-reposnap` | GitHub repos |
| [arxivsnap](https://github.com/rook-builds/arxivsnap) | `arxivsnap` | arXiv papers |

All sources are fetched in parallel — a five-source digest takes roughly as long as the slowest single source.

## License

MIT
