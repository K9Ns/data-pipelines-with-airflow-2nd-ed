# Movielens API

이 디렉터리에는 Movielens 데이터 세트용 API가 Docker 컨테이너로 들어 있습니다. Airflow DAG에서 소비할 예시 API로 사용합니다.

## 데이터

사용하는 데이터는 [여기](https://grouplens.org/datasets/movielens/)에서 받을 수 있는 공개 데이터 세트입니다. 이 구성을 만들다 보니, 이미지 시작 시점에 이 데이터를 실시간으로 내려받는 방식이 모두에게 안정적으로 동작하지는 않는다는 것이 드러났습니다(연결이 곧잘 끊겼습니다). 그래서 문제가 되지 않도록 데이터를 zip 파일로 이 저장소에 포함하기로 했습니다. 덕분에 Movielens API가 *항상* 뜨는 것이 보장되고, 덤으로 꽤 빨라졌습니다. 이 zip 파일이 `ml-2023-ratings.zip`입니다.

파일은 다음 명령으로 생성했습니다. 참고로 필요한 데이터 양을 줄이기 위해 특정 기간만 걸러 냈습니다.

```bash
curl -O http://files.grouplens.org/datasets/movielens/ml-latest.zip
unzip ml-latest.zip
cd ml-latest
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
```

그다음 대화형 파이썬 셸에서 다음을 실행해 2023년 데이터만 남깁니다.

```python
import pandas as pd
ratings = pd.read_csv("ratings.csv")
ts_parsed = pd.to_datetime(ratings["timestamp"], unit="s")
ratings = ratings.loc[(ts_parsed >= "2023-01-01") & (ts_parsed < "2023-12-31")]
ratings.to_csv("2023-ratings.csv", index=False)
```

마지막으로 데이터를 다시 zip으로 묶습니다.

```bash
zip -r ml-2023-ratings.zip ./2023-ratings.csv
```
