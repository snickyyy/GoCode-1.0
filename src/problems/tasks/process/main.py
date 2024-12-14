import importlib
import json
from time import sleep

import redis


def main():
    """will work in a container for running tests"""
    redis_cliend = redis.Redis(host="redis", port=6379, db=0)
    while True:
        sleep(1)
        data = redis_cliend.rpop("data")
        if data is not None:
            data = json.loads(data)
            pk = data["pk"]
            try:
                compiled_code = compile(data.get("code"), "<string>", "exec")
            except Exception as e:
                result = {
                    "status": False,
                    "failures": str(e),
                    "successful_tests": 0
                }
                redis_cliend.hset("results", data["pk"], json.dumps(result))
                redis_cliend.srem("pks", data.get("pk"))
                continue
            namespase = {}
            exec(compiled_code, {}, namespase)
            test_case = importlib.import_module(f"data_tests.{data.get("test_name").replace(".py", "")}").TestCase(namespase.get("two_sum"))
            result = test_case.run_tests(namespase.get("two_sum"))
            redis_cliend.hset("results", pk, json.dumps(result))
            redis_cliend.srem("pks", data.get("pk"))


if __name__ == "__main__":
    main()
