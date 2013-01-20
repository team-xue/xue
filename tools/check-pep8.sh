#!/bin/bash

for dir in accounts auditlock classes common impexp infocenter limitedcomment materials prepopulate scores scripts tagfrontend uniapply ; do
	echo "checking ${dir}" ;
	find "${dir}/" -type f -name '*.py' | grep -v '/migrations/' | xargs pep8 || exit 1;
done
