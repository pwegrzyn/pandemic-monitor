import logging

from flask import jsonify, request
from flask_restx import Resource, reqparse
import geohash

from wsgi import api
from .models import LocationPoint
from wsgi import db


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

post_reqparser = reqparse.RequestParser()
post_reqparser.add_argument(
    "latitude",
    type=float,
    location="json",
    required=True,
    help="Please provide the latitude -",
)
post_reqparser.add_argument(
    "longitude",
    type=float,
    location="json",
    required=True,
    help="Please provide the longitude -",
)
post_reqparser.add_argument(
    "timestamp",
    type=int,
    location="json",
    required=True,
    help="Please provide the Unix timestamp -",
)
post_reqparser.add_argument(
    "identifier",
    type=int,
    location="json",
    required=True,
    help="Please provide the User Identifier -",
)

get_regions_reqparser = reqparse.RequestParser()
get_regions_reqparser.add_argument(
    "from", type=int, location="args", required=True,
)
get_regions_reqparser.add_argument(
    "to", type=int, location="args", required=True,
)
get_regions_reqparser.add_argument(
    "unit", type=str, location="args", required=True,
)

get_locations_reqparser = reqparse.RequestParser()
get_locations_reqparser.add_argument(
    "from", type=int, location="json", required=True,
)
get_locations_reqparser.add_argument(
    "to", type=int, location="json", required=True,
)
get_locations_reqparser.add_argument(
    "unit", type=str, location="json", required=True,
)
get_locations_reqparser.add_argument(
    "user_id", type=int, location="json", required=True,
)
get_locations_reqparser.add_argument(
    "region_prefixes_to_check", type=str, location="json", required=True,
)


@api.route("/location")
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
                    "geohash": geohash.encode(args["latitude"], args["longitude"]),
                },
                "time": args["timestamp"],
                "fields": {"lat": args["latitude"], "lng": args["longitude"],},
            }
        ]

        try:
            db.write_points(json_body)
        except Exception:
            api.abort(500, "Error while saving geolocation to Influx.")
        else:
            return {"msg": "ok"}, 201

    def get(self):
        args = get_locations_reqparser.parse_args()

        # TODO refactor copy-pasted code
        if args["unit"] == "seconds":
            from_unix = args["from"] * 1_000_000_000
            to_unix = args["to"] * 1_000_000_000
        elif args["unit"] == "milliseconds":
            from_unix = args["from"] * 1_000_000
            to_unix = args["to"] * 1_000_000
        elif args["unit"] == "microseconds":
            from_unix = args["from"] * 1_000
            to_unix = args["to"] * 1_000
        elif args["unit"] == "nanoseconds":
            from_unix = args["from"]
            to_unix = args["to"]
        else:
            api.abort(
                400,
                "Unit needs to be either seconds, miliseconds, microseconds or nanoseconds.",
            )

        # At this point it turned out that in the current version Influx does not allow to use SUBSTR() in
        # the WHERE close in queries, so the whole optimization with geohash prefixes is kinda pointless for now...
        query = f"SELECT * FROM user_locations WHERE user_id = '{args['user_id']}' AND time >= {from_unix} AND time <= {to_unix};"

        try:
            result = db.query(query)
        except Exception as e:
            logger.warning(f"Error while querying Influx:\n {str(e)}")
            api.abort(500, "Error while querying Influx.")
        else:
            filtered_results = [
                p
                for p in result.get_points(measurement="user_locations")
                if p["geohash"][0] in args["region_prefixes_to_check"]
            ]
            final_result = [
                {"lat": p["lat"], "lng": p["lng"], "time": p["time"]}
                for p in filtered_results
            ]
            return final_result, 200


@api.route("/location_all")
class GeoLocationAll(Resource):
    def get(self):
        query = "SELECT * FROM user_locations;"

        try:
            result = db.query(query)
        except Exception as e:
            logger.warning(f"Error while querying Influx:\n {str(e)}")
            api.abort(500, "Error while querying Influx.")
        else:
            final_result = [
                {
                    "lat": p["lat"],
                    "lng": p["lng"],
                    "time": p["time"],
                    "user_id": p["user_id"],
                }
                for p in result.get_points(measurement="user_locations")
            ]
            print(final_result)
            return final_result, 200


@api.route("/users")
class InfluxRegisteredUsers(Resource):
    def get(self):
        # Can't use DISTINCT() on tags in Influx...
        query = "SELECT * FROM user_locations;"
        try:
            result = db.query(query)
        except Exception as e:
            logger.warning(f"Error while querying Influx:\n {str(e)}")
            api.abort(500, "Error while querying Influx.")
        else:
            all_users = [
                p["user_id"] for p in result.get_points(measurement="user_locations")
            ]
            all_users = list(set(all_users))
            return all_users, 200


@api.route("/geohashRegionsForUser/<int:user_id>")
class GeohashRegionsForUser(Resource):
    """
    Represents the list of geohash regions a user has been checked in 
    during a given time period. We define a geohash region as a prefix of
    the geohash - currently the first letter (about 2500 km).
    """

    def get(self, user_id):
        """
        For a given User and for a given time period return the list of Geohash regions
        this user has visited in this time
        """
        args = get_regions_reqparser.parse_args()

        if args["unit"] == "seconds":
            from_unix = args["from"] * 1_000_000_000
            to_unix = args["to"] * 1_000_000_000
        elif args["unit"] == "milliseconds":
            from_unix = args["from"] * 1_000_000
            to_unix = args["to"] * 1_000_000
        elif args["unit"] == "microseconds":
            from_unix = args["from"] * 1_000
            to_unix = args["to"] * 1_000
        elif args["unit"] == "nanoseconds":
            from_unix = args["from"]
            to_unix = args["to"]
        else:
            api.abort(
                400,
                "Unit needs to be either seconds, miliseconds, microseconds or nanoseconds.",
            )

        # InfluxQL does not support substrings in quries...
        query = f"SELECT * FROM user_locations WHERE user_id = '{user_id}' AND time >= {from_unix} AND time <= {to_unix};"
        try:
            result = db.query(query)
        except Exception as e:
            logger.warning(f"Error while querying Influx:\n {str(e)}")
            api.abort(500, "Error while querying Influx.")
        else:
            result_regions = [
                p["geohash"][0] for p in result.get_points(measurement="user_locations")
            ]
            return result_regions, 200


# TODO: check if necessary (and possibly finish?)
@api.route("/location_batch")
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
