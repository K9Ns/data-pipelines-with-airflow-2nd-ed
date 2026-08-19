# 1장

『Data Pipelines with Apache Airflow, Second Edition』 1장의 예제 코드입니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01_umbrella.py`: 우산 사용 사례를 보여 주는 DAG.

## 사용법

다음 명령으로 Docker에서 Airflow를 시작합니다.

```
docker compose up -d
```

몇 초 기다리면 http://localhost:8080/ 에서 예제에 접근할 수 있습니다.

예제 실행을 멈추려면 다음 명령을 실행합니다.

```
docker compose down -v
```
