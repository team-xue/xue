# -*- coding: utf-8 -*-

from django.shortcuts import redirect, get_object_or_404
from django.db import transaction

from xue.common.decorators import quickview, limit_role

from xue.tutor.forms import StudentApplicationForm, ProjectSelectionForm
from xue.tutor.models import StudentProject, StudentApplication

# expiration...
PRELIMINARY_EXPIRED, SECONDARY_EXPIRED = True, True


@limit_role([0])
@quickview('tutor/stud_apply_expired.html')
def apply_expired_view(request):
    return {}


@limit_role([0])
@quickview('tutor/stud_apply.html')
def apply_view(request):
    is_repeat = False
    try:
        StudentApplication.objects.get(student=request.user)
        is_repeat = True
    except StudentApplication.DoesNotExist:
        pass

    if request.method == 'POST':
        # form data
        frm = StudentApplicationForm(request.POST)
        if frm.is_valid():
            # valid data, store it if no previous application exists
            if not is_repeat:
                with transaction.commit_on_success():
                    entry = frm.save(commit=False)
                    entry.student = request.user
                    entry.save()
                return redirect('xue.tutor.views.mainpage_view')
    else:
        frm = StudentApplicationForm()

    return {'form': frm,
            'is_repeat': is_repeat,
             }


@limit_role([0])
@quickview('tutor/stud_selectproj.html')
def selectproj_view(request):
    # protect against rejected applicants and other random people
    dummy = get_object_or_404(
            StudentApplication,
            student=request.user,
            status=1,
            )

    # verify max count
    projs = list(StudentProject.objects.filter(student=request.user))
    if len(projs) >= 2:
        return {'is_exceeded': True,
                'projects': projs,
                }

    if request.method == 'POST':
        # form data
        frm = ProjectSelectionForm(request.POST)
        if frm.is_valid():
            # valid data, store it
            with transaction.commit_on_success():
                entry = frm.save(commit=False)
                entry.student = request.user
                entry.save()
            return redirect('xue.tutor.views.mainpage_view')
    else:
        frm = ProjectSelectionForm()

    return {'is_exceeded': False,
            'projects': projs,
            'form': frm,
            }

# expiration
if PRELIMINARY_EXPIRED:
    apply_view = apply_expired_view

if SECONDARY_EXPIRED:
    selectproj_view = apply_expired_view


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
