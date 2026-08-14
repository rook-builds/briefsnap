"""Shared fixtures for briefsnap tests."""
import pytest


@pytest.fixture
def base_cfg():
    """Minimal config with all sources disabled (HN too)."""
    return {
        "hackersnap": {"enabled": False, "limit": 5, "type": "top"},
        "feedsnap":   {"enabled": False, "feeds": []},
        "bskysnap":   {"enabled": False, "handles": []},
        "reposnap":   {"enabled": False, "repos": []},
        "arxivsnap":  {"enabled": False, "queries": []},
    }


@pytest.fixture
def hn_only_cfg():
    """Config with only HN enabled."""
    return {
        "hackersnap": {"enabled": True, "limit": 3, "type": "top"},
        "feedsnap":   {"enabled": False, "feeds": []},
        "bskysnap":   {"enabled": False, "handles": []},
        "reposnap":   {"enabled": False, "repos": []},
        "arxivsnap":  {"enabled": False, "queries": []},
    }
