# -*- coding: utf-8 -*-
from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class GeocodingWidget(forms.TextInput):
    class Media:
        css = {
                'all': ('geode_geocoding/css/geocoding.css',)
            }
        js = ('geode_geocoding/js/geocoding.js','typeahead.js/dist/typeahead.bundle.min.js')

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        base_attrs = {
            'data-provide':'typeahead',
            'autocomplete':'off',
            'class':'form-control typeahead'
        }
        base_attrs.update(attrs)
        final_attrs = self.build_attrs(base_attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        url = reverse('AutocompleteAdresse')
        geocoding_html = """
         <input{} />
        """
        geocoding_js = """
        <script type="text/javascript">
            showadresse('%s', '%s');
        </script>
        """ % (url, id_)
        return format_html(mark_safe(geocoding_html), flatatt(final_attrs)) + geocoding_js
