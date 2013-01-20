# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from .models import CentralStudentInfo


class EditInfoForm(forms.ModelForm):
    class Meta:
        model = CentralStudentInfo
        exclude = (
                'user',
                'join_date',
                'klass',
                'is_locked',
                )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
