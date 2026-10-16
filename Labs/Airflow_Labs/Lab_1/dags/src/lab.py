"""
ML functions used by the Airflow DAG (dags/airflow.py).

Every function returns JSON-safe values (strings / dicts / lists), so results
can be passed between tasks through XCom without enabling pickling.
"""
import json
import logging
import os
import pickle
import shutil
from datetime import datetime
from io import StringIO

import pandas as pd
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

log = logging.getLogger(__name__)

# dags/src/lab.py -> BASE_DIR = dags/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "file.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

FEATURES = ["BALANCE", "PURCHASES", "CREDIT_LIMIT"]
K_RANGE = range(2, 9)          # number of clusters to try per algorithm
SILHOUETTE_SAMPLE = 2000       # sample size for silhouette (keeps it fast)


# --------------------------------------------------------------------------
# 1. Load
# --------------------------------------------------------------------------
def load_data():
    """Read the CSV and return it as a JSON string."""
    df = pd.read_csv(DATA_PATH)
    log.info("Loaded %d rows x %d columns from %s", len(df), df.shape[1], DATA_PATH)
    return df.to_json(orient="split")


# --------------------------------------------------------------------------
# 2. Validate (used by a BranchPythonOperator)
# --------------------------------------------------------------------------
def validate_data(data_json, **context):
    """
    Data quality checks. Returns the task_id of the next task to run:
      - 'data_preprocessing_task' if the data passes
      - 'data_quality_alert'      if it fails
    """
    params = context["params"]
    min_rows = int(params.get("min_rows", 100))
    max_null_ratio = float(params.get("max_null_ratio", 0.05))

    df = pd.read_json(StringIO(data_json), orient="split")
    missing_cols = [c for c in FEATURES if c not in df.columns]
    null_ratio = (
        float(df[FEATURES].isnull().mean().max()) if not missing_cols else 1.0
    )

    checks = {
        "required_columns_present": not missing_cols,
        "enough_rows": len(df) >= min_rows,
        "null_ratio_ok": null_ratio <= max_null_ratio,
    }
    report = {
        "rows": len(df),
        "missing_columns": missing_cols,
        "max_null_ratio": round(null_ratio, 4),
        "thresholds": {"min_rows": min_rows, "max_null_ratio": max_null_ratio},
        "checks": checks,
        "passed": all(checks.values()),
    }
    context["ti"].xcom_push(key="validation_report", value=report)
    log.info("Validation report: %s", json.dumps(report, indent=2))

    return "data_preprocessing_task" if report["passed"] else "data_quality_alert"


def data_quality_alert(**context):
    """Runs only when validation fails: logs the problem and saves a report."""
    report = context["ti"].xcom_pull(task_ids="validate_data_task", key="validation_report")
    log.warning("DATA QUALITY CHECK FAILED - training skipped. Details: %s", report)
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, f"data_quality_alert_{_ts()}.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return path


# --------------------------------------------------------------------------
# 3. Preprocess
# --------------------------------------------------------------------------
def data_preprocessing(data_json):
    """Drop nulls, standardize the feature columns, save the scaler."""
    df = pd.read_json(StringIO(data_json), orient="split")
    df = df[FEATURES].dropna()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(os.path.join(MODEL_DIR, "scaler.sav"), "wb") as f:
        pickle.dump(scaler, f)

    log.info("Preprocessed %d rows with StandardScaler", len(df))
    return pd.DataFrame(scaled, columns=FEATURES).to_json(orient="split")


# --------------------------------------------------------------------------
# 4. Train (three algorithms, run in parallel by the DAG)
# --------------------------------------------------------------------------
def _train(name, make_model, data_json):
    """Try every k in K_RANGE, keep the k with the best silhouette score."""
    X = pd.read_json(StringIO(data_json), orient="split").values
    best = {"model": name, "k": None, "silhouette": -1.0}
    best_model = None
    scores = {}

    for k in K_RANGE:
        model = make_model(k).fit(X)
        labels = model.predict(X)
        if len(set(labels)) < 2:          # silhouette needs >= 2 clusters
            continue
        score = float(
            silhouette_score(
                X, labels,
                sample_size=min(SILHOUETTE_SAMPLE, len(X)),
                random_state=42,
            )
        )
        scores[k] = round(score, 4)
        if score > best["silhouette"]:
            best.update(k=k, silhouette=round(score, 4))
            best_model = model

    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, f"{name}.sav")
    with open(path, "wb") as f:
        pickle.dump(best_model, f)

    best["path"] = path
    best["scores_by_k"] = scores
    log.info("%s -> best k=%s, silhouette=%.4f", name, best["k"], best["silhouette"])
    return best


