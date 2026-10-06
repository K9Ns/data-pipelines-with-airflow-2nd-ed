# chapter17 (Kubernetes에 Airflow 배포)

『[Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)』의 배포 장(원서 최종판 기준, 번역 원고 MEAP v15에는 미수록) 예제 코드입니다.

이 장은 Kubernetes에 Airflow를 배포하는 여러 방법을 설명합니다. 배포 명령을 실행할 수 있도록, 이 장의 `docker-compose.yml` 에 Docker Compose 기반 Kubernetes 클러스터가 마련되어 있습니다. 다음 명령으로 클러스터를 시작합니다.

```bash
docker compose up -d
```

!! **이 구성은 자원이 더 필요하므로 docker에 최소 CPU 4개와 메모리 8GB를 주는 것이 좋습니다**

## 더 알아보기

### kubectl과 helm

Kubernetes 클러스터를 다루도록 `kubectl` 과 `helm` 명령을 실행하는 별도 컨테이너가 있습니다. 이 컨테이너는 이른바 login shell로 시작하는 것이 중요합니다. k8s 서버에 접속하는 --server 명령줄 옵션을 채워 주는 `kubectl` 별칭이 필요하기 때문입니다.

```bash
docker exec -ti chapter17-k3s-cli-1 /bin/bash -l
```

#### 대안: k9s 또는 로컬 kubectl

