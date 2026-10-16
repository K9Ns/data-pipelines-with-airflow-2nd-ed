#! /usr/bin/env python

import click
import requests


@click.command()
@click.argument("city", type=str)
@click.option(
    "--output_path",
    default=None,
    type=click.Path(dir_okay=False, writable=True),
    help="출력을 기록할 파일(선택).",
)
def fetch_weather(city, output_path):
    """wttr.in에서 일기 예보를 가져오는 CLI 애플리케이션."""

    response = requests.get(f"https://v2.wttr.in/{city}")
    response.raise_for_status()

    if output_path:
        with open(output_path, "wb") as file_:
            file_.write(response.content)
    else:
        print(response.content.decode())


if __name__ == "__main__":
    fetch_weather()
