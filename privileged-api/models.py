from app import db, bcrypt
import enum
import jwt
import datetime
import os

secret = os.environ["SECRET"]


class PrivilegedUser(db.Model):
    __tablename__ = "privileged_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    pass_hash = db.Column(db.String)

    def __init__(self, email, password):
        super().__init__()
        self.name = ""
        self.surname = ""
        self.email = email
        self.pass_hash = bcrypt.generate_password_hash(password).decode("utf8")

    @staticmethod
    def encode_auth_token(email):
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, seconds=60),
                "iat": datetime.datetime.utcnow(),
                "sub": email,
            }
            return jwt.encode(payload, secret, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, secret)
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired"
        except jwt.InvalidTokenError:
            return "Invalid token"


class NormalUser(db.Model):
    __tablename__ = "normal_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_api_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, user_api_id, name, surname, status="healthy"):
        super().__init__()
        self.user_api_id = user_api_id
        self.name = name
        self.surname = surname
        self.status = status


class TestStages(enum.Enum):
    user_checked_in: int = 1
    test_started: int = 2
    test_result_negative: int = 3
    test_result_positive: int = 4
