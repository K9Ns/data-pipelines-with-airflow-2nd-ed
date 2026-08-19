# chapter05 (번역서 4장)

『[Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)』 번역서 4장의 예제 코드입니다.

## 구성

이 폴더의 DAG는 파일명과 DAG id가 책의 리스트 번호를 따릅니다. 장 끝부분에서는 `SQLExecuteQueryOperator` 사용을 시연합니다. 이 폴더의 Docker Compose 예제는 두 번째 Postgres 데이터베이스를 만들어 주므로, 예제를 실행할 때 직접 준비할 것이 없습니다. 원한다면 다음 정보로 접근할 수 있습니다.

- 호스트: `localhost`
- 포트: `5433`
- 사용자명: `airflow`
- 비밀번호: `airflow`
- 데이터베이스: `airflow`

이 데이터베이스에는 책에 나온 `pageview_counts` 테이블이 초기화되어 있습니다.

## 사용법

다음 명령으로 Docker Compose에서 Airflow를 시작합니다.

```bash
docker compose up -d
```

초기화에 몇 초 걸리니 잠시 기다리면 http://localhost:8080 에서 Airflow 웹 UI에 접근할 수 있습니다.

예제 실행을 멈추려면 다음 명령을 실행합니다.

```bash
docker compose down -v
```
