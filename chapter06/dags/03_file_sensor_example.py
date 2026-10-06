"""
    그림: 6.5
"""


import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.timetables.trigger import CronTriggerTimetable

with DAG(
    dag_id="03_file_sensor_example",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule=CronTriggerTimetable("0 16 * * *", timezone="UTC"),
    description="슈퍼마켓 프로모션 데이터를 수집하는 배치 워크플로. FileSensor를 시연합니다.",
    default_args={"depends_on_past": True},
):
    create_metrics = EmptyOperator(task_id="create_metrics")

    for supermarket_id in [1, 2, 3, 4]:
        wait = FileSensor(
            task_id=f"wait_for_supermarket_{supermarket_id}",
            filepath=f"/data/supermarket{supermarket_id}/data.csv",
        )
        copy = EmptyOperator(task_id=f"copy_to_raw_supermarket_{supermarket_id}")
        process = EmptyOperator(task_id=f"process_supermarket_{supermarket_id}")
        wait >> copy >> process >> create_metrics
