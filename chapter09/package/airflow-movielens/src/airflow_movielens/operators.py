import json
import os

from airflow.models import BaseOperator
from airflow.utils import apply_defaults

from .hooks import MovielensHook


class MovielensFetchRatingsOperator(BaseOperator):
    """
    Operator that fetches ratings from the Movielens API.

    Parameters
    ----------
    conn_id : str
        Movielens API에 연결할 때 사용할 연결의 ID. 연결에는 인증 정보
        (login/password)와 API를 제공하는 호스트가 들어 있어야 한다.
    output_path : str
        가져온 평점을 기록할 경로.
    start_date : str
        (템플릿 지원) 평점을 가져오기 시작할 시작 날짜(포함).
        기대 형식은 YYYY-MM-DD(Airflow의 ds 형식과 동일).
    end_date : str
        (템플릿 지원) 평점을 가져올 종료 날짜(제외).
        기대 형식은 YYYY-MM-DD(Airflow의 ds 형식과 동일).
    batch_size : int
        API에서 가져올 배치(페이지) 크기. 값이 클수록 요청 수는 줄지만
        요청당 전송되는 데이터는 많아진다.
    """

    template_fields = ("_start_date", "_end_date", "_output_path")

    @apply_defaults
    def __init__(
        self,
        conn_id,
        output_path,
        start_date="{{data_interval_start | ds}}}",
        end_date="{{data_interval_end | ds}}}",
        batch_size=1000,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._conn_id = conn_id
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date
        self._batch_size = batch_size

    # pylint: disable=unused-argument,missing-docstring
    def execute(self, context):
        hook = MovielensHook(self._conn_id)

        try:
            self.log.info(f"Fetching ratings for {self._start_date} to {self._end_date}")
            ratings = list(
                hook.get_ratings(
                    start_date=self._start_date,
                    end_date=self._end_date,
                    batch_size=self._batch_size,
                )
            )
            self.log.info(f"Fetched {len(ratings)} ratings")
        finally:
            # 훅의 세션을 항상 닫도록 보장한다.
            hook.close()

        self.log.info(f"Writing ratings to {self._output_path}")

        # 출력 디렉터리가 있는지 확인한다.
        output_dir = os.path.dirname(self._output_path)
        os.makedirs(output_dir, exist_ok=True)

        # 출력을 JSON으로 쓴다.
        with open(self._output_path, "w") as file_:
            json.dump(ratings, fp=file_)
