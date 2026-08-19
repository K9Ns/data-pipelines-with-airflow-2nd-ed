#!/usr/bin/env python

import json
import logging
from pathlib import Path

import click
import requests

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option(
    "--start_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    required=True,
    help="평점 시작 날짜.",
)
@click.option(
    "--end_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    required=True,
    help="평점 종료 날짜.",
)
@click.option(
    "--output_path",
    type=click.Path(dir_okay=False),
    required=True,
    help="출력 파일 경로.",
)
@click.option("--host", type=str, default="http://movielens:5000", help="Movielens API URL.")
@click.option(
    "--user",
    type=str,
    envvar="MOVIELENS_USER",
    required=True,
    help="Movielens API 사용자.",
)
@click.option(
    "--password",
    type=str,
    envvar="MOVIELENS_PASSWORD",
    required=True,
    help="Movielens API 비밀번호.",
)
@click.option("--batch_size", type=int, default=100, help="레코드 조회 배치 크기.")
def main(start_date, end_date, output_path, host, user, password, batch_size):
    """movielens API에서 영화 평점을 가져오는 CLI 스크립트."""

    # 세션 준비.
    session = requests.Session()
    session.auth = (user, password)

    # 평점 가져오기.
    logging.info("Fetching ratings from %s (user: %s)", host, user)

    ratings = list(
        _get_ratings(
            session=session,
            host=host,
            start_date=start_date,
            end_date=end_date,
            batch_size=batch_size,
        )
    )
    logging.info("Retrieved %d ratings!", len(ratings))

    # 출력 쓰기.
    output_path = Path(output_path)

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Writing to %s", output_path)
    with output_path.open("w") as file_:
        json.dump(ratings, file_)


def _get_ratings(session, host, start_date, end_date, batch_size=100):
    yield from _get_with_pagination(
        session=session,
        url=host + "/ratings",
        params={
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        },
        batch_size=batch_size,
    )


def _get_with_pagination(session, url, params, batch_size=100):
    """
    주어진 url/params로 get 요청을 보내 레코드를 가져온다.
    페이지네이션을 고려한다.
    """

    offset = 0
    total = None
    while total is None or offset < total:
        response = session.get(url, params={**params, **{"offset": offset, "limit": batch_size}})
        response.raise_for_status()
        response_json = response.json()

        yield from response_json["result"]

        offset += batch_size
        total = response_json["total"]


if __name__ == "__main__":
    main()
