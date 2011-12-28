"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User

from jazzchanges.tunes.models import (  Tune, Change, KEYS, EXTENDED_KEY_DICT, 
                                        TIMES, INTERVALS, REVERSE_EXTENSIONS_DICT,
                                        REVERSE_KEY_DICT, REVERSE_INTERVAL_DICT)


class TunesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')


    def test_basic_transposition(self):
        """
        Run through a bunch of general tests for transposing keys/intevals.
        """
        def build_change(interval, key):
            return Change(interval=REVERSE_INTERVAL_DICT[interval]).get_root(REVERSE_KEY_DICT[key])

        # generic I-IV-V
        self.assertEquals('G', build_change('I', 'G')) # tonic
        self.assertEquals('C', build_change('IV', 'G')) # subdominant
        self.assertEquals('D', build_change('V', 'G')) # dominant

        # a few random ones
        self.assertEquals('G', build_change('bIII', 'E')) # minor 3rd of E
        self.assertEquals('G', build_change('bII', 'Gb')) # flat 9th of Gb
        self.assertEquals('G', build_change('VII', 'Ab')) # major 7th of Ab

        # sample chord, lets say... A7
        self.assertEquals('A', build_change('I', 'A')) # root
        self.assertEquals('Db', build_change('III', 'A')) # major 3rd
        self.assertEquals('E', build_change('V', 'A')) # 5th
        self.assertEquals('G', build_change('bVII', 'A')) # dominant 7th


    def test_text_import_export(self):
        tune = Tune.objects.create(
            title = 'Sample Progression',
            artist = 'Sample Artist',
            key = REVERSE_KEY_DICT['C'], # 1
            time = '4/4',
            owner = self.user)
        
        for x in (0, 1):
            Change.objects.create(
                interval = REVERSE_INTERVAL_DICT['II'],
                extension = REVERSE_EXTENSIONS_DICT['minor'],
                beats = 4,
                order = 1+(x*3),
                tune = tune)

            Change.objects.create(
                interval = REVERSE_INTERVAL_DICT['V'],
                extension = REVERSE_EXTENSIONS_DICT['7th'],
                beats = 4,
                order = 1+(x*3),
                tune = tune)

            Change.objects.create(
                interval = REVERSE_INTERVAL_DICT['I'],
                extension = REVERSE_EXTENSIONS_DICT['major 7th'],
                beats = 8,
                order = 1+(x*3),
                tune = tune)
        
        prerendered = "II-7 / / / V7 / / / I^ / / / / / / /\nII-7 / / / V7 / / / I^ / / / / / / /"
        self.assertEquals(prerendered, tune.dump())
