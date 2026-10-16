"""
리스트: 6.26, 6.27, 6.28
그림: 6.18
"""

import uuid

import pendulum
from airflow.sdk import DAG, task

with DAG(
    dag_id="12_taskflow",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule="@daily",
    catchup=True,
):

    @task
    def train_model():
        model_id = str(uuid.uuid4())
        return model_id

    @task
    def deploy_model(model_id: str):
        print(f"Deploying model {model_id}")

    model_id = train_model()
    deploy_model(model_id)
