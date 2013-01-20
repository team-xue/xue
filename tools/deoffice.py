#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Deletes Microsoft Office markups from HTML fragment
# using simple RE's for this use

import sys
import re

DESTYLER = re.compile(ur'(?imu)<(.*?)\s+(?:style=".*?"|lang=".*?"|class="Mso.*?"|width=".*?"|height=".*?")\s*>')
DESPACER_GENERAL = re.compile(ur'[ 銆€\t\v]{2,}')
DETAGGER = re.compile(ur'(?i)</?(?:span|strong)>')

def process(content):
    tmp = DESTYLER.sub(ur'<\1>', content)
    tmp = tmp.replace(u'&nbsp;', u' ')
    tmp = DESPACER_GENERAL.sub(u' ', tmp)
    tmp = DETAGGER.sub(u'', tmp)
    tmp = tmp.replace(u'<p> ', u'<p>')
    tmp = tmp.replace(u' </p>', u'</p>')
    tmp = tmp.replace(u'<p></p>', u'')
    return tmp.strip()

def main(argc, argv):
    if argc != 3:
        print >>sys.stderr, (u'deletes micro$oft office markups from '
                             u'an html fragment\n'
                             )
        print >>sys.stderr, u'usage: %s <input_file> <output_file>' % argv[0]
        return 1
    infilename, outfilename = argv[1], argv[2]

    try:
        with open(infilename, 'rb') as infp:
            source_chunk = infp.read()
    except IOError, e:
        print >>sys.stderr, u'error: there is something wrong with IO'
        print >>sys.stderr, u'       exc message:', e.message
        return 2

    try:
        source = source_chunk.decode('utf-8-sig')
    except UnicodeDecodeError:
        print >>sys.stderr, u'error: input appears not utf-8'
        return 4

    # should not have problem encoding because it's valid unicode
    result = process(source).encode('utf-8')

    try:
        with open(outfilename, 'w') as outfp:
            outfp.write(result)
    except IOError, e:
        print >>sys.stderr, u'error: can\'t write output'
        print >>sys.stderr, u'       exc message:', e.message
        return 8

    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))


# vim:ai:et:ts=4:sw=4:sts=4:ff=unix:fenc=utf-8:
