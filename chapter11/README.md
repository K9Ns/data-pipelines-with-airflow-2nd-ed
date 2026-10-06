# chapter12 (번역서 11장)

『Data Pipelines with Apache Airflow, Second Edition』 번역서 11장의 예제 코드입니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01_task_factory.py`: 흔한 태스크 패턴을 팩토리 메서드로 만드는 방법.
- `02_dag_factory_customers.py` / `02_dag_factory_sales.py`: 비슷한 DAG 여러 인스턴스를 팩토리 메서드로 만드는 방법.
- `03_task_groups.py`: 태스크 그룹 사용법.
- `04_task_groups_umbrella.py`: 날씨 API 예제로 보는 좀 더 복잡한 태스크 그룹.
- `06_dynamic_task_mapping.py`: 전통적 API로 구성한 동적 태스크 매핑 시연.
- `07_dynamic_task_mapping_taskflow.py`: 06과 같되 TaskFlow API 사용.
- `08_dynamic_task_mapping_taskgroup.py`: 동적 태스크 매핑과 태스크 그룹의 조합.
- `09_no_dynamic_task_mapping.py`: 동적 태스크 매핑을 쓰지 않았다면 어떤 DAG가 되는지.

동적 태스크 매핑을 위해, 영화 리뷰를 무작위 개수(1~10)로 생성하는 아주 단순한 REST API도 들어 있습니다. 이를 통해 동적 태스크 매핑이 데이터 구조·내용에 따라 DAG를 동적으로 구성하게 해 준다는 것을 시연합니다. 이 API는 Docker Compose 환경에 포함되어 있습니다.

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
