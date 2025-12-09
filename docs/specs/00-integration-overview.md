# Integration Spec: bids-hub → neuroimaging-go-brrrr

**Status**: Ready for Implementation
**Source**: `_reference_repos/bids-hub/` (git-delinked copy)

---

## Executive Summary

We're integrating a complete, battle-tested production pipeline (1,976 lines) into an empty skeleton.

| What Exists | What We're Adding |
|-------------|-------------------|
| Empty `src/neuroimaging_go_brrrr/` | Full `src/bids_hub/` (13 Python files) |
| Broken toy script | Working CLI with 10+ commands |
| Missing deps | Complete dependency set + critical git pin |
| No tests | 9 test files with fixtures |

---

## Phase Overview

| Phase | Description | Complexity |
|-------|-------------|------------|
| **Phase 1** | Copy `src/bids_hub/` | Trivial (copy) |
| **Phase 2** | Update `pyproject.toml` | Medium (merge configs) |
| **Phase 3** | Copy tests | Trivial (copy) |
| **Phase 4** | Delete obsolete scripts | Trivial (delete) |
| **Phase 5** | Verify & commit | Verify (run tests) |

---

## Decision: Keep `bids_hub` Package Name

**DO NOT rename to `neuroimaging_go_brrrr`**

Reasons:
1. `bids_hub` is accurate (BIDS → HuggingFace Hub)
2. CLI is `bids-hub` (clear, memorable)
3. Renaming breaks imports in all test files
4. The repo name (`neuroimaging-go-brrrr`) ≠ package name (that's normal)

The package inside is `bids_hub`. The repo that hosts it is `neuroimaging-go-brrrr`.

---

## Files to Copy

### Source → Destination

```
_reference_repos/bids-hub/src/bids_hub/    →    src/bids_hub/
_reference_repos/bids-hub/tests/           →    tests/
_reference_repos/bids-hub/UPSTREAM_BUG.md  →    docs/UPSTREAM_BUG.md
_reference_repos/bids-hub/CLAUDE.md        →    CLAUDE.md (merge or replace)
```

### Files to Delete

```
src/neuroimaging_go_brrrr/          # Empty skeleton, useless
scripts/push_to_hub_ds004884_full.py  # Broken toy script
scripts/download_ds004884.sh          # One-liner, not needed
```

### Files to Keep

```
scripts/visualization/              # Tobias's notebooks (consumption demo)
docs/brainstorming/                 # Context
```

---

## pyproject.toml Changes

### Current (broken)
```toml
name = "neuroimaging-go-brrrr"
dependencies = [
  "datasets>=3.4.0",
  "huggingface-hub>=0.32.0",
  "nibabel>=5.0.0",
  "pandas>=2.0.0",
  "pandas-stubs>=2.3.3.251201",  # This is a dev dep, not runtime
]
# Missing: typer, openpyxl, hf-xet
# Missing: [project.scripts]
# Missing: [tool.uv.sources] datasets pin
```

### Target (working)
```toml
name = "neuroimaging-go-brrrr"  # Keep repo name
version = "0.2.0"

dependencies = [
  "datasets>=3.4.0",
  "hf-xet>=1.0.0",
  "huggingface-hub>=0.32.0",
  "nibabel>=5.0.0",
  "openpyxl>=3.1.5",
  "pandas>=2.0.0",
  "typer>=0.12.0",
]

[project.scripts]
bids-hub = "bids_hub.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["src/bids_hub"]

[tool.uv.sources]
datasets = { git = "https://github.com/huggingface/datasets.git", rev = "004a5bf4addd9293d6d40f43360c03c8f7e42b28" }
```

---

## Execution Order

1. **Phase 1**: `cp -r _reference_repos/bids-hub/src/bids_hub src/`
2. **Phase 2**: Update `pyproject.toml` (detailed in next spec)
3. **Phase 3**: `cp -r _reference_repos/bids-hub/tests .` (replace existing)
4. **Phase 4**: `rm -rf src/neuroimaging_go_brrrr scripts/push_to_hub*.py scripts/download*.sh`
5. **Phase 5**: `uv sync && uv run pytest && uv run bids-hub --help`

---

## Success Criteria

```bash
# CLI works
bids-hub --help
bids-hub list
bids-hub arc --help
bids-hub isles24 --help

# Tests pass
uv run pytest -v

# Imports work
python -c "from bids_hub import build_and_push_arc, ValidationResult"
```
