#!/bin/sh
as_yuicompressor="yuicompressor"

cat `find . -maxdepth 1 -type f -name '*.js'` | $as_yuicompressor --type js
