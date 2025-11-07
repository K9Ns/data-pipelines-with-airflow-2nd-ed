# Chapter 7

Code accompanying Chapter 7 of the book [Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow).

## Contents

This folder contains DAGs from Chapter 7.

## Usage

To get started with the code examples, start Airflow with Docker Compose with the following command:

```bash
docker compose up -d
```

The webserver initializes a few things, so wait for a few seconds, and you should be able to access the
Airflow webserver at http://localhost:8080.

To stop running the examples, run the following command:

```bash
docker compose down -v
```

To test the file triggered DAGs (e.g. `02_wait_for_supermarket_1`, `03_file_sensor_example`, `04_PythonSensor_example`, `05_PythonSensor_example`, `06_Sensor_deadlock`, `08_reschedule_mode_example`), you'll need to perform a few steps:
1. Bash into the api server container:
   ```bash
   docker exec -it chapter07-api-server-1 /bin/bash
   ```
2. Create the data directories: 
    ```bash
    mkdir -p /data/supermarket1 &&
    mkdir -p /data/supermarket2 &&
    mkdir -p /data/supermarket3 &&
    mkdir -p /data/supermarket4
    ```
3. Create the test files:
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
4. This will trigger the DAGs mentioned. Note: not all files will be needed for all of the DAGs mentioned.

To run the Kafka example DAG:
1. Turn the DAG on
2. Bash into the Kafka container:
   ```bash
   docker exec -it chapter07-kafka-1 /bin/bash
   ```
3. Run the CLI producer:
   ```bash
   /opt/kafka/bin/kafka-console-producer.sh --topic events --bootstrap-server localhost:9092
   ```
   Send a message when `>` appears. This will trigger the `12_kafka_trigger` DAG to run.
