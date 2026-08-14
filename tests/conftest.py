"""Shared fixtures for briefsnap tests.

Stubs all five snap packages in sys.modules *before* any briefsnap
module is imported, so the test suite runs cleanly whether or not the
real packages are installed in the environment.

If the real packages ARE installed, sys.modules.setdefault() leaves them
in place and the stubs are never applied.  Either way, individual tests
can still override specific functions with unittest.mock.patch().
"""
from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# Snap-package stubs — must run before any briefsnap import
# ---------------------------------------------------------------------------

def _make_core_stub(pkg: str) -> ModuleType:
    """Return a minimal module object that mimics <pkg>.core."""
    m = ModuleType(f"{pkg}.core")
    m.fetch = MagicMock(return_value=[])     # type: ignore[attr-defined]
    m.to_text = MagicMock(return_value="")   # type: ignore[attr-defined]
    m.to_json = MagicMock(return_value="[]") # type: ignore[attr-defined]
    m.to_table = MagicMock(return_value="")  # type: ignore[attr-defined]
    m.to_csv = MagicMock(return_value="")    # type: ignore[attr-defined]
    return m


_SNAP_PKGS = ["hackersnap", "feedsnap", "bskysnap", "reposnap", "arxivsnap"]

for _pkg in _SNAP_PKGS:
    sys.modules.setdefault(_pkg, MagicMock())
    sys.modules.setdefault(f"{_pkg}.core", _make_core_stub(_pkg))


# ---------------------------------------------------------------------------
# pytest fixtures
# ---------------------------------------------------------------------------

import pytest  # noqa: E402  (must come after sys.modules manipulation)


@pytest.fixture
def base_cfg():
    """Minimal config with all sources disabled."""
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
