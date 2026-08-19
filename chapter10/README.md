# chapter10 (번역서 9장)

『Data Pipelines with Apache Airflow, Second Edition』 번역서 9장의 예제 코드입니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01_dag_cycle.py`
- `02_bash_operator_no_command.py`
- `03_duplicate_task_ids.py`
- `04_nodags.py`
- `dagtestdag.py` (번호를 붙이면 pytest에서 모듈을 임포트할 때 문제가 생겨 번호가 없습니다.)

이 DAG들은 UI에서 실행하라고 있는 것이 아니라(일부러 실패하는 것도 있습니다) 테스트 사용법을 보여 주기 위한 것입니다. 그래서 UI에 오류가 표시되지 않도록 `.airflowignore` 파일에 명시적으로 추가되어 있습니다.

`dags/custom` 디렉터리에는 8장에서 소개한 커스텀 훅과 오퍼레이터 여럿이 들어 있습니다. 이를 재료로 (커스텀) 오퍼레이터의 테스트 작성법을 보여 줍니다. 테스트는 `tests` 디렉터리에 있습니다.

## 사용법

다음 명령으로 Docker에서 Airflow를 시작합니다.

```bash
docker compose up
```

몇 초 기다리면 http://localhost:8080/ 에서 예제에 접근할 수 있습니다.

예제 실행을 멈추려면 다음 명령을 실행합니다.

```bash
docker compose down -v
```

테스트 자체를 돌릴 때는 로컬 파이썬 환경을 권합니다. 일부 테스트가 Postgres 같은 서비스를 Docker로 띄우는 데 의존하기 때문입니다. Docker 안의 Docker 문제를 피하려면 가상 환경이 가장 좋습니다. 준비 방법은 다음과 같습니다.

```bash
python -m venv my-venv
source my-venv/bin/activate
pip install -r requirements.txt
airflow db reset
```

마지막 줄은 (일부 테스트에 필요한) 로컬 Airflow 데이터베이스를 초기화합니다. 기본값은 기본 `AIRFLOW_HOME` 경로의 sqlite 데이터베이스이고, 다른 것을 원한다면 구성은 각자의 몫입니다.

이제 다음처럼 테스트를 실행할 수 있습니다.

```bash
pytest tests/
```

모든 테스트를 돌리려면 Docker가 필요합니다. Docker를 쓰는 테스트(test_dagtestdag, test_movielens_to_postgres_operator)는 불안정하게 동작할 수 있어 `@flaky` 표시가 붙어 있습니다. 이 구성은 Python 3.12.4에서 동작이 확인되었습니다.
