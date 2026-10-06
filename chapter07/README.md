# chapter08 (번역서 7장)

『Data Pipelines with Apache Airflow, Second Edition』 번역서 7장의 예제 코드입니다.

## 구성

이 예제에는 다음 DAG가 들어 있습니다.

- `01_aws_handwritten_digits_classifier.py`: SageMaker 외부 연결을 보여 주는 DAG.
- `chapter8_insideairbnb*.py`: postgres-to-s3 오퍼레이터를 보여 주는 작은 DAG.

## 준비

`01_aws_handwritten_digits_classifier`를 실행하려면 다음을 준비해야 합니다.

- AWS ACCESS KEY와 AWS SECRET을 발급받아, 코드를 실행하는 셸에서 쓸 수 있게 합니다.
- SageMaker 실행 역할을 만듭니다(https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html 참고). 그 ARN도 셸에서 쓸 수 있어야 합니다.
- 역할을 만든 리전, 즉 DAG가 태스크를 실행할 리전을 지정합니다.

```sh
export SAGEMAKER_EXEC_ROLE_ARN=
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_REGION=
export AWS_DEFAULT_REGION=
# SECRET KEY에 슬래시(/)가 들어 있으면 URL 인코딩해야 한다
export ENCODED_AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY//\//%2F}
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

## MNIST 분류기 시험하기

SageMaker 엔드포인트로 공개한 MNIST 분류기를 시험하는 방법으로, 책은 Chalice로 만든 작은 API 애플리케이션을 소개합니다.

이 앱은 다음처럼 로컬에서 실행할 수 있습니다.

```sh
cd api/classifier
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_REGION=
export AWS_DEFAULT_REGION=
chalice local --port 8000
```

## airflow test 명령 실행하기

책의 airflow test 명령을 실행하려면 올바른 파이썬 패키지를 갖춘 로컬 환경이 필요합니다.

```sh
python3 -m venv .airflowlocal
source .airflowlocal/bin/activate
pip install -r requirements.txt
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_REGION=
export AWS_DEFAULT_REGION=

airflow tasks test 01_aws_handwritten_digits_classifier create_mnist_bucket 2024-01-01
```