def build_save_model(data_json, filename):
    """
    ORIGINAL LAB TASK (kept): builds KMeans for each k, saves the model, and
    returns the SSE list used by the elbow method.
    MODIFIED: also returns the silhouette-based best k so it can be compared
    with the other two algorithms.
    """
    X = pd.read_json(StringIO(data_json), orient="split").values
    sse = []
    for k in K_RANGE:
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42).fit(X)
        sse.append(float(km.inertia_))

    result = _train(
        "kmeans",
        lambda k: KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42),
        data_json,
    )
    # also save under the original lab's filename (model.sav)
    shutil.copy(result["path"], os.path.join(MODEL_DIR, filename))
    result["sse"] = sse
    return result


def load_model_elbow(filename, kmeans_result):
    """
    ORIGINAL LAB TASK (kept): loads the saved KMeans model and finds the
    optimal number of clusters with the elbow method (kneed).
    """
    from kneed import KneeLocator

    with open(os.path.join(MODEL_DIR, filename), "rb") as f:
        model = pickle.load(f)
    kl = KneeLocator(list(K_RANGE), kmeans_result["sse"], curve="convex", direction="decreasing")
    log.info(
        "Elbow method optimal k = %s (silhouette picked k = %s, saved model has %s clusters)",
        kl.elbow, kmeans_result["k"], model.n_clusters,
    )
    return {"elbow_k": int(kl.elbow) if kl.elbow is not None else None,
            "silhouette_k": kmeans_result["k"]}


def train_minibatch_kmeans(data_json):
    return _train(
        "minibatch_kmeans",
        lambda k: MiniBatchKMeans(n_clusters=k, batch_size=1024, n_init=10, random_state=42),
        data_json,
    )


def train_gmm(data_json):
    return _train(
        "gaussian_mixture",
        lambda k: GaussianMixture(n_components=k, covariance_type="full", random_state=42),
        data_json,
    )


# --------------------------------------------------------------------------
# 5. Select best + quality gate
# --------------------------------------------------------------------------
def select_best_model(training_task_ids, **context):
    """Pull every training result from XCom and pick the highest silhouette."""
    results = context["ti"].xcom_pull(task_ids=training_task_ids)
    results = [r for r in results if r and r.get("k") is not None]
    if not results:
        raise ValueError("No training task produced a usable model")

    for r in sorted(results, key=lambda r: r["silhouette"], reverse=True):
        log.info("  %-18s k=%-2s silhouette=%.4f", r["model"], r["k"], r["silhouette"])

    best = max(results, key=lambda r: r["silhouette"])
    log.info("BEST MODEL: %s (k=%s, silhouette=%.4f)", best["model"], best["k"], best["silhouette"])
    return best


def quality_gate(best, **context):
    """Branch: promote the model only if it beats the silhouette threshold."""
    threshold = float(context["params"].get("silhouette_threshold", 0.25))
    passed = best["silhouette"] >= threshold
    log.info(
        "Quality gate: silhouette %.4f vs threshold %.2f -> %s",
        best["silhouette"], threshold, "PROMOTE" if passed else "REJECT",
    )
    return "promote_model" if passed else "reject_model"


def promote_model(best):
    """Copy the winning model to production_model.sav and save its metadata."""
    prod_path = os.path.join(MODEL_DIR, "production_model.sav")
    shutil.copy(best["path"], prod_path)
    meta = {**best, "promoted_at": datetime.now().isoformat(), "production_path": prod_path}
    with open(os.path.join(MODEL_DIR, "production_model_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    log.info("Promoted %s to %s", best["model"], prod_path)
    return meta


def reject_model(best, **context):
    """Runs when the best model is not good enough - nothing is promoted."""
    threshold = context["params"].get("silhouette_threshold", 0.25)
    log.warning(
        "Model %s rejected: silhouette %.4f < threshold %s. Production model unchanged.",
        best["model"], best["silhouette"], threshold,
    )
    return {"rejected_model": best["model"], "silhouette": best["silhouette"]}


# --------------------------------------------------------------------------
# 6. Final report (runs whichever branch was taken)
# --------------------------------------------------------------------------
def generate_report(training_task_ids, **context):
    ti = context["ti"]
    report = {
        "dag_run_id": context["run_id"],
        "generated_at": datetime.now().isoformat(),
        "params": dict(context["params"]),
        "validation": ti.xcom_pull(task_ids="validate_data_task", key="validation_report"),
        "training_results": ti.xcom_pull(task_ids=training_task_ids),
        "elbow_method": ti.xcom_pull(task_ids="train_models.load_model_task"),
        "best_model": ti.xcom_pull(task_ids="select_best_model_task"),
        "quality_gate_decision": ti.xcom_pull(task_ids="quality_gate_task"),
        "promoted": ti.xcom_pull(task_ids="promote_model"),
    }
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, f"pipeline_report_{_ts()}.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    log.info("Pipeline report written to %s", path)
    return path


def on_task_failure(context):
    """Failure callback attached to every task."""
    ti = context["task_instance"]
    log.error("TASK FAILED: %s (try %s) in run %s", ti.task_id, ti.try_number, context["run_id"])


def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
