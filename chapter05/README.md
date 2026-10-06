# chapter06 (번역서 5장)

『Data Pipelines with Apache Airflow, Second Edition』 번역서 5장의 예제 코드입니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01_rocket_pipeline_dependencies.py`: 태스크 여럿으로 구성한 초기 DAG.
- `02_branch_function.py`: 함수 안에서 분기하기.
- `03_branch_dag_old_new.py`: DAG 안에서 분기하기.
- `04_branch_dag_join.py`: DAG 안에서 분기한 뒤 합류하기.
- `05_condition_function.py`: 함수 안에서 조건 처리하기.
- `06_condition_dag.py`: DAG 안에서 조건 처리하기.
- `07_latest_only_condition.py`: 최신 실행에서만 진행하는 조건.
- `08_trigger_rules.py`: 여러 트리거 규칙을 보여 주는 DAG.
- `09_xcoms.py`: XCom 기초.
- `10_xcoms_template.py`: 템플릿과 함께 쓰는 XCom.
- `11_xcoms_return.py`: 반환값으로 등록되는 기본 XCom.
- `12_taskflow.py`: Taskflow API.
- `13_dag_decorator.py`: dag 데코레이터 사용.
- `14_taskflow_mixed_operators.py`: Taskflow와 일반 태스크의 혼합.

## 사용법

다음 명령으로 Docker에서 Airflow를 시작합니다.

```bash
docker compose up -d
```

몇 초 기다리면 http://localhost:8080/ 에서 예제에 접근할 수 있습니다.

예제 실행을 멈추려면 다음 명령을 실행합니다.

```bash
docker compose down -v
```
