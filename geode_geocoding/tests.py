# -*- coding: utf-8 -*-
from django.test import TestCase

from geode_geocoding.factories import GeocoderFactory, ParserFactory

from geode_geocoding.OSM.osm import Osm
from geode_geocoding.Google.google import Google

from geode_geocoding.BXL.bxl import BxlParser

class GeocoderTestCase(TestCase):

    def test_factories(self):
        facto = GeocoderFactory()
        osm = facto.createGeocoder('osm')
        self.assertEqual(type(osm), Osm)

        google = facto.createGeocoder('google')
        self.assertEqual(type(google), Google)

        parse = ParserFactory()
        bxl = parse.createParser('bxl')
        self.assertEqual(type(bxl), BxlParser)

    def test_bxl_encoding(self):
        parser = ParserFactory().createParser('bxl')
        data = parser.getAddresses("Avenue des héliotropes 2")
        self.assertEqual(data['result'][0]['address']['street']['name'], 'Avenue des Héliotropes')

    def test_osm_coder(self):
        facto = GeocoderFactory()

        osm_be = facto.createGeocoder('osm')
        osm_be.coder("Rue Chapelle des Clercs 3, Liège, 4000, Wallonie, Belgique")
        self.assertEqual(osm_be.ok, True)
        self.assertEqual(osm_be.city, 'Liège')
        self.assertEqual(osm_be.postal, '4000')
        self.assertEqual(osm_be.country_code, 'be')

        osm_usa = facto.createGeocoder('osm')
        osm_usa.coder("623 Broadway, New York, NY 10012, USA")
        self.assertEqual(osm_usa.ok, True)
        self.assertEqual(osm_usa.city, 'NYC')
        self.assertEqual(osm_usa.postal, '10012')
        self.assertEqual(osm_usa.country_code, 'us')

    def test_osm_coder_reverse(self):
        facto = GeocoderFactory()

        osm_be = facto.createGeocoder('osm')
        osm_be.coder_reverse([50.6435567, 5.5743504])
        self.assertEqual(osm_be.ok, True)
        self.assertEqual(osm_be.city, 'Liège')
        self.assertEqual(osm_be.postal, '4000')
        self.assertEqual(osm_be.country_code, 'be')

        osm_usa = facto.createGeocoder('osm')
        osm_usa.coder_reverse([40.7259395, -73.9965313])
        self.assertEqual(osm_usa.ok, True)
        self.assertEqual(osm_usa.city, 'NYC')
        self.assertEqual(osm_usa.postal, '10012')
        self.assertEqual(osm_usa.country_code, 'us')

    def test_google_coder(self):
        facto = GeocoderFactory()

        google_be = facto.createGeocoder('google')
        google_be.coder("Rue Chapelle des Clercs 3, Liège, 4000, Wallonie, Belgique")
        self.assertEqual(google_be.ok, True)
        self.assertEqual(google_be.city, 'Liège')
        self.assertEqual(google_be.postal, '4000')
        self.assertEqual(google_be.country_code, 'BE')

        google_usa = facto.createGeocoder('google')
        google_usa.coder("623 Broadway, New York, NY 10012, USA")
        self.assertEqual(google_usa.ok, True)
        self.assertEqual(google_usa.city, 'New York')
        self.assertEqual(google_usa.postal, '10012')
        self.assertEqual(google_usa.country_code, 'US')

    def test_google_coder_reverse(self):
        facto = GeocoderFactory()

        google_be = facto.createGeocoder('google')
        google_be.coder_reverse([50.6435567, 5.5743504])
        self.assertEqual(google_be.ok, True)
        self.assertEqual(google_be.city, 'Liège')
        self.assertEqual(google_be.postal, '4000')
        self.assertEqual(google_be.country_code, 'BE')

        google_usa = facto.createGeocoder('google')
        google_usa.coder_reverse([40.7259395, -73.9965313])
        self.assertEqual(google_usa.ok, True)
        self.assertEqual(google_usa.city, 'New York')
        self.assertEqual(google_usa.postal, '10012')
        self.assertEqual(google_usa.country_code, 'US')
