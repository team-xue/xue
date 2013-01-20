# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.db import transaction

from xue.common.decorators import quickview
from springaid2012.models import ApplicationEntry
from springaid2012.forms import ApplicationForm

@quickview('springaid2012/application.html')
def application_view(request):
    if request.method == 'POST':
        # form data
        frm = ApplicationForm(request.POST)
        if frm.is_valid():
            # valid data, store it
            with transaction.commit_on_success():
                entry = frm.save(commit=False)
                entry.student = request.user
                entry.save()
            return redirect('springaid2012.views.submitted_view')
    else:
        frm = ApplicationForm()

    return {
             u'form': frm,
             }

@quickview('springaid2012/apply_ok.html')
def submitted_view(request):
    return {}


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
