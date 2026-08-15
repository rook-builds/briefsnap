# briefsnap

**One command. Five data sources. Your morning in one digest.**

`briefsnap` pulls Hacker News, RSS feeds, Bluesky profiles, GitHub repos, and arXiv papers in parallel and formats them as a combined morning briefing — text or JSON.

```
$ briefsnap
# Morning Briefing — August 15, 2026

## Hacker News

1. **Show HN: I built a thing**  (342 points · 87 comments · by someone)
   https://example.com/thing
...
```

## Install

```bash
pip install briefsnap
```

Requires Python 3.10+. Pulls in the five `*snap` sibling packages automatically.

## Quickstart

```bash
# Default: HN top 5 stories
briefsnap

# More HN stories
briefsnap --hn 10

# Add an RSS feed
briefsnap --rss https://simonwillison.net/atom/everything/

# Follow a Bluesky handle
briefsnap --bsky simonw.bsky.social

# Watch a GitHub repo
briefsnap --repo simonw/llm

# arXiv search
briefsnap --arxiv "LLM agents"

# Mix and match
briefsnap --hn 5 --rss https://news.ycombinator.com/rss --bsky simonw.bsky.social

# JSON output
briefsnap --output json | jq .
```

## Config file

For a repeatable daily briefing, drop a `briefsnap.toml` anywhere and point at it with `--config`:

```toml
[hackersnap]
enabled = true
limit   = 5
type    = "top"   # top / new / best / ask / show / job

[feedsnap]
feeds = [
  { url = "https://simonwillison.net/atom/everything/", limit = 5 },
  { url = "https://www.joelonsoftware.com/feed/", limit = 3 },
]

[bskysnap]
handles = [
  { handle = "simonw.bsky.social", limit = 5 },
]

[reposnap]
repos = [
  { repo = "simonw/llm", limit = 5 },
]

[arxivsnap]
queries = [
  { query = "LLM agents", limit = 3 },
]
```

```bash
briefsnap --config briefsnap.toml
briefsnap --config briefsnap.toml --output json
```

CLI flags override the config file — handy for one-off adjustments:

```bash
briefsnap --config briefsnap.toml --hn 10
```

## Output modes

| Flag | Description |
|------|-------------|
| `--output text` | Markdown digest (default) |
| `--output json` | Structured JSON with date envelope |

## Agent / ACLI support

```bash
briefsnap introspect   # ACLI-compliant JSON description
briefsnap skill        # agentskills.io SKILL.md
```

## How it works

- Each source is fetched in a **separate thread** (`ThreadPoolExecutor`) — five sources run in parallel, not serially.
- One source failing (network error, bad feed) does **not** kill the digest — it falls back to an empty section.
- Uses [`hackersnap`](https://pypi.org/project/hackersnap/), [`feedsnap`](https://pypi.org/project/feedsnap/), [`bskysnap`](https://pypi.org/project/bskysnap/), [`rook-reposnap`](https://pypi.org/project/rook-reposnap/), and [`arxivsnap`](https://pypi.org/project/arxivsnap/) as library imports.

## License

MIT
