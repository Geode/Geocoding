# -*- coding: utf-8 -*-
from django import forms
from geode_geocoding.widgets import GeocodingWidget

class GeocodingForm(forms.Form):
    address = forms.CharField(widget=GeocodingWidget())
