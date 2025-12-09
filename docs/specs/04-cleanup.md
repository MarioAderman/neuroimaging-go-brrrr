# Phase 4: Delete Obsolete Files

**Complexity**: Trivial (delete)

---

## Files to Delete

### 1. Empty Skeleton Package

```bash
rm -rf src/neuroimaging_go_brrrr/
```

**Why**: Empty `__init__.py`. The real package is now `src/bids_hub/`.

### 2. Broken Toy Script

```bash
rm scripts/push_to_hub_ds004884_full.py
```

**Why**: 42-line script that:
- Uses wrong API (`load_dataset("bids", ...)` doesn't exist)
- Has no validation
- Has no error handling
- Replaced by `bids-hub arc build`

### 3. One-liner Download Script

```bash
rm scripts/download_ds004884.sh
```

**Why**: Single `aws s3 sync` command. Not worth keeping.

---

## Files to KEEP

### Visualization Notebooks

```
scripts/visualization/
├── ArcAphasiaBids.ipynb
├── ArcAphasiaBidsLoadData.ipynb
└── data/.gitkeep
```

**Why**: Tobias's consumption pipeline demos. Different purpose than production pipeline.

### Brainstorming Docs

```
docs/brainstorming/consolidation-strategy.md
```

**Why**: Context document you wrote.

---

## Commands (All Deletes)

```bash
rm -rf src/neuroimaging_go_brrrr/
rm scripts/push_to_hub_ds004884_full.py
rm scripts/download_ds004884.sh
```

---

## Verification

```bash
# src/ should only have bids_hub
ls src/
# Expected: bids_hub

# scripts/ should only have visualization/
ls scripts/
# Expected: visualization
```
