import os, requests, xmltodict, json
from flask import Flask, request, Response, make_response, url_for

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
    return "Try out an API call. <br /> http://portalportal.herokuapp.com/portalportal/v1/portals.json?latitude=39.062&longitude=-94.548"

@app.route("/portalportal/v1/portals.json")
def portalportal():

    def get_coords():
        latitude = None
        longitude = None
        latitude = request.args.get("latitude", "")
        longitude = request.args.get("longitude", "")
        if not latitude or not longitude:
            return "Make sure to put in a latitude and logitude, like http://portalportal.herokuapp.com/portalportal/v1/portals.json?latitude=39.062&longitude=-94.548"
        return latitude, longitude

    latitude, longitude = get_coords()

    geonames_url = 'http://api.geonames.org/extendedFindNearby?lat='+latitude+'&lng='+longitude+'&username=ondrae'

    response = requests.get(geonames_url)
    geonames = xmltodict.parse(response.text)
    
    city_name = geonames['geonames']['address']['placename']
    county_name = geonames['geonames']['address']['adminName2']
    state_code = geonames['geonames']['address']['adminCode1']
    state_name = geonames['geonames']['address']['adminName1']
    country_code = geonames['geonames']['address']['countryCode']

    city_state = city_name + ', ' + state_name
    county_state = county_name + ', ' + state_name

    response = requests.get('https://raw.github.com/ondrae/portalportal/master/static/data/portals.json')
    portals = response.json()
    
    city_portal = portals['city'][city_state]
    county_portal = portals['county'][county_state]
    state_portal = portals['state'][state_name]
    country_portal = portals['country'][country_code]

    res = {}
    res["country"] = {"name" : country_code, "data_portal_url" : country_portal}
    res["state"] = {"name" : state_name, "data_portal_url" : state_portal}
    res["county"] = {"name" : county_name, "data_portal_url" : county_portal}
    res["city"] = {"name" : city_name, "data_portal_url" : city_portal}

    return cors_response(Response(json.dumps(res), mimetype='application/json'))

if __name__ == "__main__":
    app.run()
