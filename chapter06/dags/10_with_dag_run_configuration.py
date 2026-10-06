"""
    리스트: 6.10, 6.11
"""


import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.timetables.trigger import CronTriggerTimetable

with DAG(
    dag_id="10_with_dag_run_configuration",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule=CronTriggerTimetable("0 16 * * *", timezone="UTC"),
    description="슈퍼마켓 프로모션 데이터를 수집하는 배치 워크플로. PythonSensor를 시연합니다.",
    default_args={"depends_on_past": True},
):
    copy = EmptyOperator(task_id="copy_to_raw")
    process = EmptyOperator(task_id="process")
    create_metrics = EmptyOperator(task_id="create_metrics")
    copy >> process >> create_metrics
