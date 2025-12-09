# Phase 1: Copy Source Code

**Complexity**: Trivial (file copy)

---

## Commands

```bash
# Copy the complete bids_hub package
cp -r _reference_repos/bids-hub/src/bids_hub src/

# Verify structure
tree src/bids_hub/
```

## Expected Result

```
src/bids_hub/
├── __init__.py          # Package exports
├── cli.py               # Typer CLI (289 lines)
├── core/
│   ├── __init__.py
│   ├── builder.py       # build_hf_dataset, push_dataset_to_hub
│   ├── config.py        # DatasetBuilderConfig
│   └── utils.py         # find_single_nifti, find_all_niftis
├── datasets/
│   ├── __init__.py
│   ├── arc.py           # ARC schema + pipeline
│   └── isles24.py       # ISLES24 schema + pipeline
└── validation/
    ├── __init__.py
    ├── base.py          # ValidationResult, generic checks
    ├── arc.py           # ARC-specific validation
    └── isles24.py       # ISLES24-specific validation
```

## Verification

```bash
# Count lines (should be ~1,976)
find src/bids_hub -name "*.py" | xargs wc -l | tail -1
```

---

## What NOT to Do

- DO NOT rename `bids_hub` to `neuroimaging_go_brrrr`
- DO NOT modify any files during copy
- DO NOT copy the `.git` directory (it's already removed)
