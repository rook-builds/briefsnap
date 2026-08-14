"""Smoke tests for briefsnap package imports."""


def test_import_briefsnap():
    import briefsnap
    assert hasattr(briefsnap, "__version__")


def test_version_string():
    import briefsnap
    assert isinstance(briefsnap.__version__, str)
    assert "." in briefsnap.__version__


def test_core_imports():
    from briefsnap.core import run_digest, to_json, to_text
    assert callable(run_digest)
    assert callable(to_text)
    assert callable(to_json)


def test_config_imports():
    from briefsnap.config import load_config
    assert callable(load_config)
