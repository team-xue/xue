#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# automatically correct markup for common CPC regulation docs
# again using simple RE's for this use

import sys
import re

NUMBER = ur'[一二三四五六七八九十零〇十百千万亿]'
ASSEMBLY = ur'第%s+编' % NUMBER
CHAPTER = ur'第%s+章' % NUMBER
SECTION = ur'第%s+节' % NUMBER
ITEM = ur'第%s+条' % NUMBER

SELECTOR = ur'(?m)^<p>(%s\s*.*?)</p>$'

ASSEMBLY_LINE = re.compile(SELECTOR % ASSEMBLY)
CHAPTER_LINE = re.compile(SELECTOR % CHAPTER)
SECTION_LINE = re.compile(SELECTOR % SECTION)

ASSEMBLY_HEADING_FORMAT = ur'<h3>%s</h3>'
CHAPTER_HEADING_FORMAT = ur'<h4>%s</h4>'
SECTION_HEADING_FORMAT = ur'<h5>%s</h5>'

ITEM_START_LINE = re.compile(SELECTOR % ITEM)

ORDINARY_LINE = re.compile(ur'^<p>(.*?)</p>$')

[
        TYP_ITEM_FIRST, TYP_ITEM_CONTINUATION,
        TYP_CHAPTER, TYP_ASSEMBLY, TYP_SECTION,
        ] = range(5)

def normalize_space(txt):
    # convert half-width spaces to full-width ones
    return txt.replace(u' ', u'　')

def classify_line(line):
    def returner(typ, matchobj):
        return (typ, normalize_space(matchobj.group(1)), )

    #print `line`
    # item start...
    attempt = ITEM_START_LINE.match(line)
    if attempt is not None:
        return returner(TYP_ITEM_FIRST, attempt)

    # chapter start...
    attempt = CHAPTER_LINE.match(line)
    if attempt is not None:
        return returner(TYP_CHAPTER, attempt)

    # section start...
    attempt = SECTION_LINE.match(line)
    if attempt is not None:
        return returner(TYP_SECTION, attempt)

    # even rarer, assembly...
    attempt = ASSEMBLY_LINE.match(line)
    if attempt is not None:
        return returner(TYP_ASSEMBLY, attempt)

    # XXX PERFORMANCE SERIOUSLY HURTS, SINCE ORDINARY LINES ARE THE MOST!!
    # fall back to something not very interesting but surely resolves
    attempt = ORDINARY_LINE.match(line)
    return returner(TYP_ITEM_CONTINUATION, attempt)

def compose_item(txtlines):
    return u'<p>%s</p>' % (u'<br />\n'.join(txtlines))

def flush_item_pool(pool, main_pool):
    if len(pool) > 0:
        main_pool.append(compose_item(pool))

def del_extra_sp(txt):
    # mainly used to reduce titles like "总 则" to one with no spaces inside
    # absolutely no half-width spaces, thanks to the normalize_spaces func...
    tmp = txt.replace(u'　', u' ', 1)
    tmp = tmp.replace(u'　', u'')
    tmp = tmp.replace(u' ', u'　', 1)
    return tmp

def process_lines(lines):
    result, pool = [], []
    for l in lines:
        line_type, line_content = classify_line(l)
        if line_type == TYP_ITEM_FIRST:
            # check if there is anything in the line pool
            # if there is something, pour into result pool
            flush_item_pool(pool, result)
            pool = [line_content]
        elif line_type == TYP_ITEM_CONTINUATION:
            # append to the current item pool
            pool.append(line_content)
        elif line_type == TYP_CHAPTER:
            # chapter line, apply the heading tag
            flush_item_pool(pool, result)
            pool = []
            result.append(CHAPTER_HEADING_FORMAT % del_extra_sp(line_content))
        elif line_type == TYP_SECTION:
            # section line, apply another heading tag
            flush_item_pool(pool, result)
            pool = []
            result.append(SECTION_HEADING_FORMAT % del_extra_sp(line_content))
        elif line_type == TYP_ASSEMBLY:
            # assembly line, apply (yet) another heading tag
            flush_item_pool(pool, result)
            pool = []
            result.append(ASSEMBLY_HEADING_FORMAT % del_extra_sp(line_content))
    # flush the pool, if there is still content in it...
    # now the flushing code isn't duplicated
    flush_item_pool(pool, result)

    return u'\n'.join(result)

def process(content):
    tmp = process_lines((l.strip() for l in content.strip().split(u'\n')))
    return tmp

def main(argc, argv):
    if argc != 3:
        print >>sys.stderr, (u'reformat an sufficiently formal Chinese document'
                             u'in the form of an html fragment\n'
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
