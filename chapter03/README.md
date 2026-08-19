# chapter03 (번역서 3장)

『Data Pipelines with Apache Airflow, Second Edition』 3장의 예제 코드입니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01_unscheduled.py`: 스케줄 없는 초기 DAG.
- `02_trigger_cron.py`: cron 표현식 기반 `CronTriggerTimetable`로 트리거하는 DAG.
- `03_trigger_preset.py`: `@daily` 같은 프리셋으로 트리거하는 DAG.
- `04_trigger_frequency.py`: `DeltaTriggerTimetable`로 일정 빈도마다 트리거하는 DAG.
- `05_interval_cron.py`: cron 기반 데이터 간격(`CronDataIntervalTimetable`)을 사용하는 DAG.
- `06_interval_delta.py`: 프리셋 기반 데이터 간격을 사용하는 DAG.
- `07_events_timetable.py`: 공휴일 목록 같은 이벤트 타임테이블로 스케줄링하는 DAG.
- `08_non_atomic_send.py`: 통계 계산과 전송이 한 태스크에 섞인, 원자적이지 않은 예제.
- `09_atomic_send.py`: 통계 계산과 전송을 태스크로 분리한 원자적 예제.

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
