# -*- coding: utf-8 -*-
# simple prepopulated tables querier -- querier object

from __future__ import unicode_literals, division

from functools import wraps
from os.path import join as pathjoin
from os.path import abspath, dirname

from django.conf import settings

from xue.prepopulate.parse import parse_file

MYPATH = settings.XUE_PREPOPULATE_DIR
INPUT_FILES = settings.XUE_PREPOPULATE_FILES


def _prepare_db():
    result_dct = {}
    for fn in INPUT_FILES:
        path = pathjoin(MYPATH, fn)
        result_dct.update(parse_file(path))
    return result_dct


class Querier(object):
    def __init__(self):
        self._db = _prepare_db()

    def have(self, num):
        return (num in self._db)

    def lookup(self, num):
        try:
            return self._db[unicode(num)]
        except KeyError:
            raise ValueError('no user matching number \'%s\' exists' % num)

    def extract_org(self, id_num):
        # TODO: refactor to use something generic, maybe file-based
        # XXX What is written below is TOTALLY hack and ABSOLUTELY NOT
        # portable across schools, so clean this up ASAP!!
        year, major_code, cls_seq = None, None, None

        if id_num[0] == '0':
            # old format
            major_code = id_num[:4]
            yr_2digit = int(id_num[4:6])
            cls_seq = int(id_num[6:8])

            year = (1900 if yr_2digit > 50 else 2000) + yr_2digit
        else:
            # new format in use beginning from 2012
            # it's like 1030512101... also 10 digits
            major_code = id_num[1:5]
            yr_2digit = int(id_num[5:7])
            cls_seq = int(id_num[7])
            year = 2000 + yr_2digit

        return year, major_code, cls_seq


querier = Querier()


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
