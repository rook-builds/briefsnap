"""Shared fixtures for briefsnap tests.

Stubs all five snap packages in sys.modules *before* any briefsnap
module is imported, so the test suite runs cleanly whether or not the
real packages are installed in the environment.

If the real packages ARE installed, sys.modules.setdefault() leaves them
in place and the stubs are never applied.  Either way, individual tests
can still override specific functions with unittest.mock.patch().

IMPORTANT: Parent packages must be ModuleType (not MagicMock) so that
`import hackersnap.core as hn_core` correctly resolves to
sys.modules["hackersnap.core"] rather than the MagicMock's auto-child.
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
    m.fetch = MagicMock(return_value=[])      # type: ignore[attr-defined]
    m.to_text = MagicMock(return_value="")    # type: ignore[attr-defined]
    m.to_json = MagicMock(return_value="[]")  # type: ignore[attr-defined]
    m.to_table = MagicMock(return_value="")   # type: ignore[attr-defined]
    m.to_csv = MagicMock(return_value="")     # type: ignore[attr-defined]
    return m


def _make_pkg_stub(pkg: str, core_stub: ModuleType) -> ModuleType:
    """Return a minimal ModuleType that mimics the top-level <pkg> package.

    Must be a real ModuleType (not MagicMock) so that Python's import
    machinery correctly resolves `import <pkg>.core as x` to the stub
    module in sys.modules rather than an auto-generated child attribute.
    """
    m = ModuleType(pkg)
    m.core = core_stub                        # type: ignore[attr-defined]
    # Re-export the most common top-level names (mirrors __init__.py)
    m.fetch = core_stub.fetch                 # type: ignore[attr-defined]
    m.to_text = core_stub.to_text             # type: ignore[attr-defined]
    m.to_json = core_stub.to_json             # type: ignore[attr-defined]
    m.to_table = core_stub.to_table           # type: ignore[attr-defined]
    m.to_csv = core_stub.to_csv               # type: ignore[attr-defined]
    return m


_SNAP_PKGS = ["hackersnap", "feedsnap", "bskysnap", "reposnap", "arxivsnap"]

for _pkg in _SNAP_PKGS:
    _core_stub = _make_core_stub(_pkg)
    _pkg_stub = _make_pkg_stub(_pkg, _core_stub)
    sys.modules.setdefault(_pkg, _pkg_stub)
    sys.modules.setdefault(f"{_pkg}.core", _core_stub)


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
