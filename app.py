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

@app.route("/portalportal/v1/portals.json")
def portalportal():
    lat = request.args.get("latitude", "")
    lon = request.args.get("longitude", "")

    carto_db_url = "http://cfa.cartodb.com/api/v2/sql"
    params = {"q":"SELECT name, state_name FROM all_census_places WHERE ST_CONTAINS(the_geom, ST_SetSRID(ST_Point(%s, %s),4326));" % (lon, lat)}

    places = requests.get(carto_db_url, params=params)

    state_name = places.json()["rows"][0]["state_name"]
    city_name = places.json()["rows"][0]["name"]
    city_state = city_name + ', ' + state_name

    f = open("data/portals.json").read()
    portals = json.loads(f)
    
    portal_url = portals['city'][city_state]
    res = {"portal_url": portal_url, "city": city_name, "state" : state_name}

    return cors_response(Response(json.dumps(res), mimetype='application/json'))

if __name__ == "__main__":
    app.run()
