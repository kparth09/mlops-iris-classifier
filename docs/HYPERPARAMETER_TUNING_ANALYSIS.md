# Hyperparameter Tuning Analysis (Experiment 7)

Baseline model development, Grid Search vs Random Search tuning, and
comparative performance analysis on the Experiment 4 feature set
(`data/processed/iris_features.csv`, 150 rows, 7 features + `species` target).

**All numbers below are the actual measured output of running the scripts in
this repository** with Python 3.11.9 / scikit-learn 1.9.1 / MLflow 2.17.2,
`random_state=42` throughout.

## 0. Environment

| Component | Version |
|---|---|
| Python | 3.11.9 (`.venv-mlflow`) |
| scikit-learn | 1.9.1 |
| NumPy | 2.4.6 |
| SciPy | 1.17.1 |
| pandas | 2.3.3 |
| MLflow | 2.17.2 |

All scripts log to the MLflow experiment **`iris-hyperparameter-tuning`**
(backend `sqlite:///mlflow.db`).

---

## 1. Baseline Model

- **Model:** `DecisionTreeClassifier` (all default hyperparameters, `random_state=42`)
- **Search:** none — deliberately naive, this is the reference point

| Metric | Value |
|---|---|
| CV F1 Macro (5-fold, on train) | **0.9663** (+/- 0.0316) |
| Test Accuracy (held-out 20%) | **0.9000** |

```text
Baseline CV f1_macro: 0.9663 (+/- 0.0316)
Baseline test accuracy: 0.9000
```

The wide gap between the CV score (0.9663) and the test score (0.9000) is the
first useful signal this experiment produces: the default Decision Tree is
high-variance. It fits the training folds very well but does not transfer as
well to genuinely unseen data.

---

## 2. Grid Search

- **Model:** `RandomForestClassifier`
- **Search:** `GridSearchCV`, exhaustive, scoring = `f1_macro`, 5-fold CV

### Grid examined

| Hyperparameter | Values | Count |
|---|---|---|
| `n_estimators` | 50, 100, 200 | 3 |
| `max_depth` | 3, 5, 10, None | 4 |
| `min_samples_split` | 2, 5, 10 | 3 |
| `max_features` | sqrt, log2 | 2 |

**Total combinations: 3 x 4 x 3 x 2 = 72**
**Total model fits: 72 x 5 = 360**

### Result

| Metric | Value |
|---|---|
| Best CV F1 Macro | **0.9663** |
| Test Accuracy | **0.9667** |
| Best params | `max_depth=3`, `max_features=sqrt`, `min_samples_split=2`, `n_estimators=50` |

```text
Grid Search evaluated 72 combinations x 5 folds = 360 total fits
Best params: {'max_depth': 3, 'max_features': 'sqrt',
              'min_samples_split': 2, 'n_estimators': 50}
Best CV f1_macro: 0.9663
Test accuracy: 0.9667
```

Every one of the 72 candidates (params, mean/std CV score, rank) is logged to
the `grid_search_all_candidates.csv` artifact.

---

## 3. Random Search

- **Model:** `RandomForestClassifier`
- **Search:** `RandomizedSearchCV`, scoring = `f1_macro`, 5-fold CV, `random_state=42`
- **Distributions:** `n_estimators ~ randint(50, 300)`,
  `min_samples_split ~ randint(2, 15)`, `max_depth in [3,5,10,15,None]`,
  `max_features in [sqrt, log2]`

**Iterations: 30** -> **Total model fits: 30 x 5 = 150**

### Result

| Metric | Value |
|---|---|
| Best CV F1 Macro | **0.9663** |
| Test Accuracy | **0.9667** |
| Best params | `max_depth=3`, `max_features=sqrt`, `min_samples_split=6`, `n_estimators=100` |

```text
Random Search evaluated 30 combinations x 5 folds = 150 total fits
Best params: {'max_depth': 3, 'max_features': 'sqrt',
              'min_samples_split': 6, 'n_estimators': 100}
Best CV f1_macro: 0.9663
Test accuracy: 0.9667
```

All 30 sampled candidates are logged to `random_search_all_candidates.csv`.

---

## 4. Comparison

Output of `python src/compare_tuning_results.py`:

```text
Run Name                      CV f1_macro    Test Accuracy  Total Fits
------------------------------------------------------------------------
baseline_decision_tree        0.9663         0.9000         5
grid_search_random_forest     0.9663         0.9667         360
random_search_random_forest   0.9663         0.9667         150
```

