"""
Tests that run INSIDE the Docker build (the `test` stage).
If any test fails, `docker build` fails and no image is produced.

MIN_ACCURACY is a build argument, so you can raise the quality bar:
  docker build --build-arg MIN_ACCURACY=0.99 -t lab1:strict .
"""
import importlib
import os
import sys

TEST_MODEL_DIR = "/tmp/test_models"
MIN_ACCURACY = float(os.environ.get("MIN_ACCURACY", "0.85"))

os.environ["MODEL_DIR"] = TEST_MODEL_DIR
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import main  # noqa: E402

metadata = main.train(model_dir=TEST_MODEL_DIR)
serve = importlib.import_module("serve")
client = serve.app.test_client()


def test_training_writes_model_and_metadata():
    assert os.path.exists(os.path.join(TEST_MODEL_DIR, "model.joblib"))
    assert os.path.exists(os.path.join(TEST_MODEL_DIR, "metadata.json"))


def test_model_meets_quality_bar():
    assert metadata["test_accuracy"] >= MIN_ACCURACY, (
        f"Accuracy {metadata['test_accuracy']} is below MIN_ACCURACY={MIN_ACCURACY}"
    )


def test_health():
    assert client.get("/health").get_json()["status"] == "ok"


def test_version():
    assert client.get("/version").get_json()["model_type"] == "RandomForestClassifier"


def test_predict_setosa():
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    assert r.get_json()["predictions"][0]["class"] == "setosa"


def test_predict_batch():
    r = client.post("/predict", json={"instances": [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3]]})
    assert [p["class"] for p in r.get_json()["predictions"]] == ["setosa", "virginica"]


def test_predict_rejects_bad_input():
    assert client.post("/predict", json={"features": [1, 2]}).status_code == 400
    assert client.post("/predict", json={"features": ["a", 1, 2, 3]}).status_code == 400
    assert client.post("/predict", data="not json").status_code == 400
