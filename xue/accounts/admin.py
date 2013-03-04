# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .models import *
from django.contrib import admin


class DMUserProfileAdmin(admin.ModelAdmin):
    list_display = (
            'nickname',
            'realname',
            'gender',
            'role',
            'id_number',
            )

    list_filter = (
            'role',
            )

    search_fields = (
            'realname',
            'id_number',
            )


admin.site.unregister(DMUserProfile)
admin.site.register(DMUserProfile, DMUserProfileAdmin)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8:
