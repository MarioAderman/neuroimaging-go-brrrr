# ruff: noqa: F401 # Ignore unused-imports in test below

"""Smoke tests to validate environment setup."""


def test_imports() -> None:
    """Verify core dependencies are importable."""
    import datasets
    import huggingface_hub
    import nibabel
    import pandas

    assert True


def test_scripts_exist() -> None:
    """Verify key scripts exist."""
    from pathlib import Path

    scripts = Path("scripts")
    assert scripts.exists()
    assert (scripts / "download_ds004884.sh").exists()
