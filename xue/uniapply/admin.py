# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .models import *
from django.contrib import admin


class TargetAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'user',
            'start_date',
            'end_date',
            'identifier',
            'template',
            )


class AuditingRuleAdmin(admin.ModelAdmin):
    list_display = (
            'target',
            'auditer',
            'niceness',
            )


class UniApplicationEntryAdmin(admin.ModelAdmin):
    list_display = (
            'user',
            'get_target_name',
            'ctime',
            )


class AuditOutcomeAdmin(admin.ModelAdmin):
    list_display = (
            'entry',
            'rule',
            'status',
            'reason',
            )


for _model, _admin in (
        (Target, TargetAdmin),
        (AuditingRule, AuditingRuleAdmin),
        (UniApplicationEntry, UniApplicationEntryAdmin),
        (AuditOutcome, AuditOutcomeAdmin),
        ):
    admin.site.register(_model, _admin)

del _model, _admin


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8
