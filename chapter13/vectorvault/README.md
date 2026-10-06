# 로컬 개발 명령

**참고:** 이 명령들은 로컬 개발용입니다. `vectorvault_chat` 서비스는 `compose.override.yaml`에 이미 정의되어 있습니다.

1) Dockerfile.cli 용

docker build -t cli -f Dockerfile.cli .

MinIO에 파일 업로드

```bash
docker run --env-file ~/.env --network=chapter13_default cli upload "2024-10-01"
```

파일 비교

```bash
docker run --env-file ~/.env --network=chapter13_default cli compare "s3://data/2024-10-05" "recipes"
```

파일 전처리

```bash
docker run --env-file ~/.env --network=chapter13_default cli create "recipes"  "text-embedding-3-large"
```

파일 전처리

```bash
docker run --env-file ../.env --network=host cli preprocess "s3://data/2024-10-14"
```

벡터 데이터베이스에 저장

```bash
docker run --env-file ../.env --network=host cli save  "recipes" "s3://data/2024-10-14"
```

Dockerfile.chat 용

```bash
docker build -t chat -f Dockerfile.chat .


docker run --env-file ~/.env -p 8084:8084 --network=chapter14_default chat
```
