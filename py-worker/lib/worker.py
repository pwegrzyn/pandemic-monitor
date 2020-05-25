import json
import pickle
import logging


class PyWorker:
    """
      Represents a Python process acting as worker (listening for jobs
      and executing them)
    """

    def __init__(self):
        logging.info("Worker has been started successfully.")

    def execute(self, job):
        parsed_job = self._parse_job(job)
        # TODO: execute the job
    
    def _parse_job(self, job):
        try:
            if isinstance(job, str):
                job = json.loads(job)
            elif isinstance(job, bytes):
                job = pickle.loads(job)
        except Exception as e:
            logging.warning(f"Error while parsing job:\n {e}")
            raise
        return job
