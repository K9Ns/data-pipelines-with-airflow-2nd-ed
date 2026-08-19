# chapter07 (번역서 6장)

『[Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)』 번역서 6장의 예제 코드입니다.

## 구성

이 폴더에는 워크플로 트리거(센서, DAG 실행 구성, 메시지 큐 트리거) 예제 DAG가 들어 있습니다.

## 사용법

다음 명령으로 Docker Compose에서 Airflow를 시작합니다.

```bash
docker compose up -d
```

초기화에 몇 초 걸리니 잠시 기다리면 http://localhost:8080 에서 Airflow 웹 UI에 접근할 수 있습니다.

예제 실행을 멈추려면 다음 명령을 실행합니다.

```bash
docker compose down -v
```

파일로 트리거되는 DAG(`02_wait_for_supermarket_1`, `03_file_sensor_example`, `04_PythonSensor_example`, `05_PythonSensor_example`, `06_Sensor_deadlock`, `08_reschedule_mode_example` 등)를 시험하려면 몇 단계를 거쳐야 합니다.

1. api server 컨테이너에 접속합니다.
   ```bash
   docker exec -it chapter07-api-server-1 /bin/bash
   ```
2. 데이터 디렉터리를 만듭니다.
    ```bash
    mkdir -p /data/supermarket1 &&
    mkdir -p /data/supermarket2 &&
    mkdir -p /data/supermarket3 &&
    mkdir -p /data/supermarket4
    ```
3. 테스트 파일을 만듭니다.
    ```bash
    touch /data/supermarket1/data-1.csv
    touch /data/supermarket2/data-1.csv
    touch /data/supermarket3/data-1.csv
    touch /data/supermarket4/data-1.csv

    touch /data/supermarket1/_SUCCESS
    touch /data/supermarket2/_SUCCESS
    touch /data/supermarket3/_SUCCESS
    touch /data/supermarket4/_SUCCESS
    ```
4. 그러면 위 DAG들이 트리거됩니다. 참고로 모든 DAG에 모든 파일이 필요한 것은 아닙니다.

Kafka 예제 DAG를 실행하려면 다음을 따릅니다.

1. DAG를 켭니다.
2. Kafka 컨테이너에 접속합니다.
   ```bash
   docker exec -it chapter07-kafka-1 /bin/bash
   ```
3. CLI 프로듀서를 실행합니다.
   ```bash
   /opt/kafka/bin/kafka-console-producer.sh --topic events --bootstrap-server localhost:9092
   ```
   `>` 가 나타나면 메시지를 보냅니다. 그러면 `12_kafka_trigger` DAG가 트리거되어 실행됩니다.
