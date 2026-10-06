from datetime import date, timedelta
import itertools
import time

from faker import Faker
from fastapi import FastAPI
import numpy as np
import pandas as pd

app = FastAPI()


def _generate_events_daily(event_date: date):
    """주어진 날짜의 이벤트를 생성한다."""

    # 날짜를 시드로 사용한다.
    seed = int(time.mktime(event_date.timetuple()))

    Faker.seed(seed)
    random_state = np.random.RandomState(seed)

    # 사용자 수와 이벤트 수를 정한다.
    n_users = random_state.randint(low=50, high=100)
    n_events = random_state.randint(low=200, high=1000)

    # 사용자 여럿을 생성한다.
    fake = Faker()
    users = [fake.ipv4() for _ in range(n_users)]

    # 사용자별 이벤트를 생성한다.
    events = pd.DataFrame(
        {
            "user": random_state.choice(users, size=n_events, replace=True),
            "timestamp": _random_datetimes(event_date, size=n_events, random_state=random_state),
        }
    ).sort_values(by="timestamp")

    # 이벤트를 레코드로 변환한다.
    records = events.to_dict(orient="records")

    return records


def _random_datetimes(event_date: date, size: int, random_state):
    """주어진 날짜 안의 무작위 시각 열을 생성한다."""
    return pd.to_timedelta(random_state.rand(size), unit='D') + pd.to_datetime(event_date)


def _generate_events_range(start_date: date, end_date: date):
    """날짜 범위의 이벤트를 생성한다(종료 날짜는 제외)."""
    return list(
        itertools.chain.from_iterable(
            _generate_events_daily(d)
            for d in date_range(start_date, end_date)
        )
    )


def date_range(start_date: date, end_date: date):
    """시작 날짜와 종료 날짜(제외) 사이를 도는 날짜 이터레이터."""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/events/latest")
def events_latest(days: int = 7):
    """지난 7일의 이벤트를 반환하는 엔드포인트."""
    start_date = date.today() - timedelta(days=days)
    end_date = date.today()
    return _generate_events_range(start_date, end_date)


@app.get("/events/range")
def events_range(start_date: date, end_date: date):
    """주어진 시작·종료 날짜(종료는 제외) 사이의 이벤트를 반환하는 엔드포인트."""
    return _generate_events_range(start_date, end_date)
