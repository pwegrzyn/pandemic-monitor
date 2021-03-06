from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_utils
import os
import time
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# loading default env values from the .env file
load_dotenv()

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
database = os.environ["POSTGRES_DB"]
port = os.environ["POSTGRES_PORT"]
CONNECT_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = CONNECT_STRING
db = SQLAlchemy(app)


def wait_for_db():
    while True:
        try:
            result = sqlalchemy_utils.database_exists(CONNECT_STRING)
            if result:
                print("Connection to database established")
                return
        except:
            pass
        print("Failed to connect to database")
        time.sleep(1)


def start():
    import models
    import routes

    wait_for_db()

    db.create_all()
    db.session.commit()


start()
