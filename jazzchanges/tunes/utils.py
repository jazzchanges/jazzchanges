# -*- coding: utf-8 -*-

ASCII_MAPPINGS = (
    (u'▵', '^'),
    (u'ø', '*'),
)

def ascii_map(s):

    for uni, asc in ASCII_MAPPINGS:
        s = s.replace(uni, asc)
    
    return s

def find_interval(ch):
    """
    Returns an integer for a chord.

    'bVII-7' -> finds bVII -> gives 10
    """
    from jazzchanges.tunes.models import INTERVALS

    # longest strings up front
    _INT = sorted(INTERVALS, key=lambda x: len(x[1]), reverse=True)

    for i, s in _INT:
        if s in ch:
            return i
    
    raise Exception('No interval found.')

def find_extension(ch):
    """
    Returns an extension for a chord.

    'I^9' -> finds ^9 -> gives '0,4,7,11,14'
    """
    from jazzchanges.tunes.models import REVERSE_EXTENSIONS_DICT

    # longest strings up front
    _EXT = sorted(REVERSE_EXTENSIONS_DICT.items(), key=lambda x: len(x[0]), reverse=True)

    for s, i in _EXT:
        if s in ch:
            return i
    
    raise Exception('No extension found.')