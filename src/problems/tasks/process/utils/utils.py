import json
import os


def clean_work():
    files = ["data.py", "two_sum.py"]
    for file in files:
        os.remove(os.path.join("process/work", file))


def make_result_to_json(result: list[dict], pk):
    with open(f"/GoCode/tasks/process/result/{pk}.json", mode="w", encoding="utf-8") as f:
        json.dump(result, f)
    return True
