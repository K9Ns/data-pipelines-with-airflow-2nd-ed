import requests
from airflow.hooks.base import BaseHook


class MovielensHook(BaseHook):
    """
    MovieLens API용 훅.

    Movielens (REST) API의 세부 사항을 추상화하고, API에서 데이터(평점, 사용자,

    영화 등)를 가져오는 여러 편의 메서드를 제공한다. 실패한 요청의 자동 재시도,

    페이지네이션·인증의 투명한 처리 등도 지원한다.

    Parameters
    ----------
    conn_id : str
        Movielens API에 연결할 때 사용할 연결의 ID. 연결에는 인증 정보
        (login/password)와 API를 제공하는 호스트가 들어 있어야 한다.
    """

    DEFAULT_SCHEMA = "http"
    DEFAULT_PORT = 8081

    def __init__(self, conn_id, retry=3):
        super().__init__(source=None)
        self._conn_id = conn_id
        self._retry = retry

        self._session = None
        self._base_url = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_conn(self):
        """
        훅이 데이터 조회에 사용하는 연결을 반환한다.
        원칙적으로 직접 사용할 일은 없어야 한다.
        """

        if self._session is None:
            # 주어진 연결의 구성(host, login 등)을 가져온다.
            config = self.get_connection(self._conn_id)

            if not config.host:
                raise ValueError(f"No host specified in connection {self._conn_id}")

            schema = config.schema or self.DEFAULT_SCHEMA
            port = config.port or self.DEFAULT_PORT

            self._base_url = f"{schema}://{config.host}:{port}"

            # API로 보내는 모든 요청에 사용할 세션 인스턴스를 만든다.
            self._session = requests.Session()

            if config.login:
                self._session.auth = (config.login, config.password)

        return self._session, self._base_url

    def close(self):
        """활성 세션이 있으면 닫는다."""
        if self._session:
            self._session.close()
        self._session = None
        self._base_url = None

    # API 메서드:

    def get_movies(self):
        """영화 목록을 가져온다."""
        raise NotImplementedError()

    def get_users(self):
        """사용자 목록을 가져온다."""
        raise NotImplementedError()

    def get_ratings(self, start_date=None, end_date=None, batch_size=100):
        """
        주어진 시작/종료 날짜 사이의 평점을 가져온다.

        Parameters
        ----------
        start_date : str
            평점을 가져오기 시작할 시작 날짜(포함). 기대 형식은
            YYYY-MM-DD(Airflow의 ds 형식과 동일).
        end_date : str
            평점을 가져올 종료 날짜(제외). 기대 형식은
            YYYY-MM-DD(Airflow의 ds 형식과 동일).
        batch_size : int
            API에서 가져올 배치(페이지) 크기. 값이 클수록 요청 수는 줄지만
            요청당 전송되는 데이터는 많아진다.
        """

        yield from self._get_with_pagination(
            endpoint="/ratings",
            params={"start_date": start_date, "end_date": end_date},
            batch_size=batch_size,
        )

    def _get_with_pagination(self, endpoint, params, batch_size=100):
        """
        주어진 url/params로 get 요청을 보내 레코드를 가져온다.
        페이지네이션을 고려한다.
        """

        session, base_url = self.get_conn()
        url = base_url + endpoint

        offset = 0
        total = None
        while total is None or offset < total:
            response = session.get(url, params={**params, **{"offset": offset, "limit": batch_size}})
            response.raise_for_status()
            response_json = response.json()

            yield from response_json["result"]

            offset += batch_size
            total = response_json["total"]
