# -*- coding: utf-8 -*-

from collections import defaultdict
import requests

class Base(object):
    _exclude = ['parse', 'json', 'url', 'fieldnames', 'help', 'debug',
                'short_name', 'api', 'content', 'params',
                'street_number', 'api_key', 'key', 'id', 'x', 'y',
                'latlng', 'headers', 'timeout', 'wkt', 'locality',
                'province', 'rate_limited_get', 'osm', 'route', 'schema',
                'properties', 'tree', 'error', 'proxies', 'road',
                'xy', 'northeast', 'northwest', 'southeast', 'southwest',
                'road_long', 'city_long', 'state_long', 'country_long',
                'postal_town_long', 'province_long', 'road_long',
                'street_long', 'interpolated', 'method', 'geometry',
                'coder','coder_reverse']
    fieldnames = []
    error = None
    status_code = None
    headers = {}
    params = {}
    provider = ''
    method = ''
    url = ''

    # Essential attributes for Quality Control
    lat = ''
    lng = ''
    accuracy = ''
    quality = ''
    confidence = ''

    # Bounding Box attributes
    northeast = []
    northwest = []
    southeast = []
    southwest = []
    bbox = {}


    def __repr__(self):
        if self.address:
            return "<[{0}] {1} - {2} [{3}]>".format(
                self.status,
                self.provider.title(),
                self.method.title(),
                self.address.title()
            )
        else:
            return "<[{0}] {1} - {2}>".format(
                self.status,
                self.provider.title(),
                self.method.title()
            )

    @staticmethod
    def rate_limited_get(url, **kwargs):
        return requests.get(url, **kwargs)

    def _get_api_key(self, base_key, **kwargs):
        key = kwargs.get('key', base_key)
        if not key:
            raise ValueError('Provide API Key')
        return key

    def _connect(self, **kwargs):
        self.status_code = 'Unknown'
        self.timeout = kwargs.get('timeout', 5.0)
        self.proxies = kwargs.get('proxies', '')
        try:
            r = self.rate_limited_get(
                self.url,
                params=self.params,
                headers=self.headers,
                timeout=self.timeout,
                proxies=self.proxies
            )
            self.status_code = r.status_code
            self.url = r.url
            if r.content:
                self.status_code = 200
        except (KeyboardInterrupt, SystemExit):
            raise
        except requests.exceptions.SSLError:
            self.status_code = 495
            self.error = 'ERROR - SSLError'
        except:
            self.status_code = 404
            self.error = 'ERROR - URL Connection'

        # Open JSON content from Request connection
        if self.status_code == 200:
            try:
                self.content = r.json()
            except:
                self.status_code = 400
                self.error = 'ERROR - JSON Corrupted'
                self.content = r.content

    def _initialize(self, **kwargs):
        # Remove extra URL from kwargs
        if 'url' in kwargs:
            kwargs.pop('url')
        self.json = {}
        self.parse = self.tree()
        self.content = None
        self.encoding = kwargs.get('encoding', 'utf-8')
        self._connect(url=self.url, params=self.params, **kwargs)
        try:
            for result in self.next():
                self._build_tree(result)
                self._exceptions()
                self._catch_errors()
                self._json()
        except:
            self._build_tree(self.content)
            self._exceptions()
            self._catch_errors()
            self._json()

    def _json(self):
        for key in dir(self):
            if not key.startswith('_') and key not in self._exclude:
                self.fieldnames.append(key)
                value = getattr(self, key)
                if value:
                    self.json[key] = value
        # Add OK attribute even if value is "False"
        self.json['ok'] = self.ok


    def _exceptions(self):
        pass

    def _catch_errors(self):
        pass

    def tree(self):
        return defaultdict(self.tree)

    def _build_tree(self, content, last=''):
        if content:
            if isinstance(content, dict):
                for key, value in content.items():
                    # Rebuild the tree if value is a dictionary
                    if isinstance(value, dict):
                        self._build_tree(value, last=key)
                    else:
                        if last:
                            self.parse[last][key] = value
                        else:
                            self.parse[key] = value

    @property
    def status(self):
        if self.ok:
            return 'OK'
        elif self.error:
            return self.error

        if self.status_code == 200:
            if not self.address:
                return 'ERROR - No results found'
            elif not (self.lng and self.lat):
                return 'ERROR - No Geometry'
        return 'ERROR - Unhandled Exception'

    def _get_bbox(self, south, west, north, east):
        # South Latitude, West Longitude, North Latitude, East Longitude
        self.south = south
        self.west = west
        self.north = north
        self.east = east

        # Bounding Box Corners
        self.northeast = [self.north, self.east]
        self.northwest = [self.north, self.west]
        self.southwest = [self.south, self.west]
        self.southeast = [self.south, self.east]

        # GeoJSON bbox
        self.westsouth = [self.west, self.south]
        self.eastnorth = [self.east, self.north]

        if all([self.south, self.east, self.north, self.west]):
            return dict(northeast=self.northeast, southwest=self.southwest)
        return {}

    @property
    def geojson(self):
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
    def wkt(self):
        if self.ok:
            return 'POINT({x} {y})'.format(x=self.x, y=self.y)
        return ''

    @property
    def xy(self):
        if self.ok:
            return [self.lng, self.lat]
        return []

    @property
    def latlng(self):
        if self.ok:
            return [self.lat, self.lng]
        return []

    @property
    def y(self):
        return self.lat

    @property
    def x(self):
        return self.lng

    @property
    def address(self):
        return self.parse.get('display_name')

    @property
    def type(self):
        return self.parse.get('type')

    @property
    def geometry(self):
        if self.ok:
            return {
                'type': 'Point',
                'coordinates': [self.x, self.y]}
        return {}

    # address properties

    @property
    def housenumber(self):
        return self.parse['address'].get('house_number')

    @property
    def street(self):
        return self.parse['address'].get('road')

    @property
    def road(self):
        return self.parse['address'].get('road')

    @property
    def city(self):
        return self.parse['address'].get('city')

    @property
    def state(self):
        return self.parse['address'].get('state')

    @property
    def country(self):
        return self.parse['address'].get('country')

    @property
    def postal(self):
        return self.parse['address'].get('postcode')

    @property
    def ok(self):
        return bool(self.lng and self.lat)

class Parser(object):

    result = {  'error': '',
                'result': [
                    {'point': {'y': '', 'x': ''},
                     'address': {
                        'number': '',
                        'street': {
                            'id': '',
                            'name': '',
                            'municipality': '',
                            'postCode': ''}},
                    'extent': {'xmin': '', 'xmax': '', 'ymax': '', 'ymin': ''},
                    'language': '',
                    'score': ''}],
                'status': ''}




    url = ''
    query = ''
    option = {}

    def __init__(self, parser_url):
        self.url = parser_url

    def getAddresses(self, query):
        self.query = query
        r = requests.get(self.url)
        if r.status_code == 200:
            self.result = r.json()
            return self.result
        else:
            return {}
