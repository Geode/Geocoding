# -*- coding: utf-8 -*-
from geocoding.base import Base

from geocoding import IGeocode
from geocoding import IGeocodeReverse

MY_PARAMS = {
    'format': "jsonv2",
    'polygon_geojson': 1,
}

class Osm(Base, IGeocode, IGeocodeReverse):

    def coder(self, location, **kwargs):
        self.provider = 'osm'
        self.method = 'geocode'
        self.url = self._get_osm_url(kwargs.get('url', ''))
        self.location = location
        self.params = {
            'q': location,
            'addressdetails': 1,
            'format': kwargs.get('format', MY_PARAMS.get('format')),
            'polygon_geojson': kwargs.get('polygon_geojson', MY_PARAMS.get('polygon_geojson')),
            'limit': kwargs.get('limit', 1),
        }
        self._initialize(**kwargs)

    def coder_reverse(self, location, **kwargs):
        self.provider = 'osm'
        self.method = 'reverse'
        self.url = self._get_osm_url_reverse(kwargs.get('url', ''))
        self.location = location
        self.params = {
            'lat': str(location[0]),
            'lon': str(location[1]),
            'addressdetails': 1,
            'format': kwargs.get('format', MY_PARAMS.get('format')),
            'limit': kwargs.get('limit', 1)
        }
        self._initialize(**kwargs)

    def _exceptions(self):
        if self.content:
            if isinstance(self.content, dict):
                self.content = [self.content]
            self._build_tree(self.content[0])

    def __iter__(self):
        for item in self.content:
            yield item

    def _get_osm_url(self, url):
        if url.lower() == 'localhost':
            return 'http://localhost/nominatim/search.php?'
        elif url:
            return url
        else:
            return 'https://nominatim.openstreetmap.org/search.php?'

    def _get_osm_url_reverse(self, url):
        if url.lower() == 'localhost':
            return 'http://localhost/nominatim/reverse.php?'
        elif url:
            return url
        else:
            return 'https://nominatim.openstreetmap.org/reverse.php?'

    @property
    def lat(self):
        lat = self.parse.get('lat')
        if lat:
            return float(lat)

    @property
    def lng(self):
        lng = self.parse.get('lon')
        if lng:
            return float(lng)

    @property
    def bbox(self):
        if self.parse['boundingbox']:
            south = float(self.parse['boundingbox'][0])
            west = float(self.parse['boundingbox'][2])
            north = float(self.parse['boundingbox'][1])
            east = float(self.parse['boundingbox'][3])
            return self._get_bbox(south, west, north, east)

    @property
    def geojson(self):
        #en cas de reverse, il n'y a pas de geojson retourner.
        if self.parse['geojson']:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": self.parse['geojson']['type'],
                    "coordinates": self.parse['geojson']['coordinates']
                },
            }
            return feature
        else:
            feature = {
                'type': 'Feature',
                'properties': self.json,
            }
            if self.bbox:
                feature['bbox'] = [self.west, self.south, self.east, self.north]
                feature['properties']['bbox'] = feature['bbox']
            if self.geometry:
                feature['geometry'] = self.geometry
            return feature


    @property
    def housenumber(self):
        return self.parse['address'].get('house_number')

    @property
    def street(self):
        return self.parse['address'].get('road')

    @property
    def neighbourhood(self):
        return self.parse['address'].get('neighbourhood')

    @property
    def city(self):
        return self.parse['address'].get('city')

    @property
    def postal(self):
        return self.parse['address'].get('postcode')

    @property
    def county(self):
        return self.parse['address'].get('county')

    @property
    def state(self):
        return self.parse['address'].get('state')

    @property
    def country(self):
        return self.parse['address'].get('country')

    @property
    def country_code(self):
        return self.parse['address'].get('country_code')
