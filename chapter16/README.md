# chapter16 (Airflow 보안)

『[Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)』의 보안 장(원서 최종판 기준, 번역 원고 MEAP v15에는 미수록) 예제 코드입니다.

## 구성

이 폴더에는 Docker Compose 예제 다섯 개가 들어 있습니다.

- `01-rbac`: RBAC 인터페이스를 설명하는 예제
- `02-webserver-theme`: UI 구성을 설명하는 예제
- `03-ldap`: OpenLDAP에서 사용자 자격 증명을 가져오는 구성 예제
- `04-ssl`: Airflow 구성요소 사이의 보안 연결 구성 예제
- `05-secretsbackend`: HashiCorp Vault에서 시크릿을 가져오는 예제

각 폴더의 Docker Compose 파일은 `docker compose up -d` 로 시작할 수 있습니다.

## 사용법

각 디렉터리의 `README.md` 파일을 읽어 보세요.
