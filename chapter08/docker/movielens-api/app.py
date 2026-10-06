import os
import time

import pandas as pd
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

DEFAULT_ITEMS_PER_PAGE = 100


def _read_ratings(file_path):

    try:
        ratings = pd.read_csv(file_path)
        if ratings.empty:
            raise ValueError("The ratings DataFrame is empty.")
        return (
            ratings
            .sample(n=100000, random_state=0)
            .sort_values(by=["timestamp", "userId", "movieId"])
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except Exception as e:
        raise e


app = Flask(__name__)
app.config["ratings"] = _read_ratings("/ratings.csv")

auth = HTTPBasicAuth()
users = {os.environ["API_USER"]: generate_password_hash(os.environ["API_PASSWORD"])}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route("/")
def hello():
    return "Hello from the Movie Rating API!"


@app.route("/ratings")
@auth.login_required
def ratings():
    """
    movielens 데이터 세트의 평점을 반환한다.

    Parameters
    ----------
    start_date : str
        조회 시작 날짜(포함).
    end_date : str
        조회 종료 날짜(제외).
    offset : int
        데이터 반환을 시작할 오프셋(페이지네이션용).
    limit : int
        반환할 최대 레코드 수(페이지네이션용).
    """

    start_date_ts = _date_to_timestamp(request.args.get("start_date", None))
    end_date_ts = _date_to_timestamp(request.args.get("end_date", None))

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", DEFAULT_ITEMS_PER_PAGE))

    ratings_df = app.config.get("ratings")

    if start_date_ts:
        ratings_df = ratings_df.loc[ratings_df["timestamp"] >= start_date_ts]

    if end_date_ts:
        ratings_df = ratings_df.loc[ratings_df["timestamp"] < end_date_ts]

    subset = ratings_df.iloc[offset : offset + limit]

    return jsonify(
        {
            "result": subset.to_dict(orient="records"),
            "offset": offset,
            "limit": limit,
            "total": ratings_df.shape[0],
        }
    )


def _date_to_timestamp(date_str):
    if date_str is None:
        return None
    return int(time.mktime(time.strptime(date_str, "%Y-%m-%d")))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
