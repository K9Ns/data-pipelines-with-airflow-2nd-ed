# RBAC 데모

Airflow RBAC 인터페이스를 시연하는 docker compose 파일입니다.

표준 compose 파일을 거의 그대로 사용합니다.

## 사용법

```
docker compose up -d
```

### 첫 사용자 만들기

다음 명령으로 명령줄에서 사용자를 추가할 수 있습니다.

```
docker compose run --remove-orphans airflow-cli bash -c "airflow users create \
  --role Admin \
  --username bobsmith \
  --password topsecret \
  --email bobsmith@company.com \
  --firstname Bob \
  --lastname Smith"
```

[Airflow UI](localhost:8080)에 사용자명/비밀번호 `bobsmith`/`topsecret` 으로 로그인합니다.
