import logging

from flask import jsonify, request
from flask_restx import Resource, reqparse
import geohash

from wsgi import api
from .models import LocationPoint
from wsgi import db


logger = logging.getLogger(__name__)

post_reqparser = reqparse.RequestParser()
post_reqparser.add_argument(
    "latitude",
    type=float,
    location="json",
    required=True,
    help="Please provide the latitude -"
)
post_reqparser.add_argument(
    "longitude",
    type=float,
    location="json",
    required=True,
    help="Please provide the longitude -"
)
post_reqparser.add_argument(
    "timestamp",
    type=int,
    location="json",
    required=True,
    help="Please provide the Unix timestamp -"
)
post_reqparser.add_argument(
    "identifier",
    type=int,
    location="json",
    required=True,
    help="Please provide the User Identifier -"
)


@api.route('/location')
class GeoLocation(Resource):
    """Represents the location endpoint for a single location msg"""

    @api.expect(post_reqparser)
    def post(self):
        # TODO: check the authorization ID from headers
        args = post_reqparser.parse_args()

        json_body = [
            {
                "measurement": "user_locations",
                "tags": {
                    "user_id": args["identifier"],
                    "geohash": geohash.encode(args["latitude"], args["longitude"])
                },
                "time": args["timestamp"],
                "fields": {
                    "lat": args["latitude"],
                    "lng": args["longitude"],
                }
            }
        ]
        
        try:
            db.write_points(json_body)
        except Exception:
            api.abort(500, "Error while saving geolocation to Influx.")
        else:
            return {"msg": "ok"}, 201

    def get(self):
        pass


# TODO: check if necessary (and finish?)
@api.route('/location_batch')
class GeoLocationBatch(Resource):
    """Represents the location endpoint for batched location msgs"""

    def post(self):
        args = post_reqparser.parse_args()
        for loc in args:
            print(args)

    def put(self):
        pass

    def get(self):
        pass
