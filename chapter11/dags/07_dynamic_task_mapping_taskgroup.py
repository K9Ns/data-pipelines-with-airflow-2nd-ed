import pendulum
import requests
from airflow.sdk import DAG, task, task_group
from airflow.timetables.trigger import CronTriggerTimetable

@task
def fetch_ratings():
    "영화 리뷰 API에서 최신 평점을 가져온다. 리뷰 수는 요청마다 다르다"
    data = requests.get("http://movie-reviews-api:8081/reviews/latest")
    return data.json()


@task_group(group_id="print_group")
def print_group(rating):
    @task
    def print_movie(rating):
        print(f"New rating for Movie: {rating["movie"]}")
        return rating

    @task
    def print_rating(rating):
        print(f"Rating: {rating["rating"]}")

    print_movie(rating) >> print_rating(rating)


with DAG(dag_id="08_dynamic_task_mapping_taskgroup",
         start_date=pendulum.today("UTC").add(days=-5),
         schedule=CronTriggerTimetable("0 16 * * *", timezone="UTC")) as dag:
    print_group.expand(rating=fetch_ratings())
