# -*- coding: utf-8 -*-

from django.forms import ModelForm
from springaid2012.models import ApplicationEntry

class ApplicationForm(ModelForm):
    class Meta:
        model = ApplicationEntry
        exclude = ('student', )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
