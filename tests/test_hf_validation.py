"""Tests for HuggingFace dataset validation helpers.

These tests intentionally use invalid NIfTI bytes to ensure the validation helpers
operate on Arrow data (no full decode) unless explicitly requested.
"""

from __future__ import annotations

from datasets import Dataset, Features, Nifti, Sequence, Value

from bids_hub.validation import (
    check_list_alignment,
    check_list_sessions,
    check_non_null_count,
    check_row_count,
    check_schema,
    check_total_list_items,
    check_unique_values,
)


def _mock_hf_dataset(*, misalign: bool = False) -> Dataset:
    features = Features(
        {
            "subject_id": Value("string"),
            "session_id": Value("string"),
            "img": Nifti(),
            "runs": Sequence(Nifti()),
            "runs_meta": Sequence(Value("string")),
        }
    )

    # NOTE: bytes are intentionally NOT valid NIfTI. The helpers should not decode them.
    runs_meta_third = ["m2", "m3"] if not misalign else ["m2"]

    data = {
        "subject_id": ["sub-1", "sub-2", "sub-3"],
        "session_id": ["ses-1", "ses-1", "ses-2"],
        "img": [
            {"path": "a.nii.gz", "bytes": b"not-a-nifti"},
            None,
            {"path": "c.nii.gz", "bytes": b"still-not-a-nifti"},
        ],
        "runs": [
            [{"path": "r1.nii.gz", "bytes": b"x"}],
            [],
            [
                {"path": "r2.nii.gz", "bytes": b"y"},
                {"path": "r3.nii.gz", "bytes": b"z"},
            ],
        ],
        "runs_meta": [["m1"], [], runs_meta_third],
    }

    return Dataset.from_dict(data, features=features)


def test_check_schema_pass_and_fail() -> None:
    ds = _mock_hf_dataset()

    ok = check_schema(ds, ["subject_id", "session_id", "img", "runs", "runs_meta"])
    assert ok.passed is True

    missing = check_schema(ds, ["subject_id", "session_id", "img", "unknown_column"])
    assert missing.passed is False
    assert "Missing:" in missing.details

    extra = check_schema(ds, ["subject_id", "img"])
    assert extra.passed is False
    assert "Extra:" in extra.details


def test_check_row_count() -> None:
    ds = _mock_hf_dataset()
    check = check_row_count(ds, expected=3)
    assert check.passed is True


def test_check_unique_values() -> None:
    ds = _mock_hf_dataset()
    check = check_unique_values(ds, "subject_id", expected=3)
    assert check.passed is True


def test_check_non_null_count_on_nifti_column_does_not_decode() -> None:
    ds = _mock_hf_dataset()
    check = check_non_null_count(ds, "img", expected=2)
    assert check.passed is True


def test_check_list_sessions_and_total_items_on_nifti_lists() -> None:
    ds = _mock_hf_dataset()

    sessions = check_list_sessions(ds, "runs", expected=2)
    assert sessions.passed is True

    total = check_total_list_items(ds, "runs", expected=3)
    assert total.passed is True


def test_check_list_alignment_includes_row_ids_on_failure() -> None:
    ds = _mock_hf_dataset(misalign=True)

    check = check_list_alignment(
        ds,
        ["runs", "runs_meta"],
        row_id_columns=["subject_id", "session_id"],
    )
    assert check.passed is False
    assert "subject_id=sub-3" in check.details
    assert "session_id=ses-2" in check.details
