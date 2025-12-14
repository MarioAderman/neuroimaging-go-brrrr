# Architecture

> **neuroimaging-go-brrrr** is the source-of-truth pipeline for publishing BIDS/NIfTI neuroimaging datasets (e.g. `hugging-science/*`) to the HuggingFace Hub using the standard `datasets` library.

---

## Positioning (Read This First)

- **Not a fork**: we do not maintain a fork/branch of `huggingface/datasets`.
- **Not blocked on upstream PRs**: we may upstream fixes, but this repo ships the production pipeline today (including workarounds + pinned deps when needed).
- **Produces standard Hub datasets**: output is a normal Hub dataset repo (Parquet shards + `dataset_info.json`).
- **Consumption uses standard tooling**: downstream users load published datasets with `datasets.load_dataset(...)` (+ `nibabel` to decode NIfTI).
- **Not affiliated with HuggingFace**: independent project built on their open-source ecosystem.

## Terminology (Avoid “datasets” Confusion)

- **`datasets` (library)**: the HuggingFace Python package (`pip install datasets`).
- **`huggingface/datasets` (repo)**: the upstream GitHub repository that publishes the `datasets` library.
- **Hub dataset repo**: a dataset on the Hub like `hugging-science/arc-aphasia-bids` (data + metadata), loaded via `datasets.load_dataset(...)`.
- **This repo**: a separate package (`bids_hub`, CLI `bids-hub`) that builds/uploads Hub dataset repos from local BIDS directories.

## Installation

**This package is NOT on PyPI**, so `pip install neuroimaging-go-brrrr` will not work. Install as a git dependency:

```bash
# Using uv (recommended)
uv add git+https://github.com/The-Obstacle-Is-The-Way/neuroimaging-go-brrrr.git

# Using pip
pip install git+https://github.com/The-Obstacle-Is-The-Way/neuroimaging-go-brrrr.git

# In pyproject.toml (for downstream projects)
[project]
dependencies = [
    "neuroimaging-go-brrrr @ git+https://github.com/The-Obstacle-Is-The-Way/neuroimaging-go-brrrr.git",
]
```

**Important (uploading/production):** reliable NIfTI embedding currently requires a git-pinned `datasets` build (see `pyproject.toml` `[tool.uv.sources]` and `docs/explanation/why-uploads-fail.md`).

---

## What This Project Is

```
+-----------------------------------------------------------------------------+
|                    THE HUGGINGFACE ECOSYSTEM FOR NEUROIMAGING               |
+-----------------------------------------------------------------------------+

    pip install datasets              uv add git+https://github.com/...
    -----------------------           ------------------------------------
    Standard HuggingFace              THIS PROJECT: Domain extension
    - Images, text, audio             - BIDS + NIfTI dataset pipelines
    - Parquet/Arrow storage           - BIDS directory structure
    - Hub integration                 - Neuroimaging validation
                                      - Upload utilities for BIDS->Hub

    +-------------------------+       +----------------------------------+
    |   huggingface/datasets  |       |   neuroimaging-go-brrrr          |
    |   (upstream library)    | <---- |   (bids_hub module)              |
    |                         |       |                                  |
    |   - Dataset             |       |   - Uses datasets.Nifti()        |
    |   - Features            |       |   - BIDS file discovery          |
    |   - Hub upload/download |       |   - Parquet sharding workarounds |
    +-------------------------+       +----------------------------------+
              ^                                      |
              |                                      |
              +--------------------------------------+
                     We EXTEND this, we don't fork it

+-----------------------------------------------------------------------------+
|  KEY INSIGHT: When you install this package, you get:                       |
|  - datasets (the standard HuggingFace library)                              |
|  - huggingface-hub (for Hub interactions)                                   |
|  - bids_hub module (our neuroimaging-specific extensions)                   |
|                                                                             |
|  We are NOT a fork or a branch of huggingface/datasets.                     |
|  We ship neuroimaging/BIDS production tooling on top of it.                 |
+-----------------------------------------------------------------------------+
```

---

## The Two Pipelines

This repo provides the **production** pipeline (uploading). The resulting Hub datasets are consumed with the standard `datasets` library.

### Pipeline 1: Production (Uploading to HuggingFace)

