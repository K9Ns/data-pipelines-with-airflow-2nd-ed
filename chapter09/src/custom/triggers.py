import asyncio
from typing import Any

from airflow.models import BaseOperator
from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.utils.context import Context


from custom.hooks import MovielensHook
import uuid

class MovielensSensorAsync(BaseOperator):
    """
    XCom을 사용할 수 있게 될 때까지 기다리는 지연 가능 센서.
    """

    template_fields = ("_start_date", "_end_date")

    def __init__(self,
                 conn_id:str, 
                 start_date:str="{{data_interval_start | ds}}", 
                 end_date:str="{{data_interval_end | ds}}",
                 sleep_interval: int = 30, 
                 **kwargs
            ):
        super().__init__(**kwargs)
        self._sleep_interval = sleep_interval
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date
        self._timeout = kwargs.get('execution_timeout')

    def execute(self, context: Context) -> None:

        self.defer(
            trigger=MovielensTrigger(
                conn_id=self._conn_id,
                sleep_interval=self._sleep_interval,
                start_date=self._start_date,
                end_date=self._end_date,
            ),
            method_name='execute_complete',
            timeout = self._timeout
        )

    def execute_complete(self,context: Context, event: dict[str, Any] | None = None ) -> None:
        self.log.info(
                f"Movie Ratings are Available! for {self._start_date}-{self._end_date}"
            )



class MovielensTrigger(BaseTrigger):
    def __init__(self,          
                 conn_id, 
                 start_date, 
                 end_date,
                 sleep_interval, 

            ):
        super().__init__()
        self._sleep_interval = sleep_interval
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date


    def serialize(self):
        return ("custom.triggers.MovielensTrigger", {
                "sleep_interval": self._sleep_interval,
                "conn_id": self._conn_id,
                "start_date": self._start_date,
                "end_date": self._end_date,
            }
        )
  
    async def run(self):
        # 데이터베이스 백엔드의 비동기 버전을 얻는다. 해당 라이브러리(예: asyncpg)가
        # 트리거러 환경에 설치되어 있다고 가정한다.

        with MovielensHook(self._conn_id) as hook:
            found_records = True
            while not found_records:
                try:
                    next(hook.get_ratings(start_date=self._start_date, end_date=self._end_date, batch_size=1))
                    # StopIteration이 나지 않았다면 요청이 레코드를 하나 이상 반환한 것이다.
                    # 주어진 기간에 레코드가 있다는 뜻이므로, True를 반환해 Airflow에 알린다.
                    self.log.info(f"Found ratings for {self._start_date} to {self._end_date}, continuing!")
                    found_records = True
                except StopIteration:
                    self.log.info(
                        f"Didn't find any ratings for {self._start_date} to {self._end_date}, waiting..."
                    )
                    # StopIteration이 났다면 요청이 레코드를 찾지 못한 것이다.
                    # 해당 기간에 평점이 없다는 뜻이므로 잠시 기다렸다가 재시도해야 한다.
                    await asyncio.sleep(self.check_interval)
        
        yield TriggerEvent(str(uuid.uuid4()))