# Data Pipelines with Apache Airflow, Second Edition

Manning 도서 [Data Pipelines with Apache Airflow, Second Edition](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)의 예제 코드 저장소입니다.

한국어판 번역 작업을 위해 원본 저장소 [godatadriven/data-pipelines-with-airflow-2nd-ed](https://github.com/godatadriven/data-pipelines-with-airflow-2nd-ed)를 클론해 공개로 관리합니다. 원본 영문 README는 [README.en.md](README.en.md)에 그대로 보존되어 있습니다.

- 1판 예제 코드(한국어판): [K9Ns/data-pipelines-with-apache-airflow](https://github.com/K9Ns/data-pipelines-with-apache-airflow)
- 원본과 동기화하려면 `upstream` 리모트로 원본 저장소를 등록해 두었습니다.

## 구조

```
├── chapter01 ~ chapter17    # 장별 예제 코드
├── official-airflow-docker-compose.yml
├── validate-dag-runs.sh     # CI 용 DAG 실행 검증 스크립트
├── pyproject.toml           # 루트 개발 환경 (poetry)
└── README.en.md             # 원본 영문 README
```

각 장 디렉터리는 대체로 다음처럼 구성됩니다.

```
├── dags                     # 장에서 다루는 DAG 예제 (+ 기타 코드)
├── compose.yaml             # 표준 Airflow 구성을 기술하는 Docker Compose 파일
├── compose.override.yaml    # 장 특화 오버라이드와 추가 서비스
├── .env                     # 장 특화 환경 변수
└── README.md                # 장 특화 안내 (있는 경우)
```

> **장 번호 매핑 주의.** 이 저장소의 chapter 디렉터리 번호는 원서 최종판 기준이라, 번역 원고(MEAP v15, 1~14장+부록 A)의 장 번호와 어긋나는 구간이 있습니다. 예를 들어 원고 13장(생성형 AI 프로젝트)의 코드는 `chapter14/`에 있습니다. 각 장 디렉터리의 README와 DAG 파일명으로 대조하세요.

## 사용법

대부분의 예제는 장 디렉터리 안에서 Docker Compose로 실행합니다.

```bash
cd chapter01
docker compose up --build
```

Compose가 필요한 리소스를 띄우고 Airflow 인스턴스를 시작하면, 로컬 브라우저에서 예제를 실행할 수 있습니다. 백그라운드 실행은 `-d`, 정리는 `docker compose down -v`입니다.

Airflow 이미지 버전은 `AIRFLOW_IMAGE_NAME` 환경 변수로 오버라이드할 수 있습니다(기본값은 대부분 `apache/airflow:3.1.2`).

```bash
AIRFLOW_IMAGE_NAME=apache/airflow:3.3.1 docker compose up --build
```

일부 뒷장 예제는 추가 설정이 필요합니다. 해당 장의 README와 책 본문을 참고하세요.

> **Windows 주의.** 각 장의 `compose.yaml`은 루트 `official-airflow-docker-compose.yml`을 가리키는 심링크입니다. Windows 기본 설정에서는 심링크가 텍스트 파일로 체크아웃되므로, 개발자 모드를 켜고 `git clone -c core.symlinks=true`로 받거나 루트 compose 파일을 장 디렉터리로 복사해 사용하세요.

## Airflow 3.3.1 검증

검증 시점(2026-08-20)의 최신 안정 버전인 Airflow 3.3.1에서 전 장의 DAG 임포트, chapter10 pytest, chapter01 통합 실행을 확인했습니다. 3.3.1 비호환으로 확인된 예제는 없으며, 세부 결과와 재현 방법은 [docs/airflow-3.3.1-verification.md](docs/airflow-3.3.1-verification.md)에 있습니다.

## DAG 실행 검증 (CI)

모든 장의 DAG를 실행해 검증하는 스크립트가 있습니다.

```bash
./validate-dag-runs.sh -c chapter01
./validate-dag-runs.sh -c chapter02
```

## 라이선스와 저작자 표시

이 저장소의 코드 저작권은 원서 저자들과 원본 저장소([godatadriven](https://github.com/godatadriven))에 있습니다. 원본 저장소의 `LICENSE` 파일은 현재 비어 있으며, 이 저장소는 원본의 라이선스 방침을 그대로 따릅니다. 한국어판 관련 추가분(README 등)만 이 저장소에서 관리합니다.
