from flask import jsonify, request
from flask_restx import Resource

from wsgi import api
from .models import LocationPoint


@api.route('/location')
class GeoLocation(Resource):
    """Represents the location endpoint"""

    def post(self):
        pass

    def put(self):
        pass

    def get(self):
        pass
