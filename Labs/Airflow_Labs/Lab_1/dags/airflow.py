r"""
Customer segmentation pipeline - modified Airflow Lab 1.

Original lab: load -> preprocess -> build_save_model -> load_model (elbow)
Modified flow:
  load -> validate --(pass)--> preprocess -> [KMeans(+elbow), MiniBatchKMeans, GMM in parallel]
                   \                         -> select best -> quality gate --(pass)--> promote
                    \                                                      \--(fail)--> reject
                     \--(fail)--> data_quality_alert
  every path ends in -> generate_report
"""
from datetime import datetime, timedelta

from airflow import DAG

# Import paths differ between Airflow 2.x and 3.x - support both.
try:
    from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
    from airflow.providers.standard.operators.empty import EmptyOperator
except ImportError:
    from airflow.operators.python import PythonOperator, BranchPythonOperator
    from airflow.operators.empty import EmptyOperator
try:
    from airflow.sdk import TaskGroup
except ImportError:
    from airflow.utils.task_group import TaskGroup

from src.lab import (
    load_data, validate_data, data_quality_alert, data_preprocessing,
    build_save_model, load_model_elbow, train_minibatch_kmeans, train_gmm,
    select_best_model, quality_gate, promote_model, reject_model,
    generate_report, on_task_failure,
)

TRAINING_TASK_IDS = [
    "train_models.build_save_model_task",
    "train_models.train_minibatch_kmeans",
    "train_models.train_gmm",
]

default_args = {
    "owner": "praniti",
    "start_date": datetime(2025, 1, 1),
    "retries": 2,                          # retry failed tasks twice
    "retry_delay": timedelta(minutes=1),
    "on_failure_callback": on_task_failure,
}

with DAG(
    dag_id="customer_segmentation_pipeline",
    default_args=default_args,
    description="Validated, multi-model clustering pipeline with a quality gate",
    schedule=None,                         # trigger manually from the UI
    catchup=False,
    tags=["mlops", "lab2"],
    # Default parameters - can be overridden with "Trigger DAG w/ config"
    params={
        "min_rows": 100,
        "max_null_ratio": 0.05,
        "silhouette_threshold": 0.25,
    },
) as dag:

    start = EmptyOperator(task_id="start")

    load_data_task = PythonOperator(
        task_id="load_data_task",
        python_callable=load_data,
    )

    validate_data_task = BranchPythonOperator(
        task_id="validate_data_task",
        python_callable=validate_data,
        op_args=[load_data_task.output],
    )

    alert_task = PythonOperator(
        task_id="data_quality_alert",
        python_callable=data_quality_alert,
    )

    data_preprocessing_task = PythonOperator(
        task_id="data_preprocessing_task",
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    # Three algorithms trained in parallel inside one TaskGroup
    with TaskGroup(group_id="train_models") as train_models:
        # ORIGINAL lab tasks, kept: build KMeans + elbow method
        build_save_model_task = PythonOperator(
            task_id="build_save_model_task",
            python_callable=build_save_model,
            op_args=[data_preprocessing_task.output, "model.sav"],
        )
        load_model_task = PythonOperator(
            task_id="load_model_task",
            python_callable=load_model_elbow,
            op_args=["model.sav", build_save_model_task.output],
        )
        build_save_model_task >> load_model_task

        # NEW: two more algorithms trained in parallel with KMeans
        PythonOperator(
            task_id="train_minibatch_kmeans",
            python_callable=train_minibatch_kmeans,
            op_args=[data_preprocessing_task.output],
        )
        PythonOperator(
            task_id="train_gmm",
            python_callable=train_gmm,
            op_args=[data_preprocessing_task.output],
        )

    select_best_task = PythonOperator(
        task_id="select_best_model_task",
        python_callable=select_best_model,
        op_kwargs={"training_task_ids": TRAINING_TASK_IDS},
    )

    quality_gate_task = BranchPythonOperator(
        task_id="quality_gate_task",
        python_callable=quality_gate,
        op_args=[select_best_task.output],
    )

    promote_task = PythonOperator(
        task_id="promote_model",
        python_callable=promote_model,
        op_args=[select_best_task.output],
    )

    reject_task = PythonOperator(
        task_id="reject_model",
        python_callable=reject_model,
        op_args=[select_best_task.output],
    )

    report_task = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report,
        op_kwargs={"training_task_ids": TRAINING_TASK_IDS},
        # run if at least one upstream path succeeded and none failed
        trigger_rule="none_failed_min_one_success",
    )

    # ---------------- dependencies ----------------
    start >> load_data_task >> validate_data_task
    validate_data_task >> [data_preprocessing_task, alert_task]
    data_preprocessing_task >> train_models >> select_best_task >> quality_gate_task
    quality_gate_task >> [promote_task, reject_task]
    [alert_task, promote_task, reject_task] >> report_task
