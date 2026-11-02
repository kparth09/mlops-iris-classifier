# tests/test_model_quality.py

"""
Tests for basic model prediction quality.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def test_model_predictions_have_valid_classes():
    df = pd.DataFrame({
        "sepal length (cm)": [5.1, 4.9, 6.2, 5.9, 7.0, 6.5,
                              5.0, 6.1, 5.8, 6.7, 4.8, 6.4],
        "sepal width (cm)": [3.5, 3.0, 3.4, 3.0, 3.2, 3.0,
                             3.4, 2.8, 2.7, 3.1, 3.1, 2.9],
        "petal length (cm)": [1.4, 1.4, 5.4, 5.1, 4.7, 5.2,
                              1.5, 4.7, 4.1, 4.4, 1.6, 4.3],
        "petal width (cm)": [0.2, 0.2, 2.3, 1.8, 1.4, 2.0,
                             0.2, 1.2, 1.0, 1.4, 0.2, 1.3],
        "species": [
            "setosa", "setosa", "virginica", "virginica",
            "versicolor", "versicolor", "setosa", "versicolor",
            "versicolor", "versicolor", "setosa", "virginica",
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
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=50,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    # Predictions must belong to known classes
    assert set(predictions).issubset(set(y))

    # Accuracy must be a valid proportion
    assert 0.0 <= accuracy <= 1.0