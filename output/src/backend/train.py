import os

import mlflow.sklearn
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

INPUTS_TEXT = """The model expects a list of 4 floats.

Example request body:
{"features": [0.1, -1.2, 0.3, 2.4]}
"""


def main() -> None:
    X, y = make_classification(n_samples=300, n_features=4, n_informative=3, n_redundant=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    model = LogisticRegression(max_iter=500, n_jobs=1)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Accuracy: {accuracy:.3f}")

    mlflow.sklearn.save_model(model, MODEL_PATH)
    with open(os.path.join(MODEL_PATH, "INPUTS.txt"), "w") as f:
        f.write(INPUTS_TEXT)
    print(f"Saved MLflow model to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
