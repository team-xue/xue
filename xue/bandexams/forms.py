# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from .models import *


class AddBandScoreForm(forms.ModelForm):
    class Meta:
        model = BandExamResult
        exclude = ('user', )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
