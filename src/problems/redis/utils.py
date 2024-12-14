import json

import redis
from django.conf import settings

redis_client = redis.Redis(settings.REDIS.get("HOST"), settings.REDIS.get("PORT"), settings.REDIS.get("DB"))


def add_in_queue(data, user_pk):
    redis_client.lpush(settings.REDIS["NAMESPACE"].get("QUEUE_INPUT"), data)
    redis_client.sadd(settings.REDIS["NAMESPACE"].get("QUEUE_PK"), user_pk)


def wait_and_get_result(key):
    while True:
        result = redis_client.hget(settings.REDIS["NAMESPACE"].get("QUEUE_RESULT"), key)
        if result is not None:
            result = json.loads(result)
            if result["failures"]:
                result["failures"] = result["failures"].replace(r"\n", "<br>")
            redis_client.hdel(settings.REDIS["NAMESPACE"].get("QUEUE_RESULT"), key)
            return result


def check_user_in_queue(pk):
    return redis_client.sismember(settings.REDIS["NAMESPACE"].get("QUEUE_PK"), pk)
