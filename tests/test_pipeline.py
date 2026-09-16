import json
from pathlib import Path

import pandas as pd
import pytest

from main import load_data, preprocess_data, quality_report, run


def test_preprocess_and_quality_report():
    frame = pd.DataFrame({" Patient ID ": [1, 1, 2], "Outcome (%)": [5, 5, None]})
    cleaned, removed = preprocess_data(frame, drop_exact_duplicates=True)
    assert cleaned.columns.tolist() == ["patient_id", "outcome"]
    assert len(cleaned) == 2
    assert removed == 1
    assert quality_report(cleaned, removed)["missing_values_by_column"]["outcome"] == 1


def test_duplicate_standardised_columns_are_rejected():
    frame = pd.DataFrame([[1, 2]], columns=["Patient ID", "patient_id"])
    with pytest.raises(ValueError, match="duplicate"):
        preprocess_data(frame)


def test_empty_input_is_rejected(tmp_path: Path):
    source = tmp_path / "empty.csv"
    source.write_text("a,b\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no data rows"):
        load_data(source)


def test_smoke_run_writes_expected_outputs(tmp_path: Path):
    source = tmp_path / "input.csv"
    pd.DataFrame({"age": [30, 40], "outcome": [0, 1]}).to_csv(source, index=False)
    output = tmp_path / "outputs"
    run(source, output)
    assert (output / "descriptive_summary.csv").is_file()
    assert (output / "quality_control.json").is_file()


@pytest.mark.parametrize("drop,expected_rows,removed", [(False, 3, 0), (True, 2, 1)])
def test_duplicate_policy_preserves_observations_by_default(tmp_path, drop, expected_rows, removed):
    source = tmp_path / "repeated.csv"
    source.write_text("age,outcome\n30,1\n30,1\n40,0\n", encoding="utf-8")
    original = source.read_bytes()
    output = tmp_path / "outputs"
    run(source, output, drop_exact_duplicates=drop)
    report = json.loads((output / "quality_control.json").read_text())
    assert report["rows_before_preprocessing"] == 3
    assert report["rows_after_preprocessing"] == expected_rows
    assert report["exact_duplicate_rows_detected"] == 1
    assert report["duplicates_removed"] == removed
    assert report["duplicate_policy"] == ("drop_exact" if drop else "preserve")
    assert source.read_bytes() == original


@pytest.mark.parametrize("header", ["age,age", "Age, age ", "age,!!!"])
def test_invalid_csv_headers_are_rejected_before_pandas_renames_them(tmp_path, header):
    source = tmp_path / "bad.csv"
    source.write_text(header + "\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate|empty"):
        load_data(source)
