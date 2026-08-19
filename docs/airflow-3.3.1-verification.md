# Airflow 3.3.1 검증 결과

한국어판 번역 과정에서, 이 저장소의 예제 코드가 검증 시점의 최신 안정 버전인 **Apache Airflow 3.3.1**(2026-08-12 릴리스)에서 동작하는지 확인한 기록입니다.

- 검증일: 2026-08-20
- 대상 코드: 이 저장소 master (원본 64f057e 기준, 기본 이미지 핀 `apache/airflow:3.1.2`)
- 검증 환경: Docker Desktop(Windows 11), 이미지 `apache/airflow:3.3.1`(파이썬 3.13)

## 검증 방법

1. **DAG 임포트 검사.** 장별 `dags/` 디렉터리를 3.3.1 컨테이너에 마운트하고 DagBag으로 로드해 임포트 오류를 수집했습니다. 장 전용 의존성이 필요한 장은 해당 패키지를 설치하거나 `PYTHONPATH`를 지정해 재검사했습니다.
2. **단위 테스트.** chapter10(테스트 장)의 pytest 스위트를 3.3.1 컨테이너에서 실행했습니다.
3. **통합 실행.** chapter01을 `AIRFLOW_IMAGE_NAME=apache/airflow:3.3.1`로 Docker Compose 기동해, 전 서비스 기동과 DAG 실행 성공까지 확인했습니다.
4. **정적 호환성 검토(2차).** 임포트 검사로 잡히지 않는 문제를 겨냥해 별도 도구로 소스를 전수 검토했습니다. Airflow 3.0에서 제거된 API(`schedule_interval`, `sla`, `SubDagOperator`, `days_ago`, `provide_context`)와 제거된 Jinja 템플릿 변수(`execution_date`, `next_ds`, `prev_ds` 계열), 구성 키 개명을 검색하고, 의심 지점은 3.3.1 컨테이너의 설정 조회와 소스 코드로 실측 대조했습니다. chapter11과 chapter16의 하위 디렉터리 DAG도 이 단계에서 보완 검사했습니다.

## 결과 요약

**3.3.1과 호환되지 않는 예제 코드는 발견되지 않았습니다.** 임포트 단계의 실패는 전부 장 전용 의존성이나 실행 환경 요건 때문이었고, 요건을 채운 재검사에서 모두 해소되었습니다. 2차 정적 검토에서도 제거 API·템플릿 변수·구성 키 문제는 나오지 않았으며, 버전과 무관한 콜백 시그니처 문제 1건(발견 6)만 새로 확인했습니다.

| 장 | DAG | 결과 | 비고 |
|---|---|---|---|
| chapter01 | 1 | 통과 + 통합 실행 성공 | 아래 통합 실행 참조 |
| chapter02 | 5 | 통과 | |
| chapter03 | 9 | 통과 | |
| chapter04 | 9 | 통과 | |
| chapter05 | 9 | 통과 | |
| chapter06 | 14 | 통과 | |
| chapter07 | 12 | 통과 | |
| chapter08 | 3 | 2 통과, 1 검증 불가 | sagemaker 번들 타르볼 설치 실패(아래 발견 2) |
| chapter09 | 5 | 통과 | `PYTHONPATH=src`, `MOVIELENS_*` 환경 변수 필요 |
| chapter10 | (검사용 픽스처) | pytest 10/12 통과 | 실패 2건은 검증 환경 요인(아래 발견 4) |
| chapter11 | 2 | 통과 | `docker/`·`kubernetes/` 하위 디렉터리의 DAG, `MOVIELENS_*` 환경 변수 필요 |
| chapter12 | 9 | 통과 | |
| chapter13 | 1 | 통과 | `geopandas`, `minio` 설치와 `PYTHONPATH=src` 필요 |
| chapter14 | 2 | 통과 | |
| chapter15 | 5 | 4 통과, 1 구성 필요 | Edge 익스큐터 예제(아래 발견 3), 콜백 시그니처(아래 발견 6) |
| chapter16 | 4 | 통과 | 하위 구성(01-rbac 등)별 dags 디렉터리 |
| chapter17 | 1 | 통과 | |

### 통합 실행 (chapter01)

`apache/airflow:3.3.1`로 기동한 결과, api-server, dag-processor, scheduler, triggerer, worker, postgres, redis 일곱 서비스가 모두 healthy 상태가 되었고, `01_umbrella` DAG의 스케줄 실행과 수동 트리거 실행이 모두 success로 끝났습니다(태스크 7개 전부 성공).

## 발견 사항

