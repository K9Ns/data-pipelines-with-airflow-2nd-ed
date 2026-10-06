"""EmptyOperator로 우산 사용 사례를 시연하는 DAG."""

import pendulum
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG
from airflow.timetables.trigger import CronTriggerTimetable

with DAG(
    dag_id="01_dag_in_image",
    description="커스텀 이미지에 DAG를 넣는 예제.",
    start_date=pendulum.today("UTC").add(days=-5),
    schedule=CronTriggerTimetable("@daily", timezone="UTC"),
):
    fetch_weather_forecast = EmptyOperator(task_id="fetch_weather_forecast")
    fetch_sales_data = EmptyOperator(task_id="fetch_sales_data")
    clean_forecast_data = EmptyOperator(task_id="clean_forecast_data")
    clean_sales_data = EmptyOperator(task_id="clean_sales_data")
    join_datasets = EmptyOperator(task_id="join_datasets")
    train_ml_model = EmptyOperator(task_id="train_ml_model")
    deploy_ml_model = EmptyOperator(task_id="deploy_ml_model")

    # 모든 태스크 사이의 의존성 설정
    fetch_weather_forecast >> clean_forecast_data
    fetch_sales_data >> clean_sales_data
    [clean_forecast_data, clean_sales_data] >> join_datasets
    join_datasets >> train_ml_model >> deploy_ml_model
