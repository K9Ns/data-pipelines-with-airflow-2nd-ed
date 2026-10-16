"""
    리스트: 6.1
"""

import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.timetables.trigger import CronTriggerTimetable

with DAG(
    dag_id="02_wait_for_supermarket_1",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule=CronTriggerTimetable("0 16 * * *", timezone="UTC"),
    description="슈퍼마켓 프로모션 데이터를 수집하는 배치 워크플로. FileSensor를 시연합니다.",
    default_args={"depends_on_past": True},
):
    wait_for_supermarket = FileSensor(
        task_id="wait_for_supermarket_1", filepath="/data/supermarket1/data.csv"
    )
