# src/compare_tuning_results.py

"""
Pulls all three tracked runs (baseline, grid search, random search)
from MLflow and prints a consolidated comparison table.

This script does NOT train another model. It only talks to the
MLflow tracking store via the MlflowClient API.
"""

import mlflow

from mlflow.tracking import MlflowClient


mlflow.set_tracking_uri("sqlite:///mlflow.db")

client = MlflowClient()

experiment = client.get_experiment_by_name(
    "iris-hyperparameter-tuning"
)

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id]
)

runs = sorted(
    runs,
    key=lambda r: r.data.tags.get("mlflow.runName", ""),
)

print(
    f"{'Run Name':<30}"
    f"{'CV f1_macro':<15}"
    f"{'Test Accuracy':<15}"
    f"{'Total Fits':<12}"
)

print("-" * 72)

for run in runs:

    name = run.data.tags.get(
        "mlflow.runName", "unknown"
    )

    cv_score = run.data.metrics.get(
        "cv_f1_macro_mean",
        run.data.metrics.get("best_cv_f1_macro", 0),
    )

    test_acc = run.data.metrics.get("test_accuracy", 0)

    n_iter = (
        run.data.params.get("total_combinations")
        or run.data.params.get("n_iter")
        or "1"
    )

    total_fits = (
        int(n_iter) * 5
        if name != "baseline_decision_tree"
        else 5
    )

    print(
        f"{name:<30}"
        f"{cv_score:<15.4f}"
        f"{test_acc:<15.4f}"
        f"{total_fits:<12}"
    )