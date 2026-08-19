# LDAP

OpenLDAP을 사용한 RBAC UI + LDAP 인증을 시연합니다.

## 사용법

```
docker compose up -d
```

Airflow에 사용자명 `bsmith`, 비밀번호 `test` 로 로그인합니다.

## 세부 사항

OpenLDAP은 다음이 미리 준비된 채 시작됩니다.

- 관리자 사용자 (DN=`cn=admin,dc=apacheairflow,dc=com`, 비밀번호=`admin`)
- 읽기 전용 사용자 (DN=`cn=readonly,dc=apacheairflow,dc=com`, 비밀번호=`readonly`)
- "engineers" 그룹 (DN=`cn=engineers,dc=apacheairflow,dc=com`)
- 이 그룹에 속한 사용자 (DN=`cn=bob smith,dc=apacheairflow,dc=com`, 비밀번호=`test`)

호스트에 노출되는 포트는 다음과 같습니다.

- 5432: PostgreSQL (user=airflow, pass=airflow)
- 8080: Airflow UI
- 8081: phpLDAPadmin (OpenLDAP UI)
