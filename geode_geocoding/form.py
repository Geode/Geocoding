# -*- coding: utf-8 -*-
from django import forms
from django.utils.html import format_html
from django.core.urlresolvers import reverse

class GeocodingWidget(forms.TextInput):
    class Media:
        css = {
                'all': ('geode_geocoding/css/geocoding.css',)
            }
        js = ('geode_geocoding/js/geocoding.js','typeahead.js/dist/typeahead.bundle.min.js')

class GeocodingForm(forms.Form):
    address = forms.CharField(widget=GeocodingWidget(attrs={ 'class':'form-control typeahead','data-provide':'typeahead', 'autocomplete':'off'}))

    def render(self):
        url = reverse('AutocompleteAdresse')
        encapsulation = """
        <script type="text/javascript">
            showadresse("%s");
        </script>
        """ % (url)
        return format_html(encapsulation)
