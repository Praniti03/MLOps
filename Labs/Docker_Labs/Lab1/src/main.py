"""
Training job (same entry point as the original lab: `python main.py`).

Trains a RandomForest on the Iris dataset and saves the model plus a
metadata.json file to MODEL_DIR. In Docker Compose, MODEL_DIR is a named
volume that the serve container reads from.

Settings come from environment variables, so you can change them at
`docker run` / `docker compose run` time without rebuilding the image:
  MODEL_DIR     where to save the model        (default: /models)
  N_ESTIMATORS  number of trees                (default: 100)
  TEST_SIZE     fraction of data used for test (default: 0.2)
"""
import json
import os
from datetime import datetime, timezone

import joblib
import sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train(model_dir=None, n_estimators=None, test_size=None):
    model_dir = model_dir or os.environ.get("MODEL_DIR", "/models")
    n_estimators = int(n_estimators or os.environ.get("N_ESTIMATORS", 100))
    test_size = float(test_size or os.environ.get("TEST_SIZE", 0.2))

    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=test_size, random_state=42, stratify=iris.target
    )
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)
    accuracy = float(accuracy_score(y_test, model.predict(X_test)))

    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "model.joblib"))
    metadata = {
        "model_type": "RandomForestClassifier",
        "dataset": "iris",
        "n_estimators": n_estimators,
        "test_size": test_size,
        "features": list(iris.feature_names),
        "classes": list(iris.target_names),
        "test_accuracy": round(accuracy, 4),
        "sklearn_version": sklearn.__version__,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "image_version": os.environ.get("IMAGE_VERSION", "dev"),
    }
    with open(os.path.join(model_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    return metadata


if __name__ == "__main__":
    meta = train()
    print(f"Trained RandomForest with {meta['n_estimators']} trees, "
          f"test accuracy {meta['test_accuracy']:.4f}")
    print(f"Model saved to {os.environ.get('MODEL_DIR', '/models')}/model.joblib")
    print("The model training was successful")
