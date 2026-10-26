# Testing Strategy — Experiment 8

## 1. Objective

The objective is to test the MLOps pipeline using automated tests for data processing, feature engineering, validation, model training, and model output quality.

## 2. Test Files

| Test file | Layer | Purpose |
|---|---|---|
| `tests/test_preprocess.py` | Data | Tests duplicate removal, missing values, missing target labels, and empty data |
| `tests/test_features.py` | Data | Tests feature calculations, petal length categories, and zero-division handling |
| `tests/test_validate.py` | Data | Tests valid data, missing columns, invalid species, and out-of-range values |
| `tests/test_training_pipeline.py` | Pipeline | Checks that model training completes and predictions have the expected shape |
| `tests/test_model_quality.py` | Model quality | Checks prediction labels and model accuracy |

## 3. Testing Tools

- **pytest:** Runs automated tests.
- **pytest-cov:** Measures code coverage.
- **JUnit XML:** Stores test results in a format suitable for CI tools.

## 4. Execution Commands

Run all tests:

`pytest -v`

Run tests with coverage and generate a JUnit XML report:

`pytest --cov=src --cov-report=term-missing --junitxml=test-results.xml`

## 5. Coverage Results

Record the actual total coverage percentage reported by pytest in `test-results.xml` generation run.

- Total tests: Record the actual number of tests passed.
- Tests passed: Record the final pytest result.
- Overall source coverage: Record the actual percentage.
- Data-processing coverage: Record the percentages for `preprocess.py`, `features.py`, and `validate.py`.

## 6. Conclusion

Automated testing helps detect data-processing errors, pipeline failures, invalid predictions, and reductions in model quality. The test suite provides a foundation for integrating automated quality checks into CI/CD.
