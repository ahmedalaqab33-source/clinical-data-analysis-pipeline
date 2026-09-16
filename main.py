"""Reproducible descriptive workflow for locally supplied tabular research data."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
from pathlib import Path

import pandas as pd

LOGGER = logging.getLogger(__name__)
DEFAULT_OUTPUT_DIR = Path("outputs")


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=os.getenv("CLINICAL_DATA_PATH"),
        help="Path to a local CSV file; alternatively set CLINICAL_DATA_PATH.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--drop-exact-duplicates",
        action="store_true",
        help="Remove exact duplicate rows only when justified by the study protocol.",
    )
    return parser.parse_args()


def load_data(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found or not a file: {path}")
    # Validate before pandas can rename repeated CSV headers (e.g. age -> age.1).
    with path.open(encoding="utf-8-sig", newline="") as stream:
        header = next(csv.reader(stream), [])
    if not header:
        raise ValueError("The input dataset contains no column headers.")
    standardise_column_names(pd.Index(header))
    frame = pd.read_csv(path)
    if frame.empty:
        raise ValueError("The input dataset contains no data rows.")
    return frame


def standardise_column_names(columns: pd.Index) -> list[str]:
    cleaned = (
        columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
        .str.strip("_")
        .tolist()
    )
    if any(not name for name in cleaned):
        raise ValueError("At least one column name is empty after standardisation.")
    if len(cleaned) != len(set(cleaned)):
        raise ValueError("Column-name standardisation produced duplicate names.")
    return cleaned


def preprocess_data(
    frame: pd.DataFrame,
    *,
    drop_exact_duplicates: bool = False,
) -> tuple[pd.DataFrame, int]:
    cleaned = frame.copy()
    cleaned.columns = standardise_column_names(cleaned.columns)
    before = len(cleaned)
    if drop_exact_duplicates:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    return cleaned, before - len(cleaned)


def describe_data(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.describe(include="all").transpose()


def quality_report(frame: pd.DataFrame, duplicates_removed: int) -> dict[str, object]:
    return {
        "rows_after_preprocessing": int(len(frame)),
        "columns": int(frame.shape[1]),
        "duplicates_removed": int(duplicates_removed),
        "missing_values_by_column": {key: int(value) for key, value in frame.isna().sum().items()},
    }


def save_results(
    summary: pd.DataFrame,
    report: dict[str, object],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_dir / "descriptive_summary.csv")
    (output_dir / "quality_control.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(data_path: Path, output_dir: Path, *, drop_exact_duplicates: bool = False) -> None:
    frame = load_data(data_path)
    cleaned, duplicates_removed = preprocess_data(
        frame, drop_exact_duplicates=drop_exact_duplicates
    )
    report = quality_report(cleaned, duplicates_removed)
    report.update(
        {
            "rows_before_preprocessing": int(len(frame)),
            "exact_duplicate_rows_detected": int(frame.duplicated().sum()),
            "duplicate_policy": "drop_exact" if drop_exact_duplicates else "preserve",
        }
    )
    save_results(describe_data(cleaned), report, output_dir)


def main() -> None:
    configure_logging()
    args = parse_args()
    if args.data is None:
        raise SystemExit("Provide --data PATH or set CLINICAL_DATA_PATH.")
    LOGGER.info("Starting analysis with local input: %s", args.data)
    run(Path(args.data), args.output_dir, drop_exact_duplicates=args.drop_exact_duplicates)
    LOGGER.info("Pipeline completed; outputs written to %s", args.output_dir)


if __name__ == "__main__":
    main()
