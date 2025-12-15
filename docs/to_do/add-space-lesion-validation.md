# TODO: Add SPACE Lesion Session Validation

**Date:** 2025-12-15
**Priority:** Medium
**Complexity:** Low (30 min)

## Problem

The validation framework (`src/bids_hub/validation/hf.py`) has efficient PyArrow helpers but **no combined check** for SPACE lesion sessions (223), which is the key SSOT metric from the Gibson et al. paper.

Current validation checks individual counts:
- `lesion_non_null`: 228 ✅
- `t2w_sessions`: 440 ✅
- (no check for combined SPACE+lesion)

## Why This Matters

The 223 SPACE lesion count is the critical metric that exposed the v3 schema bug. Without automated validation, we would miss regressions.

## Proposed Solution

Add `check_space_lesion_sessions()` to `src/bids_hub/validation/hf.py` using efficient PyArrow operations:

```python
def check_space_lesion_sessions(
    ds: Dataset,
    expected: int = 223,
) -> HFValidationCheck:
    """Count sessions with SPACE T2w AND lesion mask.

    Uses PyArrow compute for O(n) on metadata only - no NIfTI decode.
    """
    table = ds.data.table

    # lesion is not null
    lesion_valid = pc.is_valid(table.column("lesion"))

    # len(t2w) > 0
    t2w_lengths = pc.fill_null(pc.list_value_length(table.column("t2w")), 0)
    t2w_has_data = pc.greater(t2w_lengths, 0)

    # t2w_acquisition in ('space_2x', 'space_no_accel')
    acq_col = table.column("t2w_acquisition")
    is_space = pc.is_in(acq_col, value_set=pa.array(["space_2x", "space_no_accel"]))

    # Combine: all three conditions
    combined = pc.and_(pc.and_(lesion_valid, t2w_has_data), is_space)
    count = pc.sum(pc.cast(combined, pa.int64())).as_py() or 0

    return HFValidationCheck(
        name="space_lesion_sessions",
        expected=str(expected),
        actual=str(count),
        passed=count == expected,
    )
```

Then add to `validate_arc_hf()`:

```python
result.add(check_space_lesion_sessions(ds, 223))
```

## Performance

- Current ad-hoc loop: ~10+ minutes (iterates and decodes NIfTI for each of 902 sessions)
- PyArrow approach: <1 second (operates on Arrow metadata only)

## Files to Modify

1. `src/bids_hub/validation/hf.py` - add generic helper
2. `src/bids_hub/validation/arc.py` - call in `validate_arc_hf()`
3. `tests/test_arc.py` - add test for new check
