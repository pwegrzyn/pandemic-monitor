from dataclasses import dataclass
from uwsgi_file_app import db, bcrypt
import enum
import jwt
import datetime
import os

secret = os.environ["SECRET"]

@dataclass
class PrivilegedUser(db.Model):
    __tablename__ = 'privileged_users'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String())
    surname: str = db.Column(db.String())
    email: str = db.Column(db.String())
    pass_hash: str = db.Column(db.String())

    def __init__(self, email, password):
        self.name = ""
        self.surname = ""
        self.email = email
        self.pass_hash = bcrypt.generate_password_hash(password).decode("utf8")

    @staticmethod
    def encode_auth_token(email):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': email
            }
            return jwt.encode(payload, secret, algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, secret)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature expired"
        except jwt.InvalidTokenError:
            return "Invalid token"


@dataclass
class NormalUser(db.Model):
    __tablename__ = "normal_users"

    id: int = db.Column(db.Integer, primary_key=True)
    user_api_id: int = db.Column(db.Integer)
    name: str = db.Column(db.String())
    surname: str = db.Column(db.String())

    def __init__(self, user_api_id, name, surname):
        self.user_api_id = user_api_id
        self.name = name
        self.surname = surname


class TestStages(enum.Enum):
    user_checked_in: int = 1
    test_started: int = 2
    test_result_negative: int = 3
    test_result_positive: int = 4




