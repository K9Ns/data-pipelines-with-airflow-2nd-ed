# chapter11 - Kubernetes (번역서 10장)

『Data Pipelines with Apache Airflow, Second Edition』 번역서 10장의 Kubernetes 부분 예제 코드입니다.

## 구성

이 디렉터리에는 docker 예제에서 시연한 추천 시스템의 Kubernetes 버전이 들어 있습니다.

### 사용법

먼저 Kubernetes 클러스터가 준비되어 있고 kubectl로 클러스터에 명령을 실행할 수 있어야 합니다.

편의를 위해 docker-compose 안에 클러스터를 하나 마련해 두었으므로, 실행 방식은 다른 장들과 비슷합니다. `minikube`, `docker-desktop`, 혹은 원하는 클라우드 서비스 등 다른 방식으로 k8s 클러스터를 준비해도 됩니다.

```
# 먼저 사용할 이미지를 빌드해 k8s 서비스에서 쓸 수 있게 한다
./setup_local_image_registry.sh
docker compose up -d
```

별도 터미널에서 책에 나온 `kubectl cluster-info` 명령으로 k8s 클러스터에 제대로 연결되는지 확인할 수 있습니다. 자기 머신에서 직접 실행하려면 KUBECONFIG 환경 변수가 올바르게 설정되어 있어야 합니다(.env 참고).
편의를 위해 kubectl이 준비된 docker 컨테이너도 있습니다. 다음처럼 접속합니다.

```
docker exec -ti kubernetes-k3s-cli-1 /bin/bash
```

준비가 되면 필요한 네임스페이스와 자원을 만들 수 있습니다.

```
kubectl create namespace airflow
kubectl -n airflow apply -f /resources/data-volume.yml
kubectl -n airflow apply -f /resources/api.yml
```

API가 제대로 도는지 다음으로 확인할 수 있습니다.

```
kubectl -n airflow port-forward --address 0.0.0.0 svc/movielens 8081:8081
```

브라우저에서 http://localhost:8081 을 열면 API의 hello world 페이지가 보여야 합니다.

이 초기 설정이 끝나면 Airflow 안에서 Kubernetes DAG를 실행할 수 있습니다.

문제가 생기면 다음으로 Kubernetes 파드들의 상태를 조회할 수 있습니다.

```
kubectl --namespace airflow get pods
```

실패한 파드는 다음으로 상태를 들여다볼 수 있습니다.

```
kubectl --namespace describe pod [NAME-OF-POD]
```

사용한 자원은 다음으로 정리할 수 있습니다.

```
docker compose down -v
```
