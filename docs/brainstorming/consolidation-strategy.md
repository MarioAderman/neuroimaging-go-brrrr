# Project Roadmap & Architecture

> **Status**: Active
> **Last Updated**: 2024-12-08

## Vision

**Generic BIDS/NIfTI infrastructure** for HuggingFace, battle-tested against real research datasets (ARC, ISLES24).

## What We Have

### Production Pipeline (bids-hub)

```text
BIDS Dataset (Local)
        │
        ▼ build_*_file_table()
pandas DataFrame (paths + metadata)
        │
        ▼ build_hf_dataset()
datasets.Dataset with Nifti() features
        │
        ▼ push_dataset_to_hub(num_shards=N)
HuggingFace Hub (Parquet shards)
```

### Module Structure

```text
src/bids_hub/
├── core/           # Generic BIDS→HF utilities
├── datasets/       # Per-dataset schemas (ARC, ISLES24)
├── validation/     # Pre-upload data integrity checks
└── cli.py          # Typer CLI (bids-hub command)
```

## Live Resources

| Resource | Description | Link |
|----------|-------------|------|
| arc-aphasia-bids | ARC dataset (293 GB, 902 sessions) | [HF Hub](https://huggingface.co/datasets/hugging-science/arc-aphasia-bids) |
| isles24-stroke | ISLES24 dataset (~100 GB, 149 subjects) | [HF Hub](https://huggingface.co/datasets/hugging-science/isles24-stroke) |

## Roadmap

| Priority | Task | Status |
|----------|------|--------|
| 1 | Monitor upstream `datasets` PR #7896 | Tracking |
| 2 | Add ATLAS v2.0 dataset support | Planned |
| 3 | Improve CLI test coverage (60% → 80%) | Planned |

## Data Governance

All datasets require proper citation per their respective licenses:

| Dataset | Citation |
|---------|----------|
| ARC (ds004884) | [Gibson et al., Scientific Data 2024](https://doi.org/10.1038/s41597-024-03819-7) |
| ISLES 2024 | [ISLES Organizers, 2024](https://isles-24.grand-challenge.org/) |

## References

- [OpenNeuro ds004884](https://openneuro.org/datasets/ds004884) - Aphasia Recovery Cohort
- [ISLES 2024 Challenge](https://isles-24.grand-challenge.org/) - Stroke lesion segmentation
- [BIDS Specification](https://bids-specification.readthedocs.io/) - Brain Imaging Data Structure
- [HuggingFace Datasets](https://huggingface.co/docs/datasets/) - Dataset library documentation
