#!/usr/bin/env python
# coding:utf-8

import re
import sys


PROCESSOR = re.compile(ur"^(\d{10})\s+([^\t]+)\s+(男|女)\s+(\d{17}[0-9Xx])$")

for l in sys.stdin:
    s = l.strip().decode('utf-8')
    print (PROCESSOR.sub(ur"\1$\2$\3$$S$\4", s)).encode('utf-8')


# vim:ai:et:ts=4:sw=4:sts=4:ff=unix:fenc=utf8:
