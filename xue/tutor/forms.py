# -*- coding: utf-8 -*-

from django import forms
from xue.tutor.models import StudentApplication, StudentProject

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        exclude = ('student', 'fail_reason', 'status', )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        exclude = ('student', 'desc', )


class ProjectSelectionForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ('project', )

    def __init__(self, year, *args, **kwargs):
        super(ProjectSelectionForm, self).__init__(*args, **kwargs)

        # filter out projects with different year set
        self.year = year
        qs = self.fields['project'].queryset
        self.fields['project'].queryset = qs.filter(year=year)


class SecondReviewForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ('status', 'fail_reason', )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
