import os
import time
import logging

from flask import Flask
from flask_restx import Api
from influxdb import InfluxDBClient
from flask_cors import CORS
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# loading default env values from the .env file
load_dotenv()

# Flask App initialization stuff
app = Flask(__name__)
api = Api(
    app, version="1.0", title="Location API", description="A simple geolocation API"
)

# Influx DB handle
db_connection_args = {
    "host": os.getenv("INFLUXDB_HOST", "influxdb"),
    "port": os.getenv("INFLUXDB_PORT", 8086),
    "username": os.getenv("INFLUXDB_USERNAME", "root"),
    "password": os.getenv("INFLUXDB_PASSWORD", "root"),
    "database": os.getenv("INFLUXDB_DATABASE", "monitor"),
}
db = None

# TODO: Check if CORS is really necessary
CORS(
    app=app,
    origins="*",
    expose_headers=None,
    allow_headers="*",
    max_age=None,
    send_wildcard=False,
    vary_header=True,
)


def wait_for_db():
    global db

    while True:
        try:
            db = InfluxDBClient(**db_connection_args)
            version = db.ping()
            if version:
                logging.info("Connection to database established")
                return
        except:
            pass
        logging.warning("Failed to connect to database")
        time.sleep(1)


def start():
    wait_for_db()

    import api.models
    import api.endpoints

    db.create_database(os.getenv("INFLUXDB_DATABASE", "monitor"))


start()
