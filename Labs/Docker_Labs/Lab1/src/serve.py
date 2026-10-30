"""
Prediction API that serves the model trained by main.py.

It loads model.joblib and metadata.json from MODEL_DIR when it starts.
  GET  /         service info
  GET  /health   used by the Docker HEALTHCHECK
  GET  /version  model metadata (accuracy, trees, training time, image version)
  POST /predict  {"features": [4 numbers]} or {"instances": [[4 numbers], ...]}
"""
import json
import os

import joblib
import numpy as np
from flask import Flask, jsonify, request

MODEL_DIR = os.environ.get("MODEL_DIR", "/models")
MAX_ROWS = 100

app = Flask(__name__)
model = joblib.load(os.path.join(MODEL_DIR, "model.joblib"))
with open(os.path.join(MODEL_DIR, "metadata.json")) as f:
    metadata = json.load(f)
N_FEATURES = len(metadata["features"])


@app.get("/")
def home():
    return jsonify({
        "message": "Iris classifier served from a Docker container",
        "endpoints": ["/health", "/version", "POST /predict"],
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/version")
def version():
    return jsonify(metadata)


def bad_request(message):
    return jsonify({"error": message}), 400


@app.post("/predict")
def predict():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return bad_request('Send JSON, e.g. {"features": [5.1, 3.5, 1.4, 0.2]}')
    if "features" in body:
        rows = [body["features"]]
    elif "instances" in body:
        rows = body["instances"]
    else:
        return bad_request("JSON must contain 'features' (one row) or 'instances' (list of rows)")
    if not isinstance(rows, list) or not rows:
        return bad_request("'instances' must be a non-empty list")
    if len(rows) > MAX_ROWS:
        return bad_request(f"At most {MAX_ROWS} rows per request")
    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != N_FEATURES:
            return bad_request(f"Row {i} must be a list of {N_FEATURES} numbers: {metadata['features']}")
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in row):
            return bad_request(f"Row {i} must contain only numbers")

    probabilities = model.predict_proba(np.array(rows, dtype=float))
    predictions = []
    for probs in probabilities:
        best = int(np.argmax(probs))
        predictions.append({
            "class": metadata["classes"][best],
            "confidence": round(float(probs[best]), 4),
        })
    return jsonify({"predictions": predictions, "model_trees": metadata["n_estimators"]})
