"""
End-to-end Feast workflow for the Iris feature repository.

Applies the feature definitions, then exercises historical retrieval,
online retrieval and Feature Service retrieval against the
`iris_measurements` and `iris_engineered_features` feature views.

Run from this directory (the Feast repo root):

    python prepare_feature_source.py
    python test_workflow.py
"""

import subprocess
import sys
from datetime import datetime

import pandas as pd

from feast import FeatureStore

# Feature lists must match the views declared in features.py.
MEASUREMENT_FEATURES = [
    "iris_measurements:sepal length (cm)",
    "iris_measurements:sepal width (cm)",
    "iris_measurements:petal length (cm)",
    "iris_measurements:petal width (cm)",
]

ENGINEERED_FEATURES = [
    "iris_engineered_features:sepal_area",
    "iris_engineered_features:petal_area",
    "iris_engineered_features:sepal_to_petal_length_ratio",
    "iris_engineered_features:petal_length_bin",
]


def run_demo() -> int:
    store = FeatureStore(repo_path=".")

    print("\n--- Run feast apply ---")
    result = subprocess.run(["feast", "apply"])
    if result.returncode != 0:
        print("feast apply failed", file=sys.stderr)
        return result.returncode

    print("\n--- Historical features for training ---")
    fetch_historical_features(store, for_batch_scoring=False)

    print("\n--- Historical features for batch scoring ---")
    fetch_historical_features(store, for_batch_scoring=True)

    print("\n--- Load features into the online store ---")
    store.materialize_incremental(end_date=datetime.now())

    print("\n--- Online features ---")
    fetch_online_features(store)

    print("\n--- Online features through the feature service ---")
    fetch_online_features(store, source="feature_service")

    return 0


def fetch_historical_features(store: FeatureStore, for_batch_scoring: bool):
    source_df = pd.read_parquet("data/iris_features.parquet")

    entity_df = source_df[["sample_id", "event_timestamp"]].head(5).copy()

    # For batch scoring we want the latest available timestamps.
    if for_batch_scoring:
        entity_df["event_timestamp"] = pd.to_datetime("now", utc=True)

    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=MEASUREMENT_FEATURES + ENGINEERED_FEATURES,
    ).to_df()

    print(training_df.head())


def fetch_online_features(store: FeatureStore, source: str = ""):
    entity_rows = [
        {"sample_id": 1},
        {"sample_id": 2},
    ]

    if source == "feature_service":
        features_to_fetch = store.get_feature_service("iris_feature_service")
    else:
        features_to_fetch = MEASUREMENT_FEATURES + ENGINEERED_FEATURES

    returned_features = store.get_online_features(
        features=features_to_fetch,
        entity_rows=entity_rows,
    ).to_dict()

    for key, value in sorted(returned_features.items()):
        print(key, " : ", value)


if __name__ == "__main__":
    sys.exit(run_demo())
