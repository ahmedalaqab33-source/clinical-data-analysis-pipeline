# Clinical Data Analysis Pipeline

[![CI](https://github.com/ahmedalaqab33-source/clinical-data-analysis-pipeline/actions/workflows/quality-checks.yml/badge.svg)](https://github.com/ahmedalaqab33-source/clinical-data-analysis-pipeline/actions/workflows/quality-checks.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--3586--3242-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0000-3586-3242)

A small, reproducible Python workflow for tabular clinical-research data quality checks and descriptive summaries. It is designed as a transparent starting point—not as a validated clinical decision system.

## Purpose

The workflow:

- reads a locally supplied CSV file;
- standardises column names and preserves all observations by default;
- checks that the dataset is non-empty and has unique column names;
- reports row, column, detected-duplicate, duplicate-removal, and missing-value counts;
- writes a descriptive summary and a machine-readable quality-control report.

No patient-level or restricted dataset is included.

## Repository structure

```text
main.py                         Pipeline entry point
documentation/methodology.md    Processing and validation scope
documentation/reproducibility_checklist.md
data/README.md                  Safe local data instructions
outputs/README.md               Generated-output description
tests/test_pipeline.py          Unit and smoke tests
```

## Quality assurance

Every push to `main` and every pull request is checked automatically with GitHub Actions. The quality workflow installs the development dependencies, runs Ruff static checks, and executes the pytest suite. The repository also includes contribution, security, citation, changelog, and reproducibility documentation.

## Requirements

- Python 3.10 or later
- Runtime packages in `requirements.txt`
- Quality-control packages in `requirements-dev.txt`

## Reproduce

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest
python main.py --data /path/to/local/input.csv --output-dir outputs
```

Alternatively, set `CLINICAL_DATA_PATH` instead of passing `--data`.

Exact duplicate rows are retained because repeated observations may be legitimate.
Use `--drop-exact-duplicates` only when the study protocol justifies removal.
The QC report records the selected policy, input row count, detected duplicates
(occurrences after the first identical row), and removals. The source CSV is never edited.
CSV headers are checked before parsing so duplicate names cannot be silently renamed.

## Expected outputs

- `descriptive_summary.csv`
- `quality_control.json`

Outputs may contain sensitive aggregates or labels. Review them before sharing.

## Data availability and privacy

This repository contains code and documentation only. Users must obtain and store data in accordance with ethics approvals, data-use agreements, institutional policy, and applicable law. Raw clinical, hospital, claims, EHR, or participant-level data must not be committed.

Security and responsible-disclosure guidance is provided in [SECURITY.md](SECURITY.md).

## Scope and limitations

This educational research workflow performs generic preprocessing and descriptive analysis. It does not select a study design, handle confounding or missingness, fit inferential models, validate clinical predictions, or establish causal or clinical conclusions. Adaptations require protocol-specific statistical review.

## Contributing

Scientific and technical contributions are welcome when they preserve privacy and transparent scope. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

See [CITATION.cff](CITATION.cff). No publication DOI is claimed for this repository.

## Author

**Ahmed Alaqab**  
PhD Candidate, University of Cyberjaya, Malaysia  
Clinical Pharmacy · Clinical Data Analysis · Digital Health · Health Informatics · Real-World Evidence · Responsible AI in Healthcare

[ORCID](https://orcid.org/0009-0000-3586-3242) · [Google Scholar](https://scholar.google.com/citations?user=swC2GY8AAAAJ) · [ResearchGate](https://www.researchgate.net/profile/Ahmed-Alaqab-2) · [LinkedIn](https://www.linkedin.com/in/ahmed-riyadh-alaqab-71377a25/) · [GitHub](https://github.com/ahmedalaqab33-source)

## License

Code and documentation are available under the [MIT License](LICENSE).
