# -*- coding: utf-8 -*-
import requests

from geode_geocoding.base import Parser

class BxlParser(Parser):

    def __init__(self, parser_url='http://service.gis.irisnet.be/urbis/Rest/Localize/getaddresses'):
        self.url = parser_url
        self.option = { 'language' : 'FR',
                        'address':''}

    def getAddresses(self, query):
        self.query = query
        self.option['address'] = query
        r = requests.get(self.url, params = self.option)
        if r.status_code == 200:
            self.result = r.json()
            return self.result
        else :
            return {}
