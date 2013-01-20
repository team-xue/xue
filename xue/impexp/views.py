# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from xue.common import choices as xue_choices
from xue.common.decorators import quickview, limit_role
from xue.common.utils import is_model_accessible

from .models import ExportTemplate
from .forms import EditInfoForm


# This CANNOT make use of quickview, because the template
# ITSELF is dynamic!
@login_required
def detail_view(request):
    usr, info_obj = request.user, None

    try:
        info_obj = usr.central_info
    except ObjectDoesNotExist:
        pass

    return {
            'entry': info_obj,
            'user': usr,
            'profile': usr.profile,
            }


@login_required
@limit_role([0])
@quickview('infocenter/edit.html')
def edit_view(request):
    usr = request.user

    try:
        info_obj = usr.central_info
    except ObjectDoesNotExist:
        # is this possible? -- maybe
        info_obj = CentralStudentInfo(user=usr)
        info_obj.save()

    # lock status
    if info_obj.is_locked:
        # this should be caught in template and render an
        # error page...
        return {
                'is_locked': True,
                }

    if request.method == 'POST':
        frm = EditInfoForm(request.POST, instance=info_obj)
        if frm.is_valid():
            frm.save()
            return redirect('xue.infocenter.views.detail_view')
    else:
        frm = EditInfoForm(instance=info_obj)

    return {
            'is_locked': False,
            'form': frm,
            }


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
