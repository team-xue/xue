# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from ..common import choices as xue_choices
from ..common.decorators import quickview

from .models import *
from .forms import *


def prepare_results(user):
    qs = BandExamResult.objects.filter(user=user)
    return (
            (xue_choices.BAND_DICT.get(i.exam_type, '[未知]'), i.score, )
            for i in qs
            )


@login_required
@quickview('bandexams/my.html')
def my_view(request):
    user = request.user
    results = prepare_results(user)

    return {
            'results': results,
            }


@login_required
@quickview('bandexams/add.html')
def add_view(request):
    user = request.user

    if request.method == 'POST':
        frm = AddBandScoreForm(request.POST)
        if frm.is_valid():
            with transaction.commit_on_success():
                entry = frm.save(commit=False)
                entry.user = user
                entry.save()

            return redirect(my_view)
    else:
        frm = AddBandScoreForm()

    return {
            'form': frm,
            }


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