```
+---------------+     +----------------------+     +---------------------+
|  Local BIDS   |     |  bids_hub (this repo)|     |   HuggingFace Hub   |
|  Directory    | --> |                      | --> |   hugging-science/  |
|  (OpenNeuro)  |     |                      |     |   arc-aphasia-bids  |
+---------------+     |  - build_*_file_     |     +---------------------+
                      |    table()           |
                      |  - get_*_features()  |
                      |  - push_dataset_     |
                      |    to_hub()          |
                      +----------------------+

   Data Flow:
   1. Download BIDS dataset from OpenNeuro/Zenodo
   2. bids_hub scans directory, builds pandas DataFrame with paths + metadata
   3. Convert to HuggingFace Dataset with Nifti() feature types
   4. Upload sharded Parquet files to HuggingFace Hub
```

**CLI for production:**
```bash
uv run bids-hub arc build data/openneuro/ds004884 --no-dry-run
uv run bids-hub isles24 build data/zenodo/isles24/train --no-dry-run
```

### Pipeline 2: Consumption (Training from HuggingFace)

```
+---------------------+     +----------------------+     +-------------------+
|   HuggingFace Hub   |     |  load_dataset()      |     |  Your ML Code     |
|   hugging-science/  | --> |  (standard HF)       | --> |  - Training       |
|   arc-aphasia-bids  |     |                      |     |  - Inference      |
+---------------------+     +----------------------+     +-------------------+

   Data Flow:
   1. Consumer calls datasets.load_dataset("hugging-science/arc-aphasia-bids")
   2. HuggingFace downloads Parquet shards to local cache
   3. Nifti() columns automatically decode to nibabel objects
   4. Standard Dataset API (filter, map, batch) works normally
```

Note: consumption does not require installing this repo; `datasets` + `nibabel` is sufficient.

**Python for consumption:**
```python
from datasets import load_dataset

ds = load_dataset("hugging-science/arc-aphasia-bids", split="train")
example = ds[0]
print(example["subject_id"])  # "sub-M2001"
print(example["t1w"])         # nibabel.Nifti1Image object
```

---

## Dependency Relationship

Consumers can load published Hub datasets with just `datasets` + `nibabel`. Downstream projects can optionally depend on this repo for shared schemas, validation, and the `bids-hub` CLI.

```
+-----------------------------------------------------------------------------+
|                         PACKAGE DEPENDENCIES                                |
+-----------------------------------------------------------------------------+

  Minimal consumption (load from the Hub)
    pip install datasets nibabel
            |
            v
      +-----------------------------------+
      |   huggingface/datasets            |
      |   - load_dataset(...)             |
      |   - Nifti() decode (via nibabel)  |
      +-----------------------------------+

  Optional shared tooling (schemas/validation/CLI)
    uv add git+https://github.com/The-Obstacle-Is-The-Way/neuroimaging-go-brrrr.git
            |
            v
      +-----------------------------------+
      |   neuroimaging-go-brrrr           |
      |   (this repo)                     |
      |   - bids_hub module               |
      |   - CLI: bids-hub                 |
      +-----------------------------------+
            |
            v
      +-----------------------------------+
      |   huggingface/datasets            |
      |   - Dataset, Features, Nifti      |
      |   - Hub upload/download           |
      +-----------------------------------+
            |
            v
      +-----------------------------------+
      |   huggingface/huggingface_hub     |
      |   - HfApi                         |
      |   - upload_large_folder           |
      +-----------------------------------+
```

---

## Module Structure

```
src/bids_hub/
|-- __init__.py          # Public API re-exports
|-- cli.py               # Typer CLI (bids-hub command)
|-- core/                # Generic BIDS->HF utilities
|   |-- builder.py       # build_hf_dataset, push_dataset_to_hub
|   |-- config.py        # DatasetBuilderConfig dataclass
|   +-- utils.py         # File discovery helpers
|-- datasets/            # Per-dataset modules
|   |-- arc.py           # ARC schema, file discovery, pipeline
|   +-- isles24.py       # ISLES24 schema, file discovery, pipeline
+-- validation/          # Per-dataset validation
    |-- base.py          # ValidationResult, ValidationCheck framework
    |-- hf.py            # HuggingFace dataset validation helpers
    |-- arc.py           # ARC validation rules
    +-- isles24.py       # ISLES24 validation rules
```

### Layer Responsibilities

