"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from jazzchanges.tunes.models import Tune, Change, REVERSE_KEY_DICT, REVERSE_INTERVAL_DICT, EXTENDED_KEY_DICT


class TunesTest(TestCase):
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