from django.db import models

from django.utils.translation import ugettext_lazy as _


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


class Tune(models.Model):
    title = models.CharField(max_length=255)
    key = models.PositiveIntegerField(choices=KEYS)

    def get_changes(self):
        changes = self.changes.with_key(key)
        return changes
    
    def __unicode__(self):
        return u'%s in %s' % (self.title, self.key)


class ChangeManager(models.Manager):
    def with_key(self, key=None):
        qs = super(ChangeManager, self).get_query_set()

        [change.get_chord(key=key) for change in qs]

        return qs


class Change(models.Model):
    def __init__(self, *args, **kwargs):
        self.chord = None
        return super(Change, self).__init__(*args, **kwargs)

    interval = models.PositiveIntegerField(choices=INTERVALS)
    beats = models.PositiveIntegerField(default=4)

    order = models.PositiveIntegerField(default=1)

    tune = models.ForeignKey('tunes.Tune', related_name='changes')

    objects = ChangeManager()

    def get_root(self, key):
        """
        Transposes into the correct root for the change given a 
        key (else defaults to tune's original key).
        """
        transposed_key = key + self.interval
        return EXTENDED_KEY_DICT[transposed_key]
    
    def get_chord(self, key=None):
        """
        Returns a chord and sets to chord attribute as text.

        Key is an integer 1-12.
        """
        key = key if key else self.tune.key

        root = self.get_root(key)
        self.chord = ' '.join([root])

        return self.chord

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s (%s) for %d beats' % (self.get_chord(), self.interval, self.beats)