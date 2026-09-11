# Local data directory

Place an authorised local CSV input here only if permitted by the applicable ethics approval and data-use agreement. Files in this directory are ignored by Git.

Do not commit raw clinical, hospital, EHR, claims, or participant-level data. The pipeline accepts any local path:

```bash
python main.py --data /secure/location/input.csv
```

Before analysis, create a protocol-specific data dictionary and confirm variable definitions, permissible values, missing-value codes, identifiers, and expected sample size.
