import json, os
from flask import Flask, request, Response, make_response
import requests

app = Flask(__name__)
app.config['DEBUG'] = True

def cors_response(data):
    response = make_response(data)
    if 'Origin' in request.headers:
        origin = request.headers['Origin']
        response.headers['Access-Control-Allow-Origin'] = origin
    return response

@app.route("/")
def index():
    return "Hello Api"


@app.route("/dataportal/v1/portals.json")
def businesses():
    lat = request.args.get("lat", "")
    lon = request.args.get("lon", "")


    carto_db_url = "http://cfa.cartodb.com/api/v2/sql"
    params = {"q":"SELECT name, geo_id FROM all_census_places WHERE ST_CONTAINS(the_geom, ST_SetSRID(ST_Point(%s, %s),4326));" % (lat, lon)}

    # Get lookup the county / state / etc by lat lng from cartodb

    places = requests.get(carto_db_url, params=params)

    geo_id = places.json()["rows"][0]["geo_id"]
    name = places.json()["rows"][0]["name"]

    f =open("data/portals.json")
    contents = f.read()

    portals = json.loads(contents)
    portal = portals['admin'][geo_id]

    # lookup county / state in portal list

    res = {"portal_url":portal, "geo_id":geo_id, "name":name}

    return cors_response(Response(json.dumps(res), mimetype='application/json'))




if __name__ == "__main__":
    app.run()
