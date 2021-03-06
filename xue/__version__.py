#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is taken from the weiyu project.
# NOTE: the SVN support code reused Django project's.

from __future__ import unicode_literals, division

__all__ = ['VERSION_MAJOR', 'VERSION_MINOR', 'VERSION_REV',
           'VERSION', 'VERSION_DEV', 'VERSION_STR',
           ]

import os.path
import re
import xue

# Version information.
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_REV = 1

VERSION = (VERSION_MAJOR, VERSION_MINOR, VERSION_REV, 'alpha', 0)

_VCS_HANDLERS = []


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])

    return version


###############################################################
## for getting revision info from a VCS
###############################################################


def get_vcs_revision(path=None):
    # try the handlers one by one, return the first successful
    # match of VCS info
    for handler in _VCS_HANDLERS:
        is_ok, result = handler(path)
        if is_ok:
            return (is_ok, result, )

    # no info available, signal failure
    return (False, None, )


def get_svn_revision(path=None):
    '''Returns the SVN revision in the form SVN-XXXX, where XXXX is the
    revision number.

    Returns (False, None) if anything goes wrong, such as an unexpected
    format of internal SVN files.

    If path is provided, it should be a directory whose SVN info you want to
    inspect. If it's not provided, this will use the root package
    directory.

    '''

    rev = None
    if path is None:
        path = xue.__path__[0]
    entries_path = '%s/.svn/entries' % path

    try:
        with open(entries_path, 'r') as fp:
            entries = fp.read()
    except IOError:
        return (False, None, )
    else:
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match(r'(\d+)', entries):
            rev_match = re.search(r'\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
        # Older XML versions of the file specify revision as an attribute of
        # the first entries node.
        else:
            from xml.dom import minidom
            dom = minidom.parse(entries_path)
            rev = dom.getElementsByTagName('entry')[0].getAttribute('revision')

    if rev:
        return (True, 'SVN-%s' % rev, )
    return (False, None, )

_VCS_HANDLERS.append(get_svn_revision)


def get_git_commit(path=None):
    '''Returns the Git commit id in the form Git-xxxxxxxx,
    where xxxxxxxx is the commit hash truncated after the 8th hex digit.

    Returns (False, None) if anything goes wrong.

    If path is provided, it should be a directory whose Git info you want to
    inspect. If it's not provided, this will use the root package
    directory's parent dir.

    '''

    # Git directory...
    if path is None:
        path = xue.__path__[0]
        git_path = '%s/../.git/' % path
    else:
        git_path = '%s/.git/' % path
    # normalize a little bit
    git_path = os.path.normpath(git_path)

    # Phase 1, read the HEAD file to get the current head
    head_path = os.path.join(git_path, 'HEAD')
    try:
        with open(head_path, 'rb') as fp:
            ref = fp.read().strip()
    except IOError:
        return (False, None, )
    else:
        ref_path_match = re.search(r'^ref: (.*)$', ref)
        if ref_path_match:
            ref_path = ref_path_match.groups()[0]
        else:
            # unrecognized HEAD format...
            return (False, None, )

    # now ref_path is ready, move on to Phase 2, pull out the commit id
    commit_path = os.path.normpath(os.path.join(git_path, ref_path))
    try:
        with open(commit_path, 'rb') as fp:
            commit = fp.read().strip()
    except IOError:
        return (False, None, )
    else:
        # Truncate the commit id.
        commit_id = commit[:8]

    # if we arrive here, we're done and commit id is ready.
    return (True, 'Git-%s' % commit_id, )

_VCS_HANDLERS.append(get_git_commit)

# init our version strings... they are constant during one run
_verstr = get_version()

# VCS revision, if we are in an devel environment
# updated to support Git too
_vcs_ok, _vcs_rev = get_vcs_revision()

VERSION_DEV = _vcs_rev if _vcs_ok else ''
VERSION_STR = _verstr if not _vcs_ok else ' '.join([_verstr, _vcs_rev])

del _vcs_ok, _vcs_rev, _verstr


# vi:ai:et:ts=4 sw=4 sts=4 fenc=utf-8
