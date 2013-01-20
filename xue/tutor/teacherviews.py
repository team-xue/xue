# -*- coding: utf-8 -*-

from functools import wraps

from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from xue.common import choices as xue_choices
from xue.common.decorators import quickview, limit_role

from xue.tutor.models import StudentApplication, APPLICATION_STATUS_DICT, \
                              TutorProject, StudentProject

from xue.tutor.forms import ReviewForm, SecondReviewForm


def ensure_teacher_proj_coherency(request, proj_id):
    usr = request.user
    usr_role = usr.profile.role
    is_allowed, disallow_reason = True, u''

    if usr_role == 0:
        # student; disallow
        is_allowed, disallow_reason = False, u'学生无权访问此页面'
    else:
        # int() call is sure to succeed because the url resolver regex already
        # ensures its (relative) sanity
        proj = get_object_or_404(TutorProject, id=int(proj_id))

        if usr != proj.teacher and not usr.is_staff:
            is_allowed, disallow_reason = False, u'您无权管理不属于自己的项目'

    if not is_allowed:
        return (False, None, {
                'is_allowed': is_allowed,
                'disallow_reason': disallow_reason,
                }, )

    # access granted. go ahead
    return (True, proj, {'is_allowed': is_allowed, }, )


@login_required
@quickview('tutor/teacher_projlist.html')
def listpage_view(request):
    usr = request.user
    usr_role = usr.profile.role
    is_allowed, disallow_reason = True, u''

    if usr_role == 0:
        # student; disallow
        is_allowed, disallow_reason = False, u'学生无权访问此页面'

    result = {
            'is_allowed': is_allowed,
            'disallow_reason': disallow_reason,
            }

    if is_allowed:
        # fetch projects owned by user
        # also admins can manage all the projects
        projs = (TutorProject.objects.all()
                if usr.is_staff
                else TutorProject.objects.filter(teacher=usr)
                )
        result['projects'] = projs

    return result


@login_required
@limit_role([1])
@quickview('tutor/teacher_index.html')
def projectpage_view(request, proj_id):
    allowed, proj, result = ensure_teacher_proj_coherency(request, proj_id)

    if allowed:
        result['project'] = proj

    return result


@login_required
@limit_role([1])
@quickview('tutor/teacher_pickinglist.html')
def pickinglist_view(request, proj_id):
    allowed, proj, result = ensure_teacher_proj_coherency(request, proj_id)

    if not allowed:
        return result

    result['project'] = proj
    result['entries'] = StudentProject.objects.filter(project=proj)

    return result


@login_required
@limit_role([1])
@quickview('tutor/review.html')
def picking_view(request, proj_id, entry_id):
    allowed, proj, result = ensure_teacher_proj_coherency(request, proj_id)

    if not allowed:
        return result

    entry = get_object_or_404(StudentProject, id=int(entry_id))
    student = entry.student
    application_entry = StudentApplication.objects.get(student=student)

    if request.method == 'POST':
        # form data
        frm = SecondReviewForm(request.POST)
        if frm.is_valid():
            # valid data, store it
            entry.status = frm.cleaned_data['status']
            if entry.status == 1:
                # succeeded
                entry.fail_reason = u''
            else:
                # failed
                entry.fail_reason = frm.cleaned_data['fail_reason']
                entry.fail_count += 1

            entry.save()
            return redirect('xue.tutor.teacherviews.pickinglist_view', proj_id=proj_id)
    else:
        frm = SecondReviewForm()

    return {'form': frm,
             'entry': application_entry,
             'student': student,
            }


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