[k9s](https://k9scli.io/)를 쓰거나 kubectl을 로컬에 설치할 수도 있습니다. k3s 클러스터에 접속하려면 클러스터 구성(`KUBECONFIG=.k3s/kubeconfig.yaml`)을 사용해야 합니다.

### K8S에 기본 airflow 배포하기

k3s-cli 컨테이너 안에서 다음 명령으로 airflow를 배포할 수 있습니다.

```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer --set postgresql.image.repository=postgres --set postgresql.image.tag=16
```

실행 중인 서비스/파드는 다음 명령으로 확인합니다.

```bash
kubectl --namespace airflow get pods
```

UI는 http://localhost:8080 에서 접근합니다(api-server 파드가 agent 노드에 배포되면 http://localhost:8081 일 수 있습니다. `kubectl --namespace airflow get pods -o wide` 명령으로 확인할 수 있습니다). 이 README의 나머지 부분에서는 http://localhost:8080 기준으로 설명합니다.

### 01 - 기본 사용자 바꾸기

values/01-user-values.yaml에서 다른 admin 사용자를 만듭니다. 다른 장들과 같은 로그인 정보를 쓰게 하면서, Airflow 배포 커스터마이징을 가볍게 맛보는 예제입니다.

```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --set apiServer.service.type=LoadBalancer -f /etc/helm/values/01-user-values.yaml
```

http://localhost:8080 에 airflow/airflow로 로그인한 뒤 http://localhost:8080/users/userinfo/ 에서 바뀐 값을 보면 Admin 사용자가 바뀌었음을 확인할 수 있습니다.

### 02 - 웹서버 시크릿 제공하기

values/02-apiserversecret-values.yaml에서 자체 시크릿을 제공해, 정적이지 않은 시크릿을 쓴다는 배포 경고를 없앱니다.

```bash
kubectl create secret generic my-apiserver-secret --namespace airflow --from-literal="api-secret-key=$(python3 -c 'import secrets; print(secrets.token_hex(16))')"
```

helm 차트 1.18 버전에서는 아직 웹서버 시크릿도 필요합니다.

```bash
kubectl create secret generic my-webserver-secret --namespace airflow --from-literal="webserver-secret-key=$(python3 -c 'import secrets; print(secrets.token_hex(16))')"
```

```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer -f /etc/helm/values/02-apiserversecret-values.yaml
```

### 03 - 외부 데이터베이스 사용하기

values/03-external-database-values.yaml에서 외부 데이터베이스를 쓰도록 배포를 구성합니다. 이 데이터베이스는 docker compose 파일에 이미 마련되어 있습니다. 연결 정보는 이번에도 kubernetes 시크릿으로 helm 차트에 전달합니다.

```bash
kubectl create secret generic mydatabase --namespace airflow --from-literal=connection=postgresql://airflow:airflow@postgres:5432/airflow
```

```bash
/enable-external-dns # 다른 docker 서비스들이 k3s 클러스터 안에서 접근되도록 한다

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer -f /etc/helm/values/03-external-database-values.yaml
```

```bash
kubectl delete statefulset airflow-postgresql --namespace airflow
```

http://localhost:8080 에 airflow/airflow로 로그인해 확인할 수 있습니다. (원래의 admin/admin 사용자는 더 이상 없습니다)

### 04 - DAG 배포 옵션

#### 04a - DAG를 airflow 이미지에 굽기

values/04-dags-in-image-values.yaml에서 커스텀 컨테이너 이미지를 쓰도록 배포를 구성합니다. 이 이미지에는 빌드할 때 추가한 dag 파일이 들어 있습니다. 이미지는 (docker compose에 마련된) 레지스트리에 푸시해 두었으므로 helm 배포가 끌어올 수 있습니다.

```bash
# 로컬 머신에서
./publish-custom-images.sh
```

```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer -f /etc/helm/values/04-dags-in-image-values.yaml
```

이제 http://localhost:8080 에 airflow/airflow로 로그인하면 `01_dag_in_image` dag가 보입니다.

#### 04b - 퍼시스턴트 볼륨의 DAG

values/04-dags-in-persistent-vol-values.yaml에서 퍼시스턴트 볼륨을 쓰도록 배포를 구성합니다. 이 볼륨에 dag 파일이 담기고 모든 airflow 서비스가 이 볼륨을 사용합니다.

먼저 퍼시스턴트 볼륨과 볼륨 클레임을 만듭니다.

```bash
kubectl -n airflow apply -f /etc/helm/values/dag-pvc.yaml
```

그다음 이 퍼시스턴트 볼륨을 쓰도록 배포를 갱신합니다.

```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer -f /etc/helm/values/04-dags-in-persistent-vol-values.yaml
```

이제 http://localhost:8080 에 airflow/airflow로 로그인하면 `02_teamA_dag_from_pvc` 와 `02_teamB_dag_from_pvc` dag가 보입니다.

#### 04c - git 저장소의 DAG

values/04-dags-in-git-values.yaml에서 git 저장소의 dag를 동기화하는 git sync 사이드카 컨테이너를 쓰도록 배포를 구성합니다. 이 예제에서는 chapter02의 dag를 사용합니다.

다음처럼 배포를 갱신합니다.

```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer -f /etc/helm/values/04-dags-in-git-values.yaml
```

이제 http://localhost:8080 에 airflow/airflow로 로그인하면 `02_teamA_dag_from_pvc` 와 `02_teamB_dag_from_pvc` dag가 보입니다.

### 05 - DAG 의존성 (파이썬 라이브러리 설치)

#### 05a - 의존성을 airflow 이미지에 굽기

values/05-dependencies-in-image-values.yaml에서 커스텀 컨테이너 이미지를 쓰도록 배포를 구성합니다. 이 이미지에는 빌드할 때 추가한 dag 의존성 라이브러리가 들어 있습니다. 이미지는 (docker compose에 마련된) 레지스트리에 푸시해 두었으므로 helm 배포가 끌어올 수 있습니다.

```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer -f /etc/helm/values/05-dependencies-in-image-values.yaml
```

이제 http://localhost:8080 에 airflow/airflow로 로그인하면 `01_dag_dependencies_in_image` dag가 보입니다. version 태스크가 성공하고 로그에 tensorflow 버전이 찍혀야 합니다.

### 06 - 익스큐터

Airflow는 사용할 익스큐터를 구성하게 해 줍니다. helm 차트의 기본값은 CeleryExecutor입니다. 여기서는 KubernetesExecutor를 추가해 다중 익스큐터를 구성합니다. 구성 방법을 보여 줄 뿐 아니라, KubernetesExecutor로 DAG의 태스크마다 다른 이미지를 쓰는 방법도 설명할 수 있게 됩니다.

values/06-multiple-executors-values.yaml에서 CeleryExecutor와 KubernetesExecutor를 함께 쓰도록 구성하고, pod_template_file 구성으로 KubernetesExecutor의 기본 이미지를 지정합니다.
DAG에서는 pod_override 메커니즘으로 태스크의 k8s 파드를 더 세밀하게 구성합니다.

```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --set apiServer.service.type=LoadBalancer -f /etc/helm/values/06-multiple-executors-values.yaml
```
