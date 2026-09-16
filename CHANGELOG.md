# Changelog

All notable changes to this repository are documented here.

## Unreleased

- Preserve identical observations by default; require `--drop-exact-duplicates` for removal.
- Record input counts, detected duplicates, removals, and the selected policy in QC output.
- Reject ambiguous CSV headers before pandas can rename them.
- Add regression tests for duplicate policies and malformed headers.

## [0.1.0] - 2026-09-11

### Added

- configurable local CSV input and output directory;
- input validation and machine-readable quality-control reporting;
- unit and end-to-end smoke tests;
- automated lint and test checks;
- data-governance, methodology, citation, contribution, and reproducibility documentation.

### Changed

- clarified that the workflow is descriptive and is not a validated clinical decision system;
- strengthened ignore rules for research data, credentials, and generated outputs;
- adopted the unified academic name Ahmed Alaqab in repository metadata.
