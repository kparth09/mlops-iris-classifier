# tests/test_training_pipeline.py

"""
Tests for the machine learning training pipeline.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def test_training_pipeline_trains_model():
    # Create a small sample dataset
    df = pd.DataFrame({
        "sepal length (cm)": [5.1, 4.9, 6.2, 5.9, 7.0, 6.5],
        "sepal width (cm)": [3.5, 3.0, 3.4, 3.0, 3.2, 3.0],
        "petal length (cm)": [1.4, 1.4, 5.4, 5.1, 4.7, 5.2],
        "petal width (cm)": [0.2, 0.2, 2.3, 1.8, 1.4, 2.0],
        "species": [
            "setosa",
            "setosa",
            "virginica",
            "virginica",
            "versicolor",
            "versicolor",
        ],
    })

    feature_cols = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
    ]

    X = df[feature_cols]

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["species"])

    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.50,
    random_state=42,
    stratify=y,
)
    model = RandomForestClassifier(
        n_estimators=10,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    assert len(predictions) == len(y_test)
    assert set(predictions).issubset(set(y))
    assert hasattr(model, "predict")