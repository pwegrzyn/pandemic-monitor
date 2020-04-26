from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import os

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

@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    status: str = db.Column(db.String())

    def __init__(self, status="healthy"):
        self.status = status


@api.route('/users')
class Users(Resource):
    def put(self):
        new_user = User()
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        return jsonify(new_user)

    def get(self):
        return jsonify(User.query.all())


@api.route('/users/<int:id>')
class SingleUser(Resource):

    def get(self, id):
        return jsonify(User.query.filter_by(id=id).first())

    def post(self, id):
        user = User.query.filter_by(id=id).first()
        if "status" in request.form.keys(): user.status = request.form["status"]
        db.session.commit()
        return jsonify(user)

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify(user)


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(host="0.0.0.0", debug=True)
