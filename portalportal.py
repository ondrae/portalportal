import requests

lat = 
lng = 

r = requests.get('http://cfa.cartodb.com/api/v2/sql?q=SELECT name, geo_id FROM all_census_places WHERE ST_CONTAINS(the_geom, ST_SetSRID(ST_Point('+lng+' '+lat+'),4326));');
city_name = r.json()['rows'][0]['name']
geo_id = r.json()['rows'][0]['geo_id']

portalportal = {
	
	'geo_id' : 'open_data_portal_url',
	'1600000US3651000' : 'https://nycopendata.socrata.com/',
	'1600000US0667000' : 'http://www.datasf.org',
	'1600000US2938000' : 'http://data.kcmo.org',

}


print portalportal[geo_id]
