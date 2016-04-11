# -*- coding: utf-8 -*-
from geocoding.base import Base

from geocoding import IGeocode
from geocoding import IGeocodeReverse

class Bing(Base, IGeocode, IGeocodeReverse):

    def __init__(self, location, **kwargs):
        pass

    def coder(self, location):
        pass

    def coder_reverse(self, location):
        pass
