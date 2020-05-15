from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import sqlalchemy_utils
import os
import time

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
database = os.environ["POSTGRES_DB"]
port = os.environ["POSTGRES_PORT"]
CONNECT_STRING = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_STRING
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


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

if __name__ == 'uwsgi_file_app':
    import models
    import routes

    wait_for_db()

    db.create_all()
    db.session.commit()