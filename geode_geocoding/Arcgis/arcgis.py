# -*- coding: utf-8 -*-
from geode_geocoding.base import Base

from geode_geocoding import IGeocode
from geode_geocoding import IGeocodeReverse

class Arcgis(Base, IGeocode, IGeocodeReverse):

    def __init__(self, location, **kwargs):
        pass

    def coder(self, location):
        pass

    def coder_reverse(self, location):
        pass
