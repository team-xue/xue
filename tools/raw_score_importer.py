#!/usr/bin/env python
# -*- coding: utf-8 -*-

# data format:
# id_number\tscore\tyear\tterm

from __future__ import unicode_literals, division

import sys
import os

realpath = os.path.realpath
pathjoin = os.path.join
normpath = os.path.normpath
dirname = os.path.dirname

PROJECT_PATH = normpath(pathjoin(dirname(realpath(__file__)), u'..'))

sys.path.insert(0, normpath(pathjoin(PROJECT_PATH, u'..')))
sys.path.insert(0, PROJECT_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'xue.settings'

from xue.scores.models import RawGradeEntry


def read_in(fname):
    result = []

    with open(fname, 'r') as fp:
        for line in fp:
            cooked = line.strip()
            if not cooked:
                continue

            cooked = cooked.replace(' ', '').split('\t')

            result.append(tuple([
                    cooked[0],
                    float(cooked[1]),
                    int(cooked[2]),
                    int(cooked[3]),
                    ]))

    return result


def import_into_db(elem):
    ident, score, yr, tm = elem

    print ('%s:' % ident),

    try:
        dummy = RawGradeEntry(id_number=ident, year=yr, term=tm)
    except RawGradeEntry.DoesNotExist:
        print 'repeat'
        return

    obj = RawGradeEntry(id_number=ident, year=yr, term=tm, rawscore=score,
            gpa=-1.0)
    obj.save()
    print 'ok'


def main():
    if len(sys.argv) == 1:
        print >>sys.stderr, ('usage: %s <files to import into raw score db>'
                % sys.argv[0]
                )
        sys.exit(1)

    for fname in sys.argv[1:]:
        print 'importing %s\'s content...' % fname
        raw_lst = read_in(fname)

        for elem in raw_lst:
            import_into_db(elem)

    sys.exit(0)


if __name__ == '__main__':
    main()


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8:
