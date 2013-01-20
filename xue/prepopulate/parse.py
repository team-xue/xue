# -*- coding: utf-8 -*-
# simple prepopulated tables querier -- input parser

from __future__ import unicode_literals, division

INPUT_ENCODING = 'utf-8'
FIELDS = ('name', 'gender', 'phone', 'role', 'ident', )


def parse_line(ln):
    lst = ln.split('$')
    # may silently eat some items... maybe
    return lst[0], dict(zip(FIELDS, lst[1:]))


def parse_lines(lst):
    result_dct = {}

    for ln in lst:
        if ln:
            num, entry = parse_line(ln)
            result_dct[num] = entry

    return result_dct


def parse_file(fn):
    with open(fn, 'rb') as fp:
        content = fp.read()

    return parse_lines(content.decode(INPUT_ENCODING).split('\n'))


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
