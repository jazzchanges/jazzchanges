# -*- coding: utf-8 -*-

UNICODE_MAPPINGS = (
    (u'▵', '^'),
    (u'ø', '*'),
)

def unicode_map(s):

    for uni, asc in UNICODE_MAPPINGS:
        s = s.replace(uni, asc)
    
    return s