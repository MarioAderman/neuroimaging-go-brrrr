# Phase 5: Verify & Commit

**Complexity**: Verification

---

## Pre-Commit Checklist

### 1. Sync Dependencies

```bash
uv sync --all-extras
```

### 2. Run Tests

```bash
uv run pytest -v
```

**Expected**: All tests pass

### 3. Verify CLI

```bash
uv run bids-hub --help
uv run bids-hub list
uv run bids-hub arc --help
uv run bids-hub arc info
uv run bids-hub isles24 --help
uv run bids-hub isles24 info
```

**Expected**: All commands work

### 4. Verify Imports

```bash
python -c "from bids_hub import build_and_push_arc, ValidationResult; print('OK')"
python -c "from bids_hub.cli import app; print('OK')"
python -c "from bids_hub.validation import validate_arc_download; print('OK')"
```

**Expected**: All imports succeed

### 5. Lint Check

```bash
uv run ruff check src/ tests/
uv run mypy src/
```

**Expected**: No errors (or acceptable warnings)

---

## Final Structure

```
neuroimaging-go-brrrr/
├── src/
│   └── bids_hub/           # 1,976 lines of production code
│       ├── __init__.py
│       ├── cli.py
│       ├── core/
│       ├── datasets/
│       └── validation/
├── tests/                  # 9 test files
├── scripts/
│   └── visualization/      # Tobias's notebooks (kept)
├── docs/
│   ├── brainstorming/      # Context (kept)
│   └── specs/              # These specs
├── pyproject.toml          # Updated with all deps + CLI
├── Makefile
└── README.md
```

---

## Commit

```bash
git add -A
git status

git commit -m "$(cat <<'EOF'
Integrate bids-hub production pipeline

- Add src/bids_hub/ (1,976 lines): complete BIDS→HF upload pipeline
- Add CLI: bids-hub arc/isles24 build/validate/info
- Add comprehensive test suite (9 files)
- Update pyproject.toml with all dependencies + datasets git pin
- Delete empty neuroimaging_go_brrrr skeleton
- Delete obsolete push_to_hub script
- Keep visualization notebooks (consumption pipeline)

The package name is `bids_hub` (accurate), hosted in
`neuroimaging-go-brrrr` repo (coordination hub).
EOF
)"
```

---

## Push

```bash
# Push to your fork
git push origin feature/bids-hub-integration

# Push to upstream (collaborators can see)
git push upstream feature/bids-hub-integration
```
