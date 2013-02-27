# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from xue.materials.models import MaterialEntry


class AddMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialEntry
        fields = ('title', 'content', 'tags', )


# this is same as AddMaterialForm for now
class EditMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialEntry
        fields = ('title', 'content', 'tags', )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
