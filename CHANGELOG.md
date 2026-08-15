# Changelog

## v0.1.0 — 2026-08-15

Initial release.

### Features

- **Parallel fetch** — HN, RSS, Bluesky, GitHub, and arXiv are fetched concurrently via `ThreadPoolExecutor`. Five sources take roughly as long as the slowest one.
- **Graceful degradation** — if one source fails (network error, bad feed URL), the rest of the digest is unaffected. That section is simply omitted.
- **Two output modes** — `text` (markdown digest, default) and `json` (structured envelope with date).
- **TOML config** — repeatable daily briefings via a `briefsnap.toml` file. Each section (`[hackersnap]`, `[feedsnap]`, `[bskysnap]`, `[reposnap]`, `[arxivsnap]`) is independently configurable and opt-in.
- **CLI flags** — `--hn N`, `--rss URL`, `--bsky handle`, `--repo owner/repo`, `--arxiv query`. Can be combined. CLI flags override the config file.
- **ACLI support** — `briefsnap introspect` returns a JSON description, `briefsnap skill` returns an agentskills.io-compliant SKILL.md.
- **Zero new dependencies** beyond the five `*snap` sibling packages and `click`.

### Snap family

briefsnap composes:
- [`hackersnap`](https://pypi.org/project/hackersnap/) — Hacker News
- [`feedsnap`](https://pypi.org/project/feedsnap/) — RSS/Atom feeds
- [`bskysnap`](https://pypi.org/project/bskysnap/) — Bluesky profiles
- [`rook-reposnap`](https://pypi.org/project/rook-reposnap/) — GitHub repos
- [`arxivsnap`](https://pypi.org/project/arxivsnap/) — arXiv papers
