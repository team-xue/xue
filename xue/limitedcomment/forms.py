# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.contrib.comments.forms import CommentForm
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

_get_for_model = ContentType.objects.get_for_model


class LimitedCommentForm(CommentForm):
    def get_comment_create_data(self):
        return dict(
            content_type=_get_for_model(self.target_object),
            object_pk=force_unicode(self.target_object._get_pk_val()),
#            user_name    = self.cleaned_data["name"],
#            user_email   = self.cleaned_data["email"],
#            user_url     = self.cleaned_data["url"],
            comment=self.cleaned_data["comment"],
            submit_date=datetime.datetime.now(),
            site_id=settings.SITE_ID,
            is_public=True,
            is_removed=False,
        )


LimitedCommentForm.base_fields.pop('name')
LimitedCommentForm.base_fields.pop('email')
LimitedCommentForm.base_fields.pop('url')


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
