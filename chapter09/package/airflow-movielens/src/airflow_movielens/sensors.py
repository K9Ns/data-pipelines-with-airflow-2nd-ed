"""파일 시스템 센서를 담은 모듈."""

from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

from .hooks import MovielensHook


class MovielensRatingsSensor(BaseSensorOperator):
    """
    해당 기간의 평점이 Movielens API에 생길 때까지 기다리는 센서.

    start_date : str

        (템플릿 지원) 확인할 기간의 시작 날짜(포함).

        기대 형식은 YYYY-MM-DD(Airflow의 ds 형식과 동일).
    end_date : str
        (템플릿 지원) 확인할 기간의 종료 날짜(제외).
        기대 형식은 YYYY-MM-DD(Airflow의 ds 형식과 동일).
    """

    template_fields = ("_start_date", "_end_date")

    @apply_defaults
    def __init__(self, conn_id, start_date="{{data_interval_start | ds}}}", end_date="{{data_interval_end | ds}}}", **kwargs):
        super().__init__(**kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date

    # pylint: disable=unused-argument,missing-docstring
    def poke(self, context):
        hook = MovielensHook(self._conn_id)

        try:
            next(hook.get_ratings(start_date=self._start_date, end_date=self._end_date, batch_size=1))
            # StopIteration이 나지 않았다면 요청이 레코드를 하나 이상 반환한 것이다.
            # 주어진 기간에 레코드가 있다는 뜻이므로, True를 반환해 Airflow에 알린다.
            self.log.info(f"Found ratings for {self._start_date} to {self._end_date}, continuing!")
            return True
        except StopIteration:
            self.log.info(
                f"Didn't find any ratings for {self._start_date} " f"to {self._end_date}, waiting..."
            )
            # StopIteration이 났다면 요청이 레코드를 찾지 못한 것이다.
            # 해당 기간에 평점이 없다는 뜻이므로 False를 반환해야 한다.
            return False
        finally:
            # 훅의 세션을 항상 닫도록 보장한다.
            hook.close()
