# FloodWatch AI – Test Results

> Fill this file with **actual** results only. Do not write "Pass" for tests that were not run.

## 1. Test Environment
| Item | Value |
|---|---|
| Date of testing | |
| Python version | |
| OS | |
| Branch / commit | |
| Command used | `pytest tests/ -v` |

## 2. Automated Test Summary
| File | Tests run | Passed | Failed | Skipped |
|---|---|---|---|---|
| tests/test_model.py | | | | |
| tests/test_database.py | | | | |
| tests/test_routes.py | | | | |
| **Total** | | | | |

Paste the final pytest output below:
```
(paste real pytest output here)
```

## 3. Manual Integration Test Cases
| ID | Scenario | Steps | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| IT-01 | Open landing page | Visit `/` | Page loads with navigation | | |
| IT-02 | Open dashboard | Click Dashboard | Charts and status shown | | |
| IT-03 | Valid prediction | Enter valid values, submit | Risk category shown | | |
| IT-04 | Invalid input | Enter text in rainfall | Clear error message | | |
| IT-05 | Empty form | Submit blank | Validation message | | |
| IT-06 | Alert display | Make High Risk prediction | Alert appears with guidance | | |
| IT-07 | History | Open History | Previous predictions listed | | |
| IT-08 | Weather API down | Disable network / wrong key | App shows unavailable/sample label, no crash | | |
| IT-09 | Missing model file | Rename `flood_model.pkl` | Friendly error shown | | |
| IT-10 | Empty history | Fresh database | "No records" message | | |

## 4. Model Evaluation Results (from Member 1)
| Metric | Value |
|---|---|
| Accuracy | |
| Precision | |
| Recall (High Risk class) | |
| F1-score | |
Confusion matrix: *(paste or insert image)*

## 5. Bugs Found
| Bug ID | Description | Module / Owner | Severity | Status |
|---|---|---|---|---|
| | | | | |

## 6. Conclusion
*(Write after testing: what works, what failed, what remains.)*
