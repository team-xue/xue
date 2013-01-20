# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.comments.models import Comment
from .forms import LimitedCommentForm


def get_model():
    return Comment


def get_form():
    return LimitedCommentForm


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
