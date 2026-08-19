# 2장

『[Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)』 2장의 예제 코드입니다.

## 구성

이 폴더에는 2장의 DAG가 들어 있습니다.

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
