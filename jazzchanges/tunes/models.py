# -*- coding: utf-8 -*-

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from jazzchanges.tunes.utils import ascii_map, find_interval, find_extension



INTERVALS = (
    (0, 'I'), # C
    (1, 'bII'),
    (2, 'II'), # D
    (3, 'bIII'),
    (4, 'III'), # E
    (5, 'IV'), # F
    (6, 'bV'),
    (7, 'V'), # G
    (8, '#V'),
    (9, 'VI'), # A
    (10, 'bVII'),
    (11, 'VII'), # B
)
INTERVAL_DICT = dict(INTERVALS)
REVERSE_INTERVAL_DICT = dict([[y, x] for x, y in INTERVALS])


EXTENSIONS_DEEP = ( 
    # (comma sep integers of intervals, name, short name)
    ('0,4,7',               'major',            u''),
    ('0,3,6',               'diminished',       u'o'),
    ('0,4,8',               'augmented',        u'+'),
    ('0,3,7',               'minor',            u'-'),

    ('0,4,7,10',            '7th',              u'7'),
    ('0,4,7,11',            'major 7th',        u'▵'),
    ('0,3,7,10',            'minor 7th',        u'-7'),

    ('0,4,7,10,13',         '7th b9',           u'7b9'),
    ('0,4,7,10,15',         '7th #9',           u'7#9'),

    ('0,3,6,10',            'minor 7th b5',     u'ø'),

    ('0,4,7,9',             '6th',              u'6'),
    ('0,3,7,9',             'minor 6th',        u'-6'),
    
    ('0,4,7,10,14',         '9th',              u'9'),
    ('0,4,7,11,14',         'major 9th',        u'▵9'),
    ('0,3,7,10,14',         'minor 9th',        u'-9'),
    
    ('0,4,7,10,14,17',      '11th',             u'11'),
    ('0,4,7,11,14,17',      'major 11th',       u'▵11'),
    ('0,3,7,10,14,17',      'minor 11th',       u'-11'),
    
    ('0,4,7,10,14,17,21',   '13th',             u'13'),
    ('0,4,7,11,14,17,21',   'major 13th',       u'▵13'),
    ('0,3,7,10,14,17,21',   'minor 13th',       u'-13'),
)

EXTENSIONS = [(x, y) for x, y, z in EXTENSIONS_DEEP]
EXTENSIONS_DICT = dict([(x, z) for x, y, z in EXTENSIONS_DEEP])
# ascii version of extensions
REVERSE_EXTENSIONS_DICT = dict([(ascii_map(z), x) for x, y, z in EXTENSIONS_DEEP])


class ChangeManager(models.Manager):
    def with_key(self, **kwargs):
        key = kwargs.pop('key', None)
        qs = super(ChangeManager, self).get_query_set().select_related().filter(**kwargs)

        [change.get_chord(key=key) for change in qs]

        return qs


class Change(models.Model):
    def __init__(self, *args, **kwargs):
        self.chord = None # text representation of chord
        return super(Change, self).__init__(*args, **kwargs)

    interval = models.PositiveIntegerField(choices=INTERVALS)
    extension = models.CharField(max_length=32, choices=EXTENSIONS)
    bass = models.PositiveIntegerField(choices=INTERVALS, blank=True, null=True)

    beats = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=1)

    tune = models.ForeignKey('tunes.Tune', related_name='changes')

    objects = ChangeManager()

    @property
    def short_extension(self):
        """
        Takes a rather convoluted 1,3,7,10 extension and turns it a 'm7'.
        """
        return EXTENSIONS_DICT[self.extension]

    def get_root(self, key):
        """
        Transposes into the correct root for the change given a key.
        """
        transposed_key = key + self.interval
        return EXTENDED_KEY_DICT[transposed_key]

    def get_bass(self, key):
        """
        Transposes into the correct bass for the change given a key.
        """
        if self.bass is None:
            return None
        
        transposed_key = key + self.bass
        return EXTENDED_KEY_DICT[transposed_key]
    
    def get_chord(self, **kwargs):
        """
        Returns a chord and sets to chord attribute as text.

        Key is an integer 1-12.
        """
        # for some reason kwarg.pop isn't working...
        key = kwargs['key'] if kwargs.get('key', None) else self.tune.key

        root = self.get_root(key)
        bass = self.get_bass(key)
        self.chord = [root, self.short_extension, bass]

        return self.chord

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s (%s) for %d beats' % (self.get_chord(), self.interval, self.beats)



