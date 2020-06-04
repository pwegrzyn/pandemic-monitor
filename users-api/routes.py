from flask import jsonify, request
from flask_restx import Resource
from uwsgi_file_app import api
from models import *

print("ROUTES IMPORT")

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
