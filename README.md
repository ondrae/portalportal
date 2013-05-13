Portal Portal
=========================

## <a name="about"></a>About

A data portal to find data portals. Plug in a point and find all the data portals that have data about that point. This is a Labs Friday project of Code for America. This means it was an expirement done in one day. Any other development pass that Friday means someone got excited about the idea and kept building on it.

#### Why does portalportal exist?

There are open data portals all over the place, with new ones coming online everyday. Portalportal is an attempt by Code for America to help developers find them.

### How to use

	Put in a latitude and longitude and get back a heirarchy of data portal urls.
	
	http://portalportal.herokuapp.com/v1/portals.json?latitude=37.80508&longitude=-122.273071

	You'll get back a json response like so:
	{
		county: {
			data_portal_url: "https://data.acgov.org/",
			name: "Alameda"
		},
		country: {
			data_portal_url: "http://www.data.gov",
			name: "US"
		},
		state: {
			data_portal_url: "http://data.ca.gov/",
			name: "California"
		},
		city: {
			data_portal_url: "https://data.oaklandnet.com/",
			name: "Oakland"
		}
	}

## <a name="contributing"></a>Contributing

* To add a link to a data portal:
** Clone this repo
** Add the link in the 'static/data/portals.json' file.
** Order it alphabetically if you please.