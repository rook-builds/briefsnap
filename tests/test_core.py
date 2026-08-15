"""Tests for briefsnap.core — all network calls mocked."""
from __future__ import annotations

import json
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest

from briefsnap.core import run_digest, to_json, to_text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_items(n: int = 3) -> list:
    items = []
    for i in range(n):
        m = MagicMock()
        m.title = f"Story {i}"
        m.url = f"https://example.com/{i}"
        m.score = 100
        m.comments = 50
        m.author = "user"
        m.created_at = None
        m.body = ""
        items.append(m)
    return items


def _base_cfg() -> dict:
    return {
        "hackersnap": {"enabled": False, "limit": 5, "type": "top"},
        "feedsnap":   {"enabled": False, "feeds": []},
        "bskysnap":   {"enabled": False, "handles": []},
        "reposnap":   {"enabled": False, "repos": []},
        "arxivsnap":  {"enabled": False, "queries": []},
    }


# ---------------------------------------------------------------------------
# run_digest tests
# ---------------------------------------------------------------------------

def test_run_digest_empty_returns_empty_dict():
    cfg = _base_cfg()
    results = run_digest(cfg)
    assert results == {}


def test_run_digest_hn_only():
    cfg = _base_cfg()
    cfg["hackersnap"]["enabled"] = True
    items = _mock_items(3)
    with patch("hackersnap.core.fetch") as mock_fetch:
        mock_fetch.return_value = items
        results = run_digest(cfg)
    assert "hn" in results
    assert len(results["hn"]) == 3


def test_run_digest_graceful_failure():
    """If one source throws, results[key] == [] — digest keeps running."""
    cfg = _base_cfg()
    cfg["hackersnap"]["enabled"] = True
    with patch("hackersnap.core.fetch") as mock_fetch:
        mock_fetch.side_effect = RuntimeError("network down")
        results = run_digest(cfg)
    assert results.get("hn") == []


def test_run_digest_rss_source():
    cfg = _base_cfg()
    cfg["feedsnap"]["enabled"] = True
    cfg["feedsnap"]["feeds"] = [{"url": "https://example.com/rss", "limit": 3}]
    items = _mock_items(3)
    with patch("feedsnap.core.fetch") as mock_fetch:
        mock_fetch.return_value = items
        results = run_digest(cfg)
    assert "feed:https://example.com/rss" in results


def test_run_digest_bsky_source():
    cfg = _base_cfg()
    cfg["bskysnap"]["enabled"] = True
    cfg["bskysnap"]["handles"] = [{"handle": "user.bsky.social", "limit": 3}]
    items = _mock_items(3)
    with patch("bskysnap.core.fetch") as mock_fetch:
        mock_fetch.return_value = items
        results = run_digest(cfg)
    assert "bsky:user.bsky.social" in results


def test_run_digest_arxiv_source():
    cfg = _base_cfg()
    cfg["arxivsnap"]["enabled"] = True
    cfg["arxivsnap"]["queries"] = [{"query": "LLMs", "limit": 3}]
    items = _mock_items(3)
    with patch("arxivsnap.core.fetch") as mock_fetch:
        mock_fetch.return_value = items
        results = run_digest(cfg)
    assert "arxiv:LLMs" in results


# ---------------------------------------------------------------------------
# to_text tests
# ---------------------------------------------------------------------------

def test_to_text_contains_date_header():
    cfg = _base_cfg()
    items = _mock_items(2)
    with patch("hackersnap.core.to_text") as mock_txt:
        mock_txt.return_value = "HN content\n"
        result = to_text({"hn": items}, cfg)
    assert "Morning Briefing" in result


def test_to_text_hn_section():
    cfg = _base_cfg()
    items = _mock_items(2)
    with patch("hackersnap.core.to_text") as mock_txt:
        mock_txt.return_value = "HN content\n"
        result = to_text({"hn": items}, cfg)
    assert "Hacker News" in result
    assert "HN content" in result


def test_to_text_skips_empty_source():
    cfg = _base_cfg()
    # Empty list — section should not appear
    result = to_text({"hn": []}, cfg)
    assert "Hacker News" not in result


def test_to_text_rss_section():
    cfg = _base_cfg()
    items = _mock_items(2)
    with patch("feedsnap.core.to_text") as mock_txt:
        mock_txt.return_value = "RSS content\n"
        result = to_text({"feed:https://example.com/rss": items}, cfg)
    assert "RSS Feed" in result


def test_to_text_bsky_section():
    cfg = _base_cfg()
    items = _mock_items(2)
    with patch("bskysnap.core.to_text") as mock_txt:
        mock_txt.return_value = "Bsky content\n"
        result = to_text({"bsky:user.bsky.social": items}, cfg)
    assert "Bluesky @user.bsky.social" in result


def test_to_text_arxiv_section():
    cfg = _base_cfg()
    items = _mock_items(2)
    with patch("arxivsnap.core.to_text") as mock_txt:
        mock_txt.return_value = "arXiv content\n"
        result = to_text({"arxiv:LLMs": items}, cfg)
    assert "arXiv: LLMs" in result


# ---------------------------------------------------------------------------
# to_json tests
# ---------------------------------------------------------------------------

@dataclass
class FakeItem:
    title: str
    url: str = ""
    author: str = ""
    score: int = 0
    comments: int = 0
    created_at: object = None
    body: str = ""


def test_to_json_structure():
    items = [FakeItem("Test Story")]
    result = to_json({"hn": items}, {})
    data = json.loads(result)
    assert "date" in data
    assert "sources" in data
    assert "hn" in data["sources"]
    assert data["sources"]["hn"][0]["title"] == "Test Story"


def test_to_json_empty():
    result = to_json({}, {})
    data = json.loads(result)
    assert data["sources"] == {}


def test_to_json_graceful_non_dataclass():
    """Items that can't be asdict'd get str'd instead of crashing."""
    items = [MagicMock()]  # not a real dataclass
    result = to_json({"hn": items}, {})
    data = json.loads(result)
    assert "hn" in data["sources"]
