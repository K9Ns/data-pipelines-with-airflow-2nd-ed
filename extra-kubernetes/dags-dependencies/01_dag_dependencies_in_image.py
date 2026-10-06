"""EmptyOperator로 우산 사용 사례를 시연하는 DAG."""

import pendulum
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from airflow.timetables.trigger import CronTriggerTimetable


def _tf_version():
    import tensorflow as tf
    print("TensorFlow version:", tf.__version__)

with DAG(
    dag_id="01_dag_dependencies_in_image",
    description="커스텀 이미지에 DAG 의존성을 넣는 예제.",
    start_date=pendulum.today("UTC").add(days=-5),
    schedule=CronTriggerTimetable("@daily", timezone="UTC"),
):
    some_init_task = EmptyOperator(task_id="init")
    version = PythonOperator(task_id="version", python_callable=_tf_version)
    finish = EmptyOperator(task_id="finish")

    # 모든 태스크 사이의 의존성 설정
    some_init_task >> version >> finish
