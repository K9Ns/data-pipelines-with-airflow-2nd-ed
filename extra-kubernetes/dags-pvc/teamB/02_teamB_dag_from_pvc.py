"""EmptyOperator로 우산 사용 사례를 시연하는 DAG."""

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG
from airflow.timetables.trigger import CronTriggerTimetable

with DAG(
    dag_id="02_teamB_dag_from_pvc",
    description="PVC에 DAG를 두는 예제.",
    start_date=pendulum.today("UTC").add(days=-5),
    schedule=CronTriggerTimetable("@daily", timezone="UTC"),
):
    teamB_init = EmptyOperator(task_id="teamB_init")

    echo_some = BashOperator(
        task_id="echo_some",
        bash_command='echo "Hello teamB from $(hostname)"',  # noqa: E501
    )

    # 모든 태스크 사이의 의존성 설정
    teamB_init >> echo_some
