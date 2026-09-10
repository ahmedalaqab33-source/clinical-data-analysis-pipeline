from pathlib import Path
import logging

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample" / "clinical_sample.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


def configure_logging():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def load_data(path):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def preprocess_data(df):
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    df = df.drop_duplicates()
    return df


def run_analysis(df):
    summary = df.describe(include="all").transpose()
    return summary


def save_results(summary):
    output_file = OUTPUT_DIR / "descriptive_summary.csv"
    summary.to_csv(output_file)
    logging.info(f"Results saved to {output_file}")


def main():
    configure_logging()
    logging.info("Starting clinical data analysis pipeline")

    df = load_data(DATA_PATH)
    df = preprocess_data(df)
    summary = run_analysis(df)
    save_results(summary)

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
  