1. **폐기 경고.** 3.3.1은 일부 예제가 쓰는 임포트 경로에 폐기 경고를 냅니다. 동작에는 지장이 없지만 이후 버전에서 제거될 예정입니다.
   - `airflow.hooks.base.BaseHook` → `airflow.sdk.bases.hook.BaseHook` (chapter09, chapter10, chapter13 등)
   - `airflow.utils.context.Context` → `airflow.sdk` 이하 경로 (chapter09)
   - `airflow.models.dagbag.DagBag` → `airflow.dag_processing.dagbag.DagBag` (검사 스크립트 작성 시 확인)
2. **chapter08 sagemaker 타르볼.** `dependencies/sagemaker-2.252.1.dev0.tar.gz`가 3.3.1 이미지(파이썬 3.13)에서 `metadata-generation-failed`로 설치되지 않습니다. `01_aws_handwritten_digits_classifier` DAG는 기본 핀(3.1.2, 파이썬 3.12) 환경에서 검증해야 합니다. 나머지 두 DAG(insideairbnb)는 3.3.1에서 통과했습니다.
3. **chapter15 Edge 익스큐터.** `05_hello_world_on_edge`는 `edge3` 공급자와 `[core] executors` 구성이 없으면 `UnknownExecutorException`이 납니다. `Dockerfile.edge`로 이미지를 구성하면 해소되는 정상 동작입니다.
4. **chapter10 pytest.** 12개 중 10개 통과. 실패 2건(`test_movielens_to_postgres_operator`, `test_dagtestdag`)은 postgres 컨테이너를 띄우는 픽스처가 이번 검증의 중첩 컨테이너 구조에서 경로를 찾지 못한 것으로, 원본 CI처럼 호스트에서 직접 실행하면 해당되지 않습니다.
5. **Windows 체크아웃 주의.** 각 장의 `compose.yaml`은 루트 `official-airflow-docker-compose.yml`을 가리키는 심링크입니다. Windows 기본 설정(`core.symlinks=false`)에서는 대상 경로가 적힌 텍스트 파일로 풀리므로, 개발자 모드에서 `git clone -c core.symlinks=true`로 받거나, 루트 compose 파일을 장 디렉터리로 복사한 뒤 실행해야 합니다.
6. **chapter15 DAG 실패 콜백 시그니처.** `02_dag_failure_callback.py`의 `send_error()`는 인자를 받지 않지만, Airflow는 실패 콜백을 `callback(context)`처럼 context를 넘겨 호출합니다(3.3.1 `airflow/dag_processing/processor.py` 실측). 그래서 콜백이 실제로 불리는 시점에 `TypeError`가 나고 "Callback failed"로 로깅만 된 채 알림 동작이 무산됩니다. 같은 저장소의 `03_task_failure_callback.py`는 `send_error(x)`로 인자를 받아 문제가 없습니다. 버전 회귀가 아니라 2.x에서도 같은 동작입니다.
7. **구성 키 실측.** 장별 `AIRFLOW__*` 키 21종을 3.3.1에서 조회한 결과, chapter13의 `webserver.expose_config`는 유효하고 chapter15의 `core.internal_api_secret_key`는 3.3.1에 존재하지 않는 키였습니다(무해한 잔재, 무시됨). 제거된 `AIRFLOW__CORE__SQL_ALCHEMY_CONN`류는 없습니다.
8. **제거 API 잔존 0건 확정.** 2차 정적 검토에서 `schedule_interval`, `sla`, `SubDagOperator`, `days_ago`, `provide_context`, `execution_date`·`next_ds`·`prev_ds` 계열 템플릿 변수의 잔존이 전 장에서 0건임을 확인했습니다. 템플릿 변수는 `logical_date`(50회), `data_interval_start`(48회) 등 3.x 체계로 정리되어 있습니다.

## 재현 방법

```bash
# 1) DAG 임포트 검사 (예: chapter02)
docker run --rm -e AIRFLOW__CORE__LOAD_EXAMPLES=false \
  -v ./chapter02/dags:/opt/airflow/dags:ro apache/airflow:3.3.1 \
  python -c "from airflow.dag_processing.dagbag import DagBag; \
             db = DagBag('/opt/airflow/dags'); print(db.import_errors or 'OK')"

# 2) chapter10 pytest (저장소 루트에서)
docker run --rm -v .:/repo:ro -v /var/run/docker.sock:/var/run/docker.sock \
  -e PYTHONPATH=/repo:/repo/chapter10/dags -e HOME=/tmp -w /repo/chapter10 \
  apache/airflow:3.3.1 bash -c "pip install -q -r requirements.txt && python -m pytest tests/ -q"

# 3) chapter01 통합 실행
cd chapter01
AIRFLOW_IMAGE_NAME=apache/airflow:3.3.1 docker compose up -d
docker compose exec airflow-scheduler airflow dags trigger 01_umbrella
docker compose down -v
```
