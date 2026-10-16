from datetime import datetime

from airflow.sdk import DAG
from airflow.timetables.interval import CronDataIntervalTimetable
from custom.operators import MovielensFetchRatingsOperator
from custom.sensors import MovielensRatingsSensor

with DAG(
    dag_id="04_sensor",
    description="커스텀 센서와 함께 Movielens API에서 평점을 가져옵니다.",
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 1, 10),
    schedule=CronDataIntervalTimetable("@daily", "UTC"),
    catchup=True
):
    wait_for_ratings = MovielensRatingsSensor(
        task_id="wait_for_ratings",
        conn_id="movielens",
        start_date="{{data_interval_start | ds}}",
        end_date="{{data_interval_end | ds}}",
    )

    fetch_ratings = MovielensFetchRatingsOperator(
        task_id="fetch_ratings",
        conn_id="movielens",
        start_date="{{data_interval_start | ds}}",
        end_date="{{data_interval_end | ds}}",
        output_path="/data/custom_sensor/{{data_interval_start | ds}}.json",
    )

    wait_for_ratings >> fetch_ratings

