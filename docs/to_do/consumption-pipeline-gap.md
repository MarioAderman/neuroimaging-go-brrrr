# Consumption Pipeline Gap Analysis

## Date: 2025-12-14

## Summary

This repo is **production-only**. We are missing consumption features that exist in pending upstream PRs.

## What This Repo Has

### Production Pipeline (Complete)
- `build_arc_file_table()` - scan BIDS directories
- `build_hf_dataset()` - convert DataFrame to HF Dataset with `Nifti()` features
- `push_dataset_to_hub()` - sharded upload with `upload_large_folder()`
- CLI: `bids-hub arc build`, `bids-hub isles24 build`

### Consumption (Minimal)
- `validate_arc_from_hub()` in `validation/arc.py:367` - calls `load_dataset(repo_id)` for validation
- That's it. No BIDS loader, no special consumption APIs.

## What's In Upstream `huggingface/datasets`

### Tobias's Merged Work
- `Nifti()` feature type - enables NIfTI columns in datasets
- Decoding: auto-converts to `nibabel.Nifti1Image` on access
- Visualization: niivue viewer on Hub

### Your Pending PRs (NOT MERGED)

| PR | Description | Status | Type |
|----|-------------|--------|------|
| [#7886](https://github.com/huggingface/datasets/pull/7886) | BIDS loader - `load_dataset('bids', data_dir='/path')` | OPEN | **LOCAL CONSUMPTION** |
| [#7887](https://github.com/huggingface/datasets/pull/7887) | Lazy loading for NIfTI (memory fix) | OPEN | **CONSUMPTION FIX** |
| [#7896](https://github.com/huggingface/datasets/pull/7896) | Fix Sequence(Nifti()) embedding crash | OPEN | **PRODUCTION FIX** |

## The Gap

Tobias merged `Nifti()` support, but:
1. **No BIDS loader** - can't do `load_dataset('bids', data_dir='/local/bids')` without PR #7886
2. **Memory issues** - NIfTI files load eagerly into RAM without PR #7887
3. **Embedding crashes** - Sequence(Nifti()) fails without PR #7896 (we have workaround)

## Current State

```
CONSUMPTION OPTIONS TODAY:

1. FROM HUB (works):
   load_dataset("hugging-science/arc-aphasia-bids")
   → Uses Tobias's Nifti() decode
   → No special tooling needed

2. FROM LOCAL BIDS (NOT POSSIBLE without upstream merge):
   load_dataset('bids', data_dir='/path/to/bids')  # PR #7886 not merged
   → Requires your pending PR
```

## Recommendation

### Option A: Wait for Upstream (Status Quo)
- Keep this repo production-only
- Wait for Tobias/maintainers to merge PRs #7886, #7887
- Document in ARCHITECTURE.md that local BIDS consumption is pending upstream

### Option B: Vendor PRs Here
- Copy BIDS loader code from PR #7886 into `src/bids_hub/loader/`
- Copy lazy loading fix from PR #7887
- Make this repo a complete solution independent of slow upstream

### Option C: Create GitHub Issues
- File issues on this repo documenting the dependency on upstream PRs
- Track upstream merge progress
- Plan to integrate once merged

## Questions to Resolve

1. Do we want to vendor the BIDS loader here to be self-sufficient?
2. Should ARCHITECTURE.md mention the pending upstream work?
3. Should we create tracking issues linking to upstream PRs?

## References

- Upstream datasets repo: https://github.com/huggingface/datasets
- PR #7886 (BIDS loader): https://github.com/huggingface/datasets/pull/7886
- PR #7887 (lazy loading): https://github.com/huggingface/datasets/pull/7887
- PR #7896 (embedding fix): https://github.com/huggingface/datasets/pull/7896
