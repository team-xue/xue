# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x


def is_model_accessible(model_user, user):
    if not user.is_staff:
        return model_user == user
    return True


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
