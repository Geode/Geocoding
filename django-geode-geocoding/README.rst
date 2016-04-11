=========
Geocoding
=========

Geocoding is a simple Django app to request infortmation from
different geosource.

Quick start
-----------

1. Add "geocoding" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'geocoding',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^geocoding/', include('geocoding.urls')),
