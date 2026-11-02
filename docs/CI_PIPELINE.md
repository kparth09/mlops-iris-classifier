# Continuous Integration Pipeline

## Purpose

The CI pipeline automatically checks Python code and tests changes to the
MLOps Iris Classifier. It runs for pushes and pull requests targeting `main`
or `develop`.

The workflow is defined in `.github/workflows/ci.yml` and runs on
`ubuntu-latest` with Python 3.11.

## Workflow jobs

### `build-and-lint`

This job installs the project requirements and the CI tools, compiles the
Python files with `python -m compileall -q src tests`, and runs Flake8 on
`src/`. The workflow sets Flake8's maximum line length to 100 and ignores
`E203`.

### `test-suite`

This job runs after `build-and-lint` succeeds. It collects Iris data,
preprocesses it, and engineers features before running the complete pytest
suite with coverage enabled. Pytest writes:

- `test-results.xml` in JUnit XML format.
- `coverage.xml` in XML coverage format.

The job uploads both reports as the `test-and-coverage-reports` GitHub Actions
artifact. The upload step uses `if: always()`, so it runs even when the tests
fail; missing report files produce a warning.

### `model-quality-gate`

This job runs after `test-suite` succeeds. It prepares the Iris data using the
same collection, preprocessing, and feature-engineering stages, then runs
`tests/test_model_quality.py`. The test checks that predictions are valid and
that accuracy meets `MIN_ACCEPTABLE_ACCURACY`.

Because this job declares `needs: test-suite`, GitHub Actions skips it when
`test-suite` fails.

## Pull-request verification

The baseline restoration was merged through
[PR #8](https://github.com/kparth09/mlops-iris-classifier/pull/8). Its
`build-and-lint`, `test-suite`, and `model-quality-gate` checks all succeeded.

For the regression demonstration, the minimum accuracy threshold was
temporarily raised from `0.90` to `0.999`. The model achieved approximately
`0.9667` accuracy, so the model-quality assertion failed because that value
was below `0.999`. In [PR #9](https://github.com/kparth09/mlops-iris-classifier/pull/9),
`build-and-lint` passed, `test-suite` failed on the raised threshold, and
`model-quality-gate` was skipped because it depends on the failed
`test-suite` job. PR #9 was closed without merging.

After capturing the regression result, the threshold was restored to `0.90`.
The restored baseline passed the focused model-quality test and all 13 tests
locally.

## Main branch protection

The `main` branch is configured to require these status checks before a pull
request can be merged:

- `build-and-lint`
- `test-suite`
- `model-quality-gate`

The regression demonstration shows how a failing test prevents the dependent
model-quality check from running and prevents the required checks from all
passing.
