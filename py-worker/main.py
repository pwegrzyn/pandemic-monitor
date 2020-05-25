import logging
import os
import time

from dotenv import load_dotenv

from lib.queue import RedisQueue
from lib.worker import PyWorker

# TODO: A good idea would be to eventually migrate to a Celery worker setup

# loading default env values from the .env file
load_dotenv()


def listen_for_jobs():
    queue = RedisQueue(
        host=os.getenv("REDIS_HOST", "queue"),
        port=os.getenv("REDIS_PORT", 6379),
        db_id=os.getenv("REDIS_DB_ID", 0),
        namespace=os.getenv("REDIS_NAMESPACE", "worker"),
        collection=os.getenv("REDIS_COLLECTION", "jobs"),
    )
    worker = PyWorker()

    logging.info("Starting to listen for jobs...")

    while True:
        try:
            job = queue.get_job(blocking=True)
            worker.execute(job)
        except Exception as e:
            logging.warning(f"Got an exception while listening for jobs:\n {e}")
            time.sleep(1)


if __name__ == "__main__":
    listen_for_jobs()
