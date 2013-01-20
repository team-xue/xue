#!/bin/sh
as_yuicompressor="yuicompressor"

cat `find . -maxdepth 1 -type f -name '*.css'` | $as_yuicompressor --type css
