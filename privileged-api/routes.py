from flask import jsonify, request
from flask_restx import Resource, abort
from uwsgi_file_app import api, db
from models import *
import requests

@api.route('/auth/register')
class UserRegistration(Resource):

    def post(self):
        post_data = request.get_json()
        user = PrivilegedUser.query.filter_by(email=post_data.get('email')).first()

        if not user:
            try:
                new_user = PrivilegedUser(post_data.get('email'), post_data.get('password'))

                db.session.add(new_user)
                db.session.commit()
                auth_token = PrivilegedUser.encode_auth_token(new_user.id)
                response = {
                    "message": "Successfully registered",
                    "status": "success",
                    "auth_token": auth_token.decode()
                }
                return response

            except Exception as e:
                return {"message": "Error occurred", "status": "fail"}, 401
        else:
            return {"message": "User already registered", "status": "fail"}, 202


@api.route('/auth/login')
class UserLogin(Resource):

    def post(self):
        post_data = request.get_json()
        try:
            user = PrivilegedUser.query.filter_by(email=post_data.get('email')).first()
            if user:
                if bcrypt.check_password_hash(user.pass_hash, post_data.get('password')):

                    auth_token = PrivilegedUser.encode_auth_token(user.id)
                    if auth_token:
                        response = {
                            'status': 'success',
                            'message': 'Successfully logged in',
                            'auth_token': auth_token.decode()
                        }
                        return response
                else:
                    return {"message": "Invalid password", "status": "fail"}, 401

            else:
                return {"message": "User does not exist", "status": "fail"}, 404

        except Exception as e:
            return {"message": "Login failed", "status": "fail"}, 500


@api.route('/privileged-users')
class PrivilegedUsers(Resource):

    def get(self):
        auth_token = request.headers.get('Authorization')

        if auth_token:
            resp = PrivilegedUser.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = PrivilegedUser.query.filter_by(id=resp).first()
                response = {
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "email": user.email,
                        "pass_hash": user.pass_hash
                    }
                }
                return response
            else:
                return {"message": resp, "status": "fail"}, 401
        else:
            return {"message": "Invalid token", "status": "fail"}, 401



@api.route('/normal-users')
class NormalUsers(Resource):

    def get(self):
        auth_token = request.headers.get('Authorization')

        if auth_token:
            resp = PrivilegedUser.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                users = NormalUser.query.all()
                return jsonify(users)
            else:
                return {"message": resp, "status": "fail"}, 401
        else:
            return {"message": "Invalid token", "status": "fail"}, 401



@api.route('/normal-user/<int:id>')
class NormalUser(Resource):

    def get(self, id):
        auth_token = request.headers.get('Authorization')

        if auth_token:
            resp = PrivilegedUser.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = NormalUser.query.filter_by(id=id).first()
                return jsonify(user)
            else:
                return {"message": resp, "status": "fail"}, 401
        else:
            return {"message": "Invalid token", "status": "fail"}, 401


    def put(self, user_api_id):
        auth_token = request.headers.get('Authorization')
        post_data = request.get_json()

        if auth_token:
            resp = PrivilegedUser.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                name = post_data["name"]
                surname = post_data["name"]
                user = NormalUser(user_api_id, name, surname)
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                return jsonify(user)
            else:
                return {"message": resp, "status": "fail"}, 401
        else:
            return {"message": "Invalid token", "status": "fail"}, 401

    def post(self, id):
        auth_token = request.headers.get('Authorization')
        post_data = request.get_json()

        if auth_token:
            resp = PrivilegedUser.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = NormalUser.query.filter_by(id=id).first()
                user_api_id = user.user_api_id
                if "status" in post_data.keys():
                    status = post_data["status"]
                    user.status = status
                    db.session.commit()
                    requests.post("users-api:5000/users/{user_api_id}".format(user_api_id=user_api_id), data={"status": status})
                return jsonify(user)
            else:
                return {"message": resp, "status": "fail"}, 401
        else:
            return {"message": "Invalid token", "status": "fail"}, 401