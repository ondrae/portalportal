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

    class PortalData:

        def __init__(self, latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

        def get_geonames(self):
            geonames_url = 'http://api.geonames.org/extendedFindNearby?lat='+self.latitude+'&lng='+self.longitude+'&username=ondrae'
            response = requests.get(geonames_url)
            geonames = xmltodict.parse(response.text)
            self.city_name = geonames['geonames']['address']['placename']
            self.county_name = geonames['geonames']['address']['adminName2']
            self.state_code = geonames['geonames']['address']['adminCode1']
            self.state_name = geonames['geonames']['address']['adminName1']
            self.country_code = geonames['geonames']['address']['countryCode']

        def get_portals(self):
            self.city_state_country = self.city_name + ', ' + self.state_name + ', ' + self.country_code
            self.county_state_country = self.county_name + ', ' + self.state_name + ', ' + self.country_code
            response = requests.get('https://raw.github.com/ondrae/portalportal/testing/static/data/portals.json')
            portals = response.json()
            print portals
            self.city_portal = portals['city'][self.city_state_country]
            self.county_portal = portals['county'][self.county_state_country]
            self.state_portal = portals['state'][self.state_name]
            self.country_portal = portals['country'][self.country_code]

    latitude = request.args.get("latitude", "")
    longitude = request.args.get("longitude", "")

    portalData = PortalData(latitude, longitude)

    portalData.get_geonames()
    portalData.get_portals()

    return portalData.country_portal

    # def get_coords():
    #     latitude = None
    #     longitude = None
    #     latitude = request.args.get("latitude", "")
    #     longitude = request.args.get("longitude", "")
    #     print latitude, longitude
    #     return latitude, longitude

    # latitude, longitude = get_coords()
    # if not latitude or not longitude:
    #     return "Make sure to put in a latitude and logitude, like http://portalportal.herokuapp.com/portalportal/v1/portals.json?latitude=39.062&longitude=-94.548"

    # def get_geonames(latitude, longitude):
    #     geonames_url = 'http://api.geonames.org/extendedFindNearby?lat='+latitude+'&lng='+longitude+'&username=ondrae'
    #     response = requests.get(geonames_url)
    #     geonames = xmltodict.parse(response.text)
    #     print geonames
    #     city_name = geonames['geonames']['address']['placename']
    #     county_name = geonames['geonames']['address']['adminName2']
    #     state_code = geonames['geonames']['address']['adminCode1']
    #     state_name = geonames['geonames']['address']['adminName1']
    #     country_code = geonames['geonames']['address']['countryCode']
    #     return city_name, county_name, state_code, state_name, country_code

    # city_name, county_name, state_code, state_name, country_code = get_geonames(latitude, longitude)

    # def get_portals(city_name, county_name, state_code, state_name, country_code):
    #     city_state_country = city_name + ', ' + state_name + ', ' + country_code
    #     county_state_country = county_name + ', ' + state_name + ', ' + country_code
    #     response = requests.get('https://raw.github.com/ondrae/portalportal/master/static/data/portals.json')
    #     portals = response.json()
    #     print type(county_state_country)
    #     for i in
    #     city_portal = portals['city'][city_state_country]
    #     county_portal = portals['county'][county_state_country]
    #     state_portal = portals['state'][state_name]
    #     country_portal = portals['country'][country_code]
    #     return city_portal, county_portal, state_portal, country_portal

    # city_portal, county_portal, state_portal, country_portal = get_portals(city_name, county_name, state_code, state_name, country_code)

    # def build_response(city_name, county_name, state_code, state_name, country_code, city_portal, county_portal, state_portal, country_portal):
    #     res = {}
    #     res["country"] = {"name" : country_code, "data_portal_url" : country_portal}
    #     res["state"] = {"name" : state_name, "data_portal_url" : state_portal}
    #     res["county"] = {"name" : county_name, "data_portal_url" : county_portal}
    #     res["city"] = {"name" : city_name, "data_portal_url" : city_portal}
    #     return res

    # return cors_response(Response(json.dumps(res), mimetype='application/json'))

if __name__ == "__main__":
    app.run()
