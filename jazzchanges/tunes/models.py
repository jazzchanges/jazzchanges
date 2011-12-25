from django.db import models

from django.utils.translation import ugettext_lazy as _


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
    ('3/4', '3/4'),
    ('4/4', '4/4'),
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
    title = models.CharField(max_length=255)
    key = models.PositiveIntegerField(choices=KEYS)
    time = models.CharField(max_length=12, default='4/4', choices=TIMES)

    owner = models.ForeignKey('auth.User', related_name='tunes')

    @property
    def beats_per_measure(self):
        return int(self.time.split('/')[0])

    @property
    def note_value(self):
        return int(self.time.split('/')[1])

    def get_changes(self, **kwargs):
        changes = self.changes.with_key(**kwargs) # custom manager method
        return changes
    
    def get_systems(self, **kwargs):
        """
        Return a tuple of a nested list of changes for a system (four bars) with
        respect to the changes and the width (rounded down) of px per chord.
        """
        length = kwargs.pop('length', SYSTEM_LENGTH)
        width = kwargs.pop('width', 620)

        changes = self.get_changes(**kwargs)

        beats_per_system = self.beats_per_measure * length

        full_list = []
        for change in changes:
            full_list += [change] * change.beats

        return list(chunks(full_list, beats_per_system)), int( (float(width) / ( beats_per_system ) ) )
    
    def __unicode__(self):
        return u'%s in %s' % (self.title, self.get_key_display())




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
    ('0,4,7',       'major',        ''),
    ('0,3,7',       'minor',        'm'),
    ('0,4,7,10',    '7th',          '7'),
    ('0,4,7,11',    'major 7th',    'maj7'),
    ('0,3,7,10',    'minor 7th',    'm7'),
)
EXTENSIONS = [(x, y) for x, y, z in EXTENSIONS_DEEP]
EXTENSIONS_DICT = dict([(x, z) for x, y, z in EXTENSIONS_DEEP])


class ChangeManager(models.Manager):
    def with_key(self, key=None):
        qs = super(ChangeManager, self).get_query_set()

        [change.get_chord(key=key) for change in qs]

        return qs


class Change(models.Model):
    def __init__(self, *args, **kwargs):
        self.chord = None # text representation of chord
        return super(Change, self).__init__(*args, **kwargs)

    interval = models.PositiveIntegerField(choices=INTERVALS)
    extension = models.CharField(max_length=32, default='', choices=EXTENSIONS)

    beats = models.PositiveIntegerField(default=4)
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
        Transposes into the correct root for the change given a 
        key (else defaults to tune's original key).
        """
        transposed_key = key + self.interval
        return EXTENDED_KEY_DICT[transposed_key]
    
    def get_chord(self, **kwargs):
        """
        Returns a chord and sets to chord attribute as text.

        Key is an integer 1-12.
        """
        # for some reason kwarg.pop isn't working...
        key = kwargs['key'] if kwargs.get('key', None) else self.tune.key

        root = self.get_root(key)
        self.chord = ''.join([root, self.short_extension])

        return self.chord

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s (%s) for %d beats' % (self.get_chord(), self.interval, self.beats)