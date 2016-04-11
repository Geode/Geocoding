# -*- coding: utf-8 -*-
from geocoding.OSM.osm import Osm
from geocoding.Arcgis.arcgis import Arcgis
from geocoding.Bing.bing import Bing
from geocoding.Google.google import Google
from geocoding.BXL.bxl import BxlParser

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
