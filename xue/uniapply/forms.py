# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from .models import *
from ..materials.models import MaterialEntry


class UniApplyForm(forms.ModelForm):
    class Meta:
        model = UniApplicationEntry
        exclude = ('user', 'target', )

    def __init__(self, *args, **kwargs):
        super(UniApplyForm, self).__init__(*args, **kwargs)

        initial = self.initial
        if 'user' not in initial:
            try:
                user = self.user
            except AttributeError:
                return
        else:
            user = initial['user']

        # Filter the materials queryset
        mat_qs = MaterialEntry.objects.filter(user=user)
        self.fields['materials'].queryset = mat_qs


class AuditForm(forms.ModelForm):
    class Meta:
        model = AuditOutcome
        exclude = ('entry', 'rule', )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
