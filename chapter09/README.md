# chapter09 (번역서 8장)

『Data Pipelines with Apache Airflow, Second Edition』 번역서 8장의 예제 코드입니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01_python.py`: 내장 PythonOperator로 사용 사례를 구현한 초기 DAG.
- `02_hook.py`: 앞 DAG를 손봐 영화 API 연결에 커스텀 Airflow 훅을 쓰는 버전.
- `03_operator.py`: 내장 PythonOperator 대신 커스텀 오퍼레이터 클래스를 쓰는 버전.
- `04_sensor.py`: 커스텀 센서 클래스 작성까지 시연하는 최종 버전.

그 밖에 다음 파일들이 있습니다.

```
├── api                         <- 영화 API의 Docker 이미지.
├── dags                        <- DAG를 담은 폴더.
│   ├── custom                  <- DAG에서 쓰는 커스텀 훅 등.
│   │   ├── __init__.py
│   │   ├── hooks.py
│   │   ├── operators.py
│   │   ├── ranking.py
│   │   └── sensors.py
│   └── *.py                    <- 위에서 말한 DAG들.
├── docker-compose.yml
├── src
│   └── airflow-movielens       <- 'custom' 디렉터리와 같은 코드를
│       ├── setup.py               제대로 된 파이썬 패키지로 만든 것.
│       └── src
│           └── airflow_movielens
│               ├── __init__.py
│               ├── hooks.py
│               ├── operators.py
│               └── sensors.py
└── readme.md                   <- 이 파일.
```

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