| Layer | Purpose | Key Functions |
|-------|---------|---------------|
| `core/` | Dataset-agnostic | `build_hf_dataset()`, `push_dataset_to_hub()` |
| `datasets/` | Dataset-specific schemas | `build_arc_file_table()`, `get_isles24_features()` |
| `validation/` | Data integrity checks | `validate_arc_download()`, expected counts |
| `cli.py` | User-facing commands | `bids-hub arc build`, `bids-hub isles24 validate` |

---

## Data Flow Detail

```
+-----------------------------------------------------------------------------+
|                              DATA FLOW                                      |
+-----------------------------------------------------------------------------+

   BIDS Dataset (Local)
         |
         |  build_*_file_table()
         |  - Scan BIDS directory structure
         |  - Extract metadata from sidecars
         |  - Return pandas DataFrame with absolute paths
         v
   +-----------------------------------+
   |  pandas DataFrame                 |
   |  - subject_id, session_id         |
   |  - t1w, t2w, flair (file paths)   |
   |  - metadata columns               |
   +-----------------------------------+
         |
         |  build_hf_dataset()
         |  - Convert DataFrame to Dataset
         |  - Cast columns to Features schema
         |  - Nifti() columns store file paths
         v
   +-----------------------------------+
   |  datasets.Dataset                 |
   |  - Nifti() feature types          |
   |  - Ready for embedding            |
   +-----------------------------------+
         |
         |  push_dataset_to_hub()
         |  - Shard dataset (often 1 per example)
         |  - Embed NIfTI bytes into Parquet
         |  - Upload via upload_large_folder()
         v
   +-----------------------------------+
   |  HuggingFace Hub                  |
   |  - Parquet shards with embedded   |
   |    NIfTI bytes                    |
   |  - Dataset card + metadata        |
   +-----------------------------------+
```

---

## Why We Exist

### The Problem

HuggingFace `datasets` natively supports images (JPEG, PNG), audio (WAV, MP3), and text.
It now includes an experimental `Nifti()` feature type, but it does not provide an end-to-end BIDS pipeline:

| Standard ML | Neuroimaging (BIDS) |
|-------------|---------------------|
| Images: JPEG, PNG | Images: NIfTI (.nii.gz) |
| Format: 2D arrays | Format: 3D/4D volumes + headers |
| Size: KB per image | Size: 50-200 MB per scan |
| Metadata: filename | Metadata: BIDS sidecar JSONs |
| Structure: flat folders | Structure: sub-*/ses-*/anat/ |

### The Solution

We build on top of HuggingFace `datasets` with:

1. **BIDS file discovery + schema**: map BIDS directories into `datasets.Features` using `datasets.Nifti()`
2. **Operational sharded uploads**: predictable memory usage + Hub upload reliability for hundreds of large files
3. **Validation framework**: pre-upload checks against expected counts and common corruption indicators

---

## Upstream Workarounds

We include workarounds for upstream bugs that affect neuroimaging use cases:

| Bug | Workaround | Location |
|-----|------------|----------|
| Sequence(Nifti()) crashes during shard | Pandas round-trip | `core/builder.py` |
| PyPI `datasets` embeds empty NIfTIs | Pin `datasets` to git | `pyproject.toml` |
| Upload timeout on large files | Extended timeout | `core/builder.py` |
| Rate limit on many shards | `upload_large_folder()` | `core/builder.py` |

See [docs/bugs/](docs/bugs/) for detailed documentation.

---

## Adding a New Dataset

1. **Create `datasets/newdataset.py`**:
   - Define `get_newdataset_features()` returning a Features schema
   - Define `build_newdataset_file_table()` returning a DataFrame
   - Define `build_and_push_newdataset()` orchestrating the pipeline

2. **Create `validation/newdataset.py`**:
   - Define expected counts from source publication
   - Define `validate_newdataset_download()` using base framework

3. **Update `cli.py`**:
   - Add new Typer subcommand group
   - Wire up `build`, `validate`, and `info` commands

4. **Update exports**:
   - Add to `datasets/__init__.py`
   - Add to `validation/__init__.py`
   - Add to root `__init__.py`

---

## Related Documentation

- [README.md](README.md) - Quick start guide
- [docs/explanation/architecture.md](docs/explanation/architecture.md) - Detailed design decisions
- [docs/reference/schema.md](docs/reference/schema.md) - Dataset schemas
- [docs/bugs/](docs/bugs/) - Known issues and workarounds
