import redis
import os


def client():
    return redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