| Model | CV F1 Macro | Test Accuracy | Total Fits |
|---|---|---|---|
| Baseline Decision Tree | 0.9663 | 0.9000 | 5 |
| Grid Search Random Forest | 0.9663 | **0.9667** | 360 |
| Random Search Random Forest | 0.9663 | **0.9667** | 150 |

### Key findings

**1. Both tuned models beat the baseline on the held-out test set.**
Test accuracy improves from **0.9000 -> 0.9667 (+6.67 percentage points)**,
with no change in CV score. The tuning effort bought real generalisation
improvement, exactly the kind of finding the baseline exists to reveal.

**2. Random Search matched Grid Search at 41.7% of the cost.**
Random Search reached the *identical* best CV score (0.9663) and the identical
test accuracy (0.9667) using **150 fits instead of 360** — a **58.3% reduction
in compute** for zero loss in performance.

**3. Why Random Search wins here — the hyperparameter sensitivity data.**
Grouping the 72 grid candidates by each hyperparameter value (mean CV F1 Macro):

| `n_estimators` | mean CV | | `max_depth` | mean CV |
|---|---|---|---|---|
| 50 | 0.9642 | | 3 | 0.9635 |
| 100 | 0.9622 | | 5 | 0.9608 |
| 200 | 0.9580 | | 10 | 0.9608 |

| `min_samples_split` | mean CV | | `max_features` | mean CV |
|---|---|---|---|---|
| 2 | 0.9635 | | sqrt | 0.9615 |
| 5 | 0.9594 | | log2 | 0.9615 |
| 10 | 0.9615 | | | |

The total score spread across all 72 candidates is only **0.0084**
(best 0.9663, worst 0.9580). On this small, clean Iris dataset **no single
hyperparameter matters very much** — every dimension moves the mean score by
less than ~0.006. This is exactly the scenario Bergstra & Bengio (2012)
describe: Grid Search spends its budget exhaustively re-sampling unimportant
dimensions, whereas Random Search's independent per-dimension sampling lands
on the good region almost immediately. Grid Search had to burn 360 fits to
confirm what Random Search found in 150.

**4. An honest caveat — the CV score is saturated.**
The baseline, Grid Search and Random Search all report the *same* CV F1 Macro
of 0.9663. On 120 training rows with 5-fold CV, the maximum attainable F1 is
already reached by a default Decision Tree, so the search had no headroom to
demonstrate a CV improvement on. The real, measurable benefit of tuning here
shows up only on the held-out test set (0.9000 -> 0.9667), not in the CV
number. A stronger conclusion would need a larger dataset or a harder task
where CV score is not already at ceiling.

**5. Selection margin.**
30 of 72 grid candidates and 1 of 30 random candidates land within 0.005 of the
best score. The optimum is a broad plateau, not a sharp peak — another reason
a large random sample finds it easily, and also a warning that picking "the
single best configuration" on this dataset is somewhat arbitrary among ties.

---

## 5. Methodology Note — avoiding test-set contamination

Both searches select hyperparameters using **5-fold cross-validation on the
training split only**. The held-out 20% test set is touched **exactly once**,
after the configuration was already chosen, purely to report a final unbiased
`test_accuracy`. Had the searches instead selected on the test set and then
reported that same number, the reported accuracy would be optimistically
biased — a form of data leakage, since the search maximises over many
candidates and would overfit the quirks of that one 30-row sample.

---

## 6. How to Reproduce

```bash
source .venv-mlflow/Scripts/activate
python src/baseline_model.py
python src/grid_search_tuning.py
python src/random_search_tuning.py
python src/compare_tuning_results.py
```

Then launch the UI to inspect all 3 runs and download the candidate CSVs:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

---

## 7. Practical Takeaways

1. **Always build a baseline first.** It is the only way to know whether an
   expensive search was worth running — here it revealed a 6.67-point test
   accuracy gain that the CV score alone completely hid.
2. **Random Search is the better default** when the space is large or mostly
   unimportant: 150 fits beat 360 fits here, at equal performance.
3. **Grid Search is still justified** when the space is small and cheap, or
   when a deterministic, exhaustive, auditable enumeration is required (e.g.
   regulatory sign-off).
4. **Track every trial in MLflow, not just the winner.** The per-candidate
   CSVs are what made the sensitivity table in Finding 3 possible at all.
5. **A CV score at ceiling is a warning sign.** When baseline and tuned models
   score identically in cross-validation, the benchmark is saturated and
   cannot discriminate between models — evaluate on genuinely unseen data.