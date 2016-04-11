# -*- coding: utf-8 -*-
from geocoding.base import Base

from geocoding import IGeocode
from geocoding import IGeocodeReverse

from geocoding.keys import google_key, google_client, google_client_secret

class Google(Base, IGeocode, IGeocodeReverse):

    def coder(self, location, **kwargs):
        self.provider = 'google'
        self.method = 'geocode'
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.location = location
        self.client = kwargs.get('client', google_client)
        self.client_secret = kwargs.get('client_secret', google_client_secret)
        self.params = {
            'address': location,
            'key': None if self.client and self.client_secret else kwargs.get('key', google_key),
            'client': self.client,
            'bounds': kwargs.get('bounds', ''),
            'language': kwargs.get('bounds ', ''),
            'region': kwargs.get('region', ''),
            'components': kwargs.get('components', ''),
        }
        self._initialize(**kwargs)

    def coder_reverse(self, location, **kwargs):
        self.provider = 'google'
        self.method = 'reverse'
        #https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.location = location
        self.short_name = kwargs.get('short_name', True)
        self.params = {
            'sensor': 'false',
            'latlng': '{0}, {1}'.format(location[0], location[1]),
            'key': kwargs.get('key', google_key),
            'language': kwargs.get('language', ''),
            'client': kwargs.get('client', google_client)
        }
        self._initialize(**kwargs)

    def _catch_errors(self):
        status = self.parse.get('status')
        if not status == 'OK':
            self.error = status

    def _exceptions(self):
        # Build intial Tree with results
        if self.parse['results']:
            self._build_tree(self.parse.get('results')[0])

            # Build Geometry
            self._build_tree(self.parse.get('geometry'))

            # Parse address components with short & long names
            for item in self.parse['address_components']:
                for category in item['types']:
                    self.parse[category]['long_name'] = item['long_name']
                    self.parse[category]['short_name'] = item['short_name']

    @property
    def ok(self):
        if self.method == 'geocode':
            return bool(self.lng and self.lat)
        elif self.method == 'reverse':
            return bool(self.address)
        else:
            return False

    @property
    def lat(self):
        return self.parse['location'].get('lat')

    @property
    def lng(self):
        return self.parse['location'].get('lng')

    @property
    def bbox(self):
        south = self.parse['southwest'].get('lat')
        west = self.parse['southwest'].get('lng')
        north = self.parse['northeast'].get('lat')
        east = self.parse['northeast'].get('lng')
        return self._get_bbox(south, west, north, east)

    @property
    def address(self):
        return self.parse.get('formatted_address')

    @property
    def housenumber(self):
        return self.parse['street_number'].get('short_name')

    @property
    def street(self):
        return self.parse['route'].get('long_name')

    @property
    def neighbourhood(self):
        return self.parse['neighborhood'].get('short_name')

    @property
    def city(self):
        return self.parse['locality'].get('long_name')

    @property
    def postal(self):
        return self.parse['postal_code'].get('long_name')

    @property
    def county(self):
        return self.parse['administrative_area_level_2'].get('long_name')

    @property
    def state(self):
        return self.parse['administrative_area_level_1'].get('long_name')

    @property
    def country(self):
        return self.parse['country'].get('long_name')

    @property
    def country_code(self):
        return self.parse['country'].get('short_name')
