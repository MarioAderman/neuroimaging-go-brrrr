# Integration Specs: bids-hub → neuroimaging-go-brrrr

These specs document the integration of the complete `bids-hub` production pipeline into this repository.

## Execution Order

| Phase | Spec | Complexity |
|-------|------|------------|
| 1 | [01-copy-source.md](./01-copy-source.md) | Trivial |
| 2 | [02-update-pyproject.md](./02-update-pyproject.md) | Medium |
| 3 | [03-copy-tests.md](./03-copy-tests.md) | Trivial |
| 4 | [04-cleanup.md](./04-cleanup.md) | Trivial |
| 5 | [05-verify.md](./05-verify.md) | Verification |

## Overview

See [00-integration-overview.md](./00-integration-overview.md) for:
- What we're integrating (1,976 lines of production code)
- Why we keep `bids_hub` as package name
- File mapping (source → destination)
- Success criteria

## Quick Reference

```bash
# Phase 1: Copy source
cp -r _reference_repos/bids-hub/src/bids_hub src/

# Phase 2: Update pyproject.toml (see spec for details)

# Phase 3: Copy tests
rm -rf tests/ && cp -r _reference_repos/bids-hub/tests .

# Phase 4: Cleanup
rm -rf src/neuroimaging_go_brrrr/
rm scripts/push_to_hub_ds004884_full.py scripts/download_ds004884.sh

# Phase 5: Verify
uv sync --all-extras && uv run pytest -v && uv run bids-hub --help
```

## Source

All code comes from: `_reference_repos/bids-hub/` (git-delinked copy of https://github.com/The-Obstacle-Is-The-Way/bids-hub)
