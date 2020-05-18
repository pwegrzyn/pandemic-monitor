import logging

import redis


class RedisQueue:
    """Interface to a redis instance acting as a job queue"""

    def __init__(self, host, port, db_id, namespace, collection):
        self._redis_instance = redis.Redis(host=host, port=port, db=db_id)
        self._locator = namespace + ":" + collection
        logging.info("Connection to Redis successfully established.")

    def get_job(self, blocking=True, timeout=None):
        popped_job = (
            self._redis_instance.blpop(self._locator, timeout=timeout)
            if blocking
            else self._redis_instance.lpop(self._locator)
        )
        logging.info("Popped new job to execute.")
        return popped_job[1] if popped_job else popped_job
