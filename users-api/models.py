from dataclasses import dataclass
from uwsgi_file_app import db

@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    status: str = db.Column(db.String())

    def __init__(self, status="healthy"):
        self.status = status
