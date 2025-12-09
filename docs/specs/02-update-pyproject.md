# Phase 2: Update pyproject.toml

**Complexity**: Medium (careful merge)

---

## Current State (neuroimaging-go-brrrr)

```toml
[project]
name = "neuroimaging-go-brrrr"
version = "0.1.0"
description = "Neuroimaging tools for HuggingFace Hub"
requires-python = ">=3.11"
dependencies = [
  "datasets>=3.4.0",
  "huggingface-hub>=0.32.0",
  "nibabel>=5.0.0",
  "pandas>=2.0.0",
  "pandas-stubs>=2.3.3.251201",  # WRONG: dev dep in runtime
]

[dependency-groups]
dev = [...]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest]
testpaths = ["tests"]
addopts = ["-v", "--tb=short"]

[tool.ruff]
target-version = "py311"
line-length = 100
extend-exclude = ["*.ipynb"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "PTH", "RUF"]
```

---

## Target State (after merge)

```toml
[project]
name = "neuroimaging-go-brrrr"
version = "0.2.0"
description = "Upload BIDS neuroimaging datasets to HuggingFace Hub"
readme = "README.md"
license = "Apache-2.0"
requires-python = ">=3.10"  # bids-hub supports 3.10+
authors = [
    { name = "The-Obstacle-Is-The-Way" },
    { name = "TobiasPitters" },
]
keywords = ["bids", "nifti", "neuroimaging", "huggingface", "datasets", "mri", "stroke", "aphasia"]

dependencies = [
    "datasets>=3.4.0",
    "hf-xet>=1.0.0",
    "huggingface-hub>=0.32.0",
    "nibabel>=5.0.0",
    "openpyxl>=3.1.5",
    "pandas>=2.0.0",
    "typer>=0.12.0",
]

[project.optional-dependencies]
dev = [
    "mypy>=1.11.0",
    "pandas-stubs>=2.0.0",
    "pre-commit>=3.0.0",
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.7.0",
]

[project.scripts]
bids-hub = "bids_hub.cli:app"

[project.urls]
Homepage = "https://github.com/CloseChoice/neuroimaging-go-brrrr"
Repository = "https://github.com/CloseChoice/neuroimaging-go-brrrr"
Issues = "https://github.com/CloseChoice/neuroimaging-go-brrrr/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/bids_hub"]

[tool.ruff]
line-length = 100
target-version = "py310"
extend-exclude = ["*.ipynb"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "PTH", "RUF"]
ignore = ["B008"]  # typer false positive

[tool.ruff.lint.isort]
known-first-party = ["bids_hub"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.mypy]
python_version = "3.10"
warn_unused_configs = true
disallow_untyped_defs = true
ignore_missing_imports = true
strict_optional = true

[tool.uv.sources]
# CRITICAL: Pin to specific commit until upstream PR #7896 is merged.
# PyPI stable has embed_table_storage bug causing SIGKILL on Sequence(Nifti()) after ds.shard()
datasets = { git = "https://github.com/huggingface/datasets.git", rev = "004a5bf4addd9293d6d40f43360c03c8f7e42b28" }
```

---

## Key Changes

| Section | Change | Why |
|---------|--------|-----|
| `dependencies` | Add `typer`, `openpyxl`, `hf-xet` | Required for CLI and ISLES24 |
| `dependencies` | Remove `pandas-stubs` | It's a dev dep |
| `requires-python` | `>=3.11` → `>=3.10` | bids-hub supports 3.10 |
| `[project.scripts]` | Add `bids-hub` CLI | Entry point |
| `[tool.hatch.build]` | Add `packages = ["src/bids_hub"]` | Tell hatch where package is |
| `[tool.uv.sources]` | Add datasets git pin | **CRITICAL**: Prevents SIGKILL |
| `[tool.ruff.lint]` | Add `ignore = ["B008"]` | Typer false positive |

---

## Verification

```bash
# Sync dependencies
uv sync --all-extras

# Verify CLI is installed
uv run bids-hub --help
```
