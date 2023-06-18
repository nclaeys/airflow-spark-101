from airflow import DAG
from datetime import datetime, timedelta
from airflow.utils import dates
from airflow.operators.bash_operator import BashOperator

default_args = {
    "depends_on_past": False,
    "start_date": datetime.now() - timedelta(days=10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "pyspark-taxi-example",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
)

BashOperator(
    dag=dag,
    task_id='execute_spark_job',
    bash_command="spark-submit /workspace/src/pysparkexample/app.py -e prd -d {{ ds }}",
)
