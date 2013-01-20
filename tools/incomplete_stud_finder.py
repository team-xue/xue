#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

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

from django.contrib.auth.models import User
#from xue.common.choices import ROLE_CHOICES


def is_empty(s):
    return len(s.strip()) == 0


def main():
    status = []

    for user in User.objects.all():
        profile = user.get_profile()

        if profile.role != 0:
            # not a student
            continue

        status = []

        if is_empty(profile.location):
            status.append(u'location')

        if is_empty(profile.phone):
            status.append(u'phone')

        if is_empty(profile.high_school):
            status.append(u'highschool')

        if is_empty(profile.hobby):
            status.append(u'hobby')

        if status:
            print u'%s %s [%s]: %s' % (
                    unicode(profile.klass),
                    profile.realname,
                    profile.phone,
                    u' '.join(status)
                    )


if __name__ == '__main__':
    main()


# vim:ai:et:ts=4:sw=4:sts=4:ff=unix:fenc=utf-8:
