import json
from flask import Flask, request, Response, make_response, url_for
from portalData import PortalData

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
    return "Try out an API call. <br /> http://portalportal.herokuapp.com/v1/portals.json?latitude=39.062&longitude=-94.548"

@app.route("/v1/portals.json")
def portalportal():
    latitude = request.args.get("latitude", "")
    longitude = request.args.get("longitude", "")

    portalData = PortalData(latitude, longitude)
    portalData.get_geonames()
    portalData.get_portals()
    portalData.build_response()

    return cors_response(Response(json.dumps(portalData.res), mimetype='application/json'))

if __name__ == "__main__":
    app.run()
