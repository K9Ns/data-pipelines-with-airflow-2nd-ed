# 시크릿 백엔드

HashiCorp Vault와 연결해 시크릿 백엔드를 사용하는 방법을 시연합니다.

## 사용법

이 데모는 다음 단계로 실행합니다.

1. `docker-compose up -d`
2. HashiCorp Vault(http://localhost:8200)에 토큰 `airflow` 로 로그인합니다.
3. `secret/` 아래에 다음 내용으로 새 시크릿을 만듭니다.
    - 경로 `connections/secure_api`
    - 키 `conn_uri`
    - 값 `http://secure_api:5000?token=supersecret`
4. Airflow(http://localhost:8080)로 가서 "secretsbackend_with_vault" DAG를 트리거합니다.
5. 성공하면 로그에 "Welcome!"이 보입니다. 디버그 로깅이 켜져 있어 Vault 호출도 로그에서 볼 수 있습니다.

## 세부 사항

호스트에 노출되는 포트는 다음과 같습니다.

- 5432: PostgreSQL (user=airflow, pass=airflow)
- 8080: Airflow 웹서버
- 8200: HashiCorp Vault
