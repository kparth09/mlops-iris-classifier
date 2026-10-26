"""Tests for model prediction quality."""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

MIN_ACCEPTABLE_ACCURACY = 0.999


def test_model_predictions_have_valid_classes():
    df = pd.read_csv("data/processed/iris_features.csv")

    target_col = "species"
    feature_cols = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
    ]

    X = df[feature_cols]
    encoder = LabelEncoder()
    y = encoder.fit_transform(df[target_col])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    assert set(predictions).issubset(set(y))
    assert accuracy >= MIN_ACCEPTABLE_ACCURACY, (
        f"Model accuracy {accuracy:.4f} is below "
        f"the minimum threshold of {MIN_ACCEPTABLE_ACCURACY:.3f}"
    )