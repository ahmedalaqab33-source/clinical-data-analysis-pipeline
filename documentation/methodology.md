# Methodology and validation scope

## Processing

The pipeline reads a CSV file with pandas, standardises column names, rejects ambiguous duplicate names, removes exact duplicate rows, and produces descriptive statistics.

## Quality controls

It verifies that:

- the supplied path points to a file;
- the input has at least one data row;
- standardised column names are non-empty and unique;
- duplicate removal and missing-value counts are recorded;
- expected output files can be generated.

## Interpretation limits

These checks do not validate clinical plausibility, study eligibility, exposure or outcome definitions, missing-data mechanisms, model assumptions, confounding control, multiplicity, causal identification, or external validity. Those elements must be specified in an approved protocol and analysis plan.

## Data governance

No dataset is distributed. Analyses must use de-identified, authorised data stored outside version control. Outputs require disclosure review before release.
