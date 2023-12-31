import redis


class RedisConnection:

    @staticmethod
    def connection():
        redis_conn = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)
        return redis_conn
