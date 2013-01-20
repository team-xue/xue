# -*- coding: utf-8 -*-
#
# tagging support for django-cms

from django.db import models

class Tag(models.Model):
    name = models.CharField(unique=True, max_length=32)

    class Meta:
        app_label = 'cms'

    def __unicode__(self):
        return u'%s' % self.name
