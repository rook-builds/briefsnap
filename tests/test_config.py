"""Tests for briefsnap.config — no network calls."""
import pytest
from briefsnap.config import load_config


def test_default_hn_enabled():
    cfg = load_config()
    assert cfg["hackersnap"]["enabled"] is True
    assert cfg["hackersnap"]["limit"] == 5
    assert cfg["hackersnap"]["type"] == "top"


def test_other_sources_disabled_by_default():
    cfg = load_config()
    assert cfg["feedsnap"]["enabled"] is False
    assert cfg["bskysnap"]["enabled"] is False
    assert cfg["reposnap"]["enabled"] is False
    assert cfg["arxivsnap"]["enabled"] is False


def test_hn_limit_override():
    cfg = load_config(hn_limit=10)
    assert cfg["hackersnap"]["limit"] == 10
    assert cfg["hackersnap"]["enabled"] is True


def test_rss_override():
    cfg = load_config(rss_urls=("https://example.com/rss",))
    assert cfg["feedsnap"]["enabled"] is True
    assert len(cfg["feedsnap"]["feeds"]) == 1
    assert cfg["feedsnap"]["feeds"][0]["url"] == "https://example.com/rss"


def test_bsky_override():
    cfg = load_config(bsky_handles=("user.bsky.social",))
    assert cfg["bskysnap"]["enabled"] is True
    assert len(cfg["bskysnap"]["handles"]) == 1


def test_repo_override():
    cfg = load_config(repos=("owner/repo",))
    assert cfg["reposnap"]["enabled"] is True
    assert len(cfg["reposnap"]["repos"]) == 1


def test_arxiv_override():
    cfg = load_config(arxiv_queries=("machine learning",))
    assert cfg["arxivsnap"]["enabled"] is True
    assert len(cfg["arxivsnap"]["queries"]) == 1


def test_multiple_rss():
    cfg = load_config(rss_urls=("https://a.com/rss", "https://b.com/rss"))
    assert len(cfg["feedsnap"]["feeds"]) == 2


def test_toml_config_hn(tmp_path):
    cfg_file = tmp_path / "brief.toml"
    cfg_file.write_bytes(b"""
[hackersnap]
enabled = true
limit = 7
type = "best"
""")
    cfg = load_config(config_path=str(cfg_file))
    assert cfg["hackersnap"]["limit"] == 7
    assert cfg["hackersnap"]["type"] == "best"


def test_toml_config_feedsnap(tmp_path):
    cfg_file = tmp_path / "brief.toml"
    cfg_file.write_bytes(b"""
[feedsnap]
feeds = [{url = "https://example.com/rss", limit = 3}]
""")
    cfg = load_config(config_path=str(cfg_file))
    assert cfg["feedsnap"]["enabled"] is True
    assert len(cfg["feedsnap"]["feeds"]) == 1


def test_cli_overrides_file(tmp_path):
    cfg_file = tmp_path / "brief.toml"
    cfg_file.write_bytes(b"""
[hackersnap]
limit = 3
""")
    cfg = load_config(config_path=str(cfg_file), hn_limit=10)
    assert cfg["hackersnap"]["limit"] == 10  # CLI wins
