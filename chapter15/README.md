# chapter15 (번역서 14장)

『[Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)』 번역서 14장의 예제 코드입니다.

## 구성

이 폴더에는 모니터링, 로깅, 수평 확장 등을 다루는 DAG가 들어 있습니다. 시연용 Docker Compose 구성이 딸려 있고, 다음을 포함합니다.

- Airflow (웹 UI, 스케줄러, Celery 워커)
- Airflow 메타스토어용 PostgreSQL 데이터베이스
- Celery 큐용 Redis
- Celery 모니터링 도구 Flower
- 메트릭 스크레이프·저장용 Prometheus
- 메트릭 시각화용 Grafana
- 메트릭 노출용 Redis·StatsD 익스포터

서비스 수가 많아 머신 자원을 꽤 잡아먹을 수 있습니다.

아쉽게도 모든 것을 스크립트로 미리 초기화할 수는 없습니다. 특히 Grafana가 그렇습니다. Prometheus를 데이터 소스로 추가하고 대시보드를 만드는 일은 직접 해야 합니다.

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
