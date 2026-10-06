# chapter11 - Docker (번역서 10장)

『Data Pipelines with Apache Airflow, Second Edition』 번역서 10장의 Docker 부분 예제 코드입니다.

## 구성

이 예제는 wttr API를 사용하는 Docker 이미지 예제로 시작합니다. 예제 이미지는 `images/wttr-example` 아래에 있습니다.

그 밖에 movielens 데이터 세트 기반 추천 시스템을 Docker로 시연하는 예제 DAG도 들어 있습니다.

## 사용법

### wttr 이미지

wttr 예제는 다음처럼 실행할 수 있습니다.

```
docker build -t manning-airflow/wttr-example images/wttr-example
docker run manning-airflow/wttr-example Amsterdam
```

wttr 이미지를 빌드하고 그 이미지로 컨테이너를 실행하는 과정이 시작됩니다.

### Docker DAG

예제 DAG는 docker-compose로 실행할 수 있습니다.

```
docker compose up -d --build
```

몇 초 기다리면 http://localhost:8080/ 에서 예제에 접근할 수 있습니다.

예제 실행을 멈추려면 다음 명령을 실행합니다.

```
docker compose down -v
```