SYSTEM_LENGTH = 4

KEYS = ( # always flat
    (1, 'C'),
    (2, 'Db'),
    (3, 'D'),
    (4, 'Eb'),
    (5, 'E'),
    (6, 'F'),
    (7, 'Gb'),
    (8, 'G'),
    (9, 'Ab'),
    (10, 'A'),
    (11, 'Bb'),
    (12, 'B'),
)

# useful to do KEY_DICT[4] -> 'Eb'
KEY_DICT = dict(KEYS)

# useful to do KEY_DICT['Eb'] -> 4
REVERSE_KEY_DICT = dict([[y, x] for x, y in KEYS])

# useful to do KEY_DICT[4] -> 'Eb' & KEY_DICT[16] -> 'Eb'
# mainly for adding interval to key
EXTENDED_KEY_DICT = dict(KEYS + tuple((i+12, c) for i, c in KEYS))


TIMES = (
    ('2/4', '2/4'),
    ('3/4', '3/4'),
    ('4/4', '4/4'),
    ('6/4', '6/4'),
    ('6/8', '6/8'),
    ('12/8', '12/8'),
)

def chunks(l, n):
    """ 
    Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

class Tune(models.Model):
    def __init__(self, *args, **kwargs):
        self.length = SYSTEM_LENGTH
        super(Tune, self).__init__(*args, **kwargs)
    
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    key = models.PositiveIntegerField(choices=KEYS)
    time = models.CharField(max_length=12, default='4/4', choices=TIMES)

    owner = models.ForeignKey('auth.User', related_name='tunes')

    ####################
    #### PROPERTIES ####
    ####################

    @property
    def title_slug(self):
        return slugify(self.title)

    @property
    def artist_slug(self):
        return slugify(self.artist)

    @property
    def beats_per_measure(self):
        return int(self.time.split('/')[0])
    
    @property
    def beats_per_system(self):
        return self.beats_per_measure * self.length

    @property
    def note_value(self):
        return int(self.time.split('/')[1])
    

    def query_string(self):
        # artist + song name for amazon link
        import urllib
        return urllib.quote_plus(' '.join([self.artist.lower(), self.title.lower()]))
    

    ########################
    #### HANDLE CHANGES ####
    ########################

    def get_root(self, interval):
        """
        Transposes into the correct root for the change given an interval.
        """
        transposed_key = self.key + interval
        return EXTENDED_KEY_DICT[transposed_key]

    def get_changes(self, **kwargs):
        changes = self.changes.with_key(tune=self, **kwargs) # custom manager method
        return changes
    
    def get_systems(self, **kwargs):
        """
        Return a tuple of a nested list of changes for a system (four bars) with
        respect to the changes.
        """
        self.length = kwargs.pop('length', self.length)

        changes = self.get_changes(**kwargs)

        full_list = []
        for change in changes:
            full_list += [change] * change.beats

        return list(chunks(full_list, self.beats_per_system))
    

    #########################
    #### IMPORT & EXPORT ####
    #########################

    def dump(self):
        out = []

        for system in self.get_systems():
            old_change = None
            for change in system:

                if change == old_change:
                    out.append( u'/ ' )
                else:
                    out.append(change.get_interval_display() + change.short_extension + ' ')
                
                old_change = change
                
            out.append( u'\n' )
        
        out = u''.join(out)
        return ascii_map(out)
    
    def load(self, s, save=False):
        # turn into a single line
        s = ' '.join(s.splitlines())
        # split by spaces
        s = s.split(' ')
        # remove all empty items
        s = [_s for _s in s if _s]

        change_list = []
        change = {}

        for item in s:
            if item == '/':
                # same change
                change['beats'] += 1
            else:
                # new change
                change = dict(
                    beats=1, 
                    interval=find_interval(item),
                    extension=find_extension(item))
                
                change_list.append(change)
        
        out_changes = []
        for i, change in enumerate(change_list, start=1):
            out_changes.append(Change(tune=self, order=i, **change))
        
        if save:
            [change.save() for change in out_changes]
        
        return out_changes
        


    class Meta:
        ordering = ['title']
    
    def __unicode__(self):
        return u'%s in %s' % (self.title, self.get_key_display())