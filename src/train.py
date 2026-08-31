import os
import joblib

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report



def load_data():
    iris = load_iris()

    X_train, X_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, n_estimators=100, max_depth=None):
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    acc = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    return acc, report


def save_model(model, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    joblib.dump(model, file_path)

    print(f"Model saved to {file_path}")


def main():
    # Load data
    X_train, X_test, y_train, y_test = load_data()

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    acc, report = evaluate_model(
        model,
        X_test,
        y_test
    )

    # Display results
    print(f"Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(report)

    # Save model
    save_model(
        model,
        "models/iris_model.joblib"
    )


if __name__ == "__main__":
    main()