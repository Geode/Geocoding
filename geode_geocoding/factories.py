# -*- coding: utf-8 -*-
from geode_geocoding.OSM.osm import Osm
from geode_geocoding.Arcgis.arcgis import Arcgis
from geode_geocoding.Bing.bing import Bing
from geode_geocoding.Google.google import Google
from geode_geocoding.BXL.bxl import BxlParser

geocodingTypesMapping = {
    'osm': Osm,
    'arcgis': Arcgis,
    'bing': Bing,
    'google': Google,
}

parserTypesMapping = {
    'bxl': BxlParser,
}

class GeocoderFactory:

    def createGeocoder(self, geocodingType):
        return geocodingTypesMapping.get(geocodingType)()

class ParserFactory:

    def createParser(self, parserType):
        return parserTypesMapping.get(parserType)()
