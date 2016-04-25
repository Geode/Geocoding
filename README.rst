=========
Geocoding
=========

Geocoding is a simple Django app to request information from
different geosource.

Quick start
-----------

1. Add "geode_geocoding" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'geode_geocoding',
    ]

2. Include the geode_geocoding URLconf in your project urls.py like this::
    url(r'^geode_geocoding/', include('geode_geocoding.urls')),

3. You must update the setting.py file by adding the various bower_install component.
    and run a 'python management bower_install'

4. A test page is present on URL/geode_geocoding/test
