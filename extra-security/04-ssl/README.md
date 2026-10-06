# SSL 구성

## SSL 인증서 생성

```bash
openssl req \
-x509 \
-newkey rsa:4096 \
-sha256 \
-nodes \
-days 365 \
-keyout privatekey.pem \
-out certificate.pem \
-extensions san \
-config \
 <(echo "[req]";
   echo distinguished_name=req;
   echo "[san]";
   echo subjectAltName=DNS:localhost,IP:127.0.0.1
   ) \
-subj "/CN=localhost"
```

## 사용법

```
docker compose up -d
```

보안 웹사이트 https://localhost:8080 에 로그인합니다.
