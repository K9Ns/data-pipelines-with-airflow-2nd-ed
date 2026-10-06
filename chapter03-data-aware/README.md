# chapter04 (데이터 인지 스케줄링)

『Data Pipelines with Apache Airflow, Second Edition』의 데이터 인지 스케줄링 예제 코드입니다. 원서 최종판에서 신설된 장으로, 번역서 기준으로는 3장의 데이터 인지 스케줄링 절에 해당합니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01a_basic_producer.py` / `01b_basic_consumer.py`: 기본 생산자·소비자 쌍.
- `02a_metadata_producer.py` / `02b_metadata_consumer.py`: 메타데이터를 함께 넘기는 생산자·소비자.
- `03a_skip_producer.py` / `03b_skip_consumer.py`: 갱신을 건너뛰는 경우의 동작.
- `04a_multi_producer1.py` / `04b_multi_producer2.py` / `04c_multi_consumer.py`: 생산자 여럿에 소비자 하나를 연결한 예제.

## 사용법

다음 명령으로 Docker에서 Airflow를 시작합니다.

```bash
docker compose up -d --build
```

몇 초 기다리면 http://localhost:8080/ 에서 예제에 접근할 수 있습니다.

예제 실행을 멈추려면 다음 명령을 실행합니다.

```bash
docker compose down -v
```

## events-api

이 장에는 예제 DAG가 사용하는 `events-api`라는 API가 딸려 있습니다. Airflow DAG 밖에서 이 API에 요청을 보내고 싶다면, Docker Compose 환경 안에서는 다음을 실행합니다.

```bash
curl http://events-api:8081/events/latest
```

로컬 시스템에서 실행하려면 다음을 사용합니다.

```bash
curl http://localhost:8081/events/latest
```
