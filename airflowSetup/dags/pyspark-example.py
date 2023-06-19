from airflow import DAG
from datetime import datetime, timedelta
from airflow.utils import dates
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator

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

DockerOperator(
    dag=dag,
    task_id='docker_execute_spark_job',
    image='taxi-pyspark:1.0',
    api_version='auto',
    auto_remove=True,
    command="/opt/spark/bin/spark-submit /opt/spark/work-dir/src/pysparkexample/app.py -e prd -d {{ ds }}",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge"
)

BashOperator(
    dag=dag,
    task_id='execute_spark_job',
    bash_command="spark-submit /workspace/src/pysparkexample/app.py -e prd -d {{ ds }}",
)
