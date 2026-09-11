from pathlib import Path

import pandas as pd
import pytest

from main import load_data, preprocess_data, quality_report, run


def test_preprocess_and_quality_report():
    frame = pd.DataFrame({" Patient ID ": [1, 1, 2], "Outcome (%)": [5, 5, None]})
    cleaned, removed = preprocess_data(frame)
    assert cleaned.columns.tolist() == ["patient_id", "outcome"]
    assert len(cleaned) == 2
    assert removed == 1
    assert quality_report(cleaned, removed)["missing_values_by_column"]["outcome"] == 1


def test_duplicate_standardised_columns_are_rejected():
    frame = pd.DataFrame([[1, 2]], columns=["Patient ID", "patient-id"])
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
