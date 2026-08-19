import csv
import json
from pathlib import Path

from custom.json_to_csv_operator import JsonToCsvOperator


def test_json_to_csv_operator(tmp_path: Path):
    print(tmp_path.as_posix())

    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.csv"

    # 입력 데이터를 tmp 경로에 쓴다
    input_data = [
        {"name": "bob", "age": "41", "sex": "M"},
        {"name": "alice", "age": "24", "sex": "F"},
        {"name": "carol", "age": "60", "sex": "F"},
    ]
    with open(input_path, "w") as f:
        f.write(json.dumps(input_data))

    # 태스크 실행
    operator = JsonToCsvOperator(
        task_id="test", input_path=input_path, output_path=output_path
    )
    operator.execute(context={})

    # 결과 읽기
    with open(output_path) as f:
        reader = csv.DictReader(f)
        result = [dict(row) for row in reader]

    # 검증
    assert result == input_data
