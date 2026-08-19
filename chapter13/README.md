# chapter13 (번역서 12장)

『[Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow-second-edition)』 번역서 12장의 예제 코드입니다.

이 사용 사례의 상당 부분은 https://toddwschneider.com/posts/taxi-vs-citi-bike-nyc 의 아이디어에 기반합니다. 주어진 시간대와 요일에 NYC의 두 동네 사이에서 가장 빠른 교통수단(Citi Bike 대 옐로 택시)이 무엇인지 판정하는 문제입니다. 이 사용 사례를 Airflow 워크플로로 프로덕션화합니다. 이를 위해 (모의) 실시간 서비스 둘을 만듭니다.

1. Citi Bike 운행 기록을 제공하는 서비스
1. NYC 옐로 택시 운행 기록을 제공하는 서비스

Airflow DAG가 이 서비스들을 주기적으로 긁어 데이터를 다듬고, 결과를 Postgres 데이터베이스로 보냅니다. 이 데이터베이스는 두 NYC 동네 사이에서 어떤 교통수단이 가장 빠른지 보여 주는 작은 웹사이트를 받칩니다.

실제 데이터는 월/년 단위 배치로만 제공됩니다. 그래서 "실시간" 시스템을 흉내 내는 API 둘을 마련했습니다. 이 저장소에 딸린 `compose.yaml`로 시스템을 띄울 수 있습니다.

```bash
docker compose up -d --build
```

처리가 잘 끝나면 최종 결과를 http://localhost:8083 에서 볼 수 있습니다.

서비스가 열리는 포트는 다음과 같습니다.

- http://localhost:5432: Airflow Postgres DB (`airflow`/`airflow`)
- http://localhost:5433: NYC 택시 Postgres DB (`taxi`/`ridetlc`)
- http://localhost:5434: Citi Bike Postgres DB (`citi`/`cycling`)
- http://localhost:5435: NYC 교통 결과 Postgres DB (`nyc`/`tr4N5p0RT4TI0N`)
- http://localhost:8080: Airflow 웹 UI (`airflow`/`airflow`)
- http://localhost:8081: NYC 택시 정적 파일 서버
- http://localhost:8082: Citi Bike API (`citibike`/`cycling`)
- http://localhost:8083: NYC 교통 API
- http://localhost:9000: MinIO (`AKIAIOSFODNN7EXAMPLE`/`wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)

## 더 알아보기

### 택시 데이터 세트

택시 데이터 세트는 "NYC Taxi and Limousine Commission (TLC) Trip Record Data"를 가리키며, https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page 에서 받을 수 있습니다.

데이터 일부는 다음과 같습니다.

```csv
VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge
1,2019-01-01 00:46:40,2019-01-01 00:53:20,1,1.50,1,N,151,239,1,7,0.5,0.5,1.65,0,0.3,9.95,
1,2019-01-01 00:59:47,2019-01-01 01:18:59,1,2.60,1,N,239,246,1,14,0.5,0.5,1,0,0.3,16.3,
2,2018-12-21 13:48:30,2018-12-21 13:52:40,3,.00,1,N,236,236,1,4.5,0.5,0.5,0,0,0.3,5.8,
2,2018-11-28 15:52:25,2018-11-28 15:55:45,5,.00,1,N,193,193,2,3.5,0.5,0.5,0,0,0.3,7.55,
2,2018-11-28 15:56:57,2018-11-28 15:58:33,5,.00,2,N,193,193,2,52,0,0.5,0,0,0.3,55.55,
2,2018-11-28 16:25:49,2018-11-28 16:28:26,5,.00,1,N,193,193,2,3.5,0.5,0.5,0,5.76,0.3,13.31,
2,2018-11-28 16:29:37,2018-11-28 16:33:43,5,.00,2,N,193,193,2,52,0,0.5,0,0,0.3,55.55,
1,2019-01-01 00:21:28,2019-01-01 00:28:37,1,1.30,1,N,163,229,1,6.5,0.5,0.5,1.25,0,0.3,9.05,
1,2019-01-01 00:32:01,2019-01-01 00:45:39,1,3.70,1,N,229,7,1,13.5,0.5,0.5,3.7,0,0.3,18.5,
```

데이터 사전: https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

### Citi Bike 데이터 세트

https://www.citibikenyc.com/system-data

데이터 일부는 다음과 같습니다.

```csv
"tripduration","starttime","stoptime","start station id","start station name","start station latitude","start station longitude","end station id","end station name","end station latitude","end station longitude","bikeid","usertype","birth year","gender"
201,"2019-01-01 03:09:09.7110","2019-01-01 03:12:30.8790",3183,"Exchange Place",40.7162469,-74.0334588,3214,"Essex Light Rail",40.7127742,-74.0364857,29612,"Subscriber",1993,1
505,"2019-01-01 05:18:00.1060","2019-01-01 05:26:25.9050",3183,"Exchange Place",40.7162469,-74.0334588,3638,"Washington St",40.7242941,-74.0354826,29213,"Subscriber",1972,2
756,"2019-01-01 10:36:33.3400","2019-01-01 10:49:10.2600",3183,"Exchange Place",40.7162469,-74.0334588,3192,"Liberty Light Rail",40.7112423,-74.0557013,26164,"Subscriber",1985,1
1575,"2019-01-01 12:43:38.6430","2019-01-01 13:09:54.5280",3183,"Exchange Place",40.7162469,-74.0334588,3638,"Washington St",40.7242941,-74.0354826,29672,"Customer",1969,0
1566,"2019-01-01 12:43:39.6010","2019-01-01 13:09:46.5100",3183,"Exchange Place",40.7162469,-74.0334588,3638,"Washington St",40.7242941,-74.0354826,29522,"Customer",1969,0
737,"2019-01-01 12:56:53.2040","2019-01-01 13:09:11.0400",3183,"Exchange Place",40.7162469,-74.0334588,3205,"JC Medical Center",40.71653978099194,-74.0496379137039,29447,"Subscriber",1993,1
917,"2019-01-01 13:03:44.7760","2019-01-01 13:19:02.7690",3183,"Exchange Place",40.7162469,-74.0334588,3277,"Communipaw & Berry Lane",40.71435836870427,-74.06661093235016,29299,"Subscriber",1986,1
3248,"2019-01-01 13:12:03.1280","2019-01-01 14:06:12.0400",3183,"Exchange Place",40.7162469,-74.0334588,3196,"Riverview Park",40.7443187,-74.0439909,29495,"Subscriber",1992,1
3168,"2019-01-01 13:13:12.0450","2019-01-01 14:06:00.4110",3183,"Exchange Place",40.7162469,-74.0334588,3196,"Riverview Park",40.7443187,-74.0439909,26312,"Customer",1969,0
```
