import json
import pickle
import logging
import datetime
import time
from datetime import timedelta

from geopy.distance import great_circle
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PyWorker:
    """
      Represents a Python process acting as worker (listening for jobs
      and executing them)
    """

    def __init__(self):
        logger.info("Worker has been started successfully.")

    def execute(self, job):
        parsed_job = self._parse_job(job)
        if parsed_job.get("type") == "scan_users_locations":
            self._execute_scan_users_locations(parsed_job["args"])
        else:
            raise ValueError(f"Got an unknown job type: {parsed_job.get('type')}")

    def _execute_scan_users_locations(self, args):
        users_id_range = args["user_id_range"]
        diagnozed_visited_regions = args["diagnozed_visited_regions"]
        diagnozed_uuid = int(args["diagnozed_uuid"])

        two_weeks_ago = datetime.date.today() - datetime.timedelta(14)
        from_unix_epoch_secs = int(two_weeks_ago.strftime("%s"))
        to_unix_epoch_secs = int(time.time())
        json_payload = {
            "from": from_unix_epoch_secs,
            "to": to_unix_epoch_secs,
            "unit": "seconds",
            "user_id": diagnozed_uuid,
            "region_prefixes_to_check": "".join(diagnozed_visited_regions),
        }
        diagonzed_patient_geolocation_data = requests.get(
            "http://location-api:5000/location", json=json_payload
        )
        if diagonzed_patient_geolocation_data.status_code != 200:
            logger.warning(
                f"Error while querying Location API for diagonzed pation geo data:\n{diagonzed_patient_geolocation_data}"
            )
            raise Exception("Error while querying Location API.")
        logger.info(f"Diagnozed patient geo data in Worker: {str(diagonzed_patient_geolocation_data.json())}")

        for user_influx_id in map(int, users_id_range):
            json_payload = {
                "from": from_unix_epoch_secs,
                "to": to_unix_epoch_secs,
                "unit": "seconds",
                "user_id": user_influx_id,
                "region_prefixes_to_check": "".join(diagnozed_visited_regions),
            }
            logger.info(f"JSON Payload for next checked user:\n{str(json_payload)}")
            next_user_geo_data = requests.get(
                "http://location-api:5000/location", json=json_payload
            )
            if next_user_geo_data.status_code != 200:
                logger.warning(
                    f"Error while querying Location API for next user geo data:\n{next_user_geo_data}"
                )
                raise Exception("Error while querying Location API.")
            logger.info(f"Checked user ({user_influx_id}) geo data in Worker: {str(next_user_geo_data.json())}")

            # Now we actually need to compare the geo-location time series to find out if the checked
            # user was potentially in contact with the diagonzed user
            # TODO: probably lots of ways to optimize this method...
            is_suspected = self._check_if_were_in_contact(
                diagonzed_patient_geolocation_data.json(), next_user_geo_data.json()
            )
            if is_suspected:
                # TODO: crap, currently theres no way to directly PUT (update) user's status knowing only his UUID from Influx...
                # Workaround: first make a query to find the Users API ID based on the Influx UUID
                user_data = requests.get(
                    f"http://users-api:5000/usersByUUID/{user_influx_id}"
                )
                if user_data.status_code != 200:
                    logger.warning(
                        f"Error while querying Users API for User data:\n{user_data}"
                    )
                    raise Exception("Error while querying Users API for User data.")
                users_api_id = user_data.json()["id"]
                status_change_payload = {"status": "suspected"}
                users_api_resp = requests.put(
                    f"http://users-api:5000/users/{users_api_id}",
                    json=status_change_payload,
                )
                if users_api_resp.status_code != 200:
                    logger.warning(
                        f"Error while changing User's status in Users API:\n{users_api_resp}"
                    )
                    raise Exception("Error while changing User's status in Users API.")
                logger.info(
                    "Sucesully changed the status of the suspect to 'suspected' in the Users API."
                )
            else:
                logger.info(f"User {user_influx_id} is not suspected.")

    def _check_if_were_close(self, diagnozed_coords, checked_coords):
        miles_threshold = 0.5
        calculated_miles_dist = great_circle(diagnozed_coords, checked_coords).miles
        logger.info(f"Calculated distance in miles: {calculated_miles_dist}")
        return calculated_miles_dist < miles_threshold

    def _check_if_were_in_contact(self, diagnozed_data, to_check_data):

        relevant_time_delta = timedelta(minutes=1)
        diagonzed_idx = 0
        to_check_idx = 0

        while True:
            if diagonzed_idx >= len(diagnozed_data) or to_check_idx >= len(
                to_check_data
            ):
                return False

            influx_dt_template = "%Y-%m-%dT%H:%M:%SZ"
            diagnozed_time = diagnozed_data[diagonzed_idx]["time"]
            if type(diagnozed_time) == str:
                diagnozed_time = datetime.datetime.strptime(diagnozed_time, influx_dt_template)
            checked_time = to_check_data[to_check_idx]["time"]
            if type(checked_time) == str:
                checked_time = datetime.datetime.strptime(checked_time, influx_dt_template)

            diagnozed_lat = diagnozed_data[diagonzed_idx]["lat"]
            diagnozed_lng = diagnozed_data[diagonzed_idx]["lng"]
            checked_lat = to_check_data[to_check_idx]["lat"]
            checked_lng = to_check_data[to_check_idx]["lng"]

            if diagnozed_time > checked_time:
                delta_to_check = diagnozed_time - checked_time
                to_check_idx += 1
            else:
                delta_to_check = checked_time - diagnozed_time
                diagonzed_idx += 1
            
            logger.info(f"Time delta to check in Worker: {str(delta_to_check)}")

            if delta_to_check < relevant_time_delta:
                if self._check_if_were_close(
                    (diagnozed_lat, diagnozed_lng), (checked_lat, checked_lng)
                ):
                    return True
                else:
                    logger.info("This time delta is not significant.")

    def _parse_job(self, job):
        try:
            if isinstance(job, str):
                logger.info("Parsing job as JSON")
                job = json.loads(job)
            elif isinstance(job, bytes):
                logger.info("Parsing job as Bytes")
                job = json.loads(job.decode("UTF-8"))
        except Exception as e:
            logger.warning(f"Error while parsing job:\n {e}")
            raise
        return job
