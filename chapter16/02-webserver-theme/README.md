# 웹서버 테마 데모

`webserver_config.py`로 웹서버 테마를 설정하는 것을 시연하는 docker-compose 파일입니다.

## 사용법

```
docker compose up -d
```

웹서버가 뜰 때까지 5초쯤 기다립니다.

Airflow에 사용자명/비밀번호 `airflow`/`airflow` 로 로그인합니다.

## 세부 사항

호스트에 노출되는 포트는 다음과 같습니다.

- 5432: PostgreSQL (user=`airflow`, pass=`airflow`)
- 8080: Airflow 웹서버
