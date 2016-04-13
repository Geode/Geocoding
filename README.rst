=========
Geocoding
=========

Geocoding is a simple Django app to request infortmation from
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
