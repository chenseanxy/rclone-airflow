
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import rclonerc


def get_client():
    return rclonerc.Client(
        group="airflow-sheduled",
    )


def test_conn():
    cli = get_client()
    return cli.op("rc/noop", {"success": "true"})


with DAG(
    "rclone-connection-test",
    start_date=datetime.min,
    tags=['rclone'],
    is_paused_upon_creation=False,
    schedule_interval=None,
    catchup=False,
) as test_dag:
    op = PythonOperator(
        task_id="connect",
        python_callable=test_conn,
    )

