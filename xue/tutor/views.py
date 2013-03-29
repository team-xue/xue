# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

import datetime

from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from xue.common import choices as xue_choices
from xue.common.decorators import quickview, limit_role

from xue.tutor.models import StudentApplication, APPLICATION_STATUS_DICT, \
                              TutorProject

from xue.tutor.forms import ReviewForm


def this_year():
    return datetime.datetime.today().year


@login_required
@quickview('tutor/index.html')
def mainpage_view(request):
    usr = request.user
    usr_role = usr.profile.role

    # role-based ident
    is_student = has_applied = False
    apply_id, apply_status, apply_obj = 0, 'n/a', None
    # XXX hardcoded role!
    if usr_role == 0:
        # student
        is_student = True

        # check if already applied
        try:
            apply_obj = StudentApplication.objects.get(student=usr)
            has_applied = True
            apply_id = apply_obj.id
            apply_status = APPLICATION_STATUS_DICT.get(
                    apply_obj.status,
                    'unknown',
                    )
        except ObjectDoesNotExist:
            pass

    return {
            'is_student': is_student,
            'has_applied': has_applied,
            'apply_id': apply_id,
            'apply_status': apply_status,
            'apply_obj': apply_obj,
            'apply_closed': True,  # XXX Hardcoded for now!!
            }


@login_required
@quickview('tutor/application_list.html')
def application_list_view(request):
    app_entries = StudentApplication.objects.filter(
            # 大二下
            student__central_info__klass__date__year=this_year() - 2,
            # 未审核的
            status=0,
            )

    return {
            'entries': app_entries,
            'STATUS_DICT': APPLICATION_STATUS_DICT,
            }


@login_required
@quickview('tutor/project_list.html')
def project_list_view(request):
    usr = request.user
    usr_role = usr.profile.role

    if usr_role == 0:
        # student, filter the project list according to year
        proj_entries = TutorProject.objects.filter(
                year=usr.central_info.get_year(),
                )
    else:
        proj_entries = TutorProject.objects.all()

    return {
            'entries': proj_entries,
            }


@login_required
@quickview('tutor/project_detail.html')
def project_detail_view(request, proj_id):
    usr = request.user
    usr_role = usr.profile.role

    extra_kwargs = (
            {}
            if usr_role != 0
            else {'year': usr.central_info.get_year(), }
            )

    project = get_object_or_404(
            TutorProject,
            id=int(proj_id),
            **extra_kwargs
            )

    return {
            'project': project,
            }


@login_required
@limit_role([1, 2])
@quickview('tutor/review.html')
def review_view(request, entry_id):
    entry = get_object_or_404(StudentApplication, id=int(entry_id))
    student = entry.student

    if request.method == 'POST':
        # form data
        frm = ReviewForm(request.POST)
        if frm.is_valid():
            # valid data, store it
            entry.status = frm.cleaned_data['status']
            entry.fail_reason = frm.cleaned_data['fail_reason']
            entry.save()
            return redirect('xue.tutor.views.application_list_view')
    else:
        frm = ReviewForm()

    return {
            'form': frm,
            'entry': entry,
            'student': student,
            }


@login_required
@limit_role([1, 2])
@quickview('tutor/student_summary.csv')
def applicant_overview_csv_view(request):
    applications = StudentApplication.objects.all()

    cooked_applications = []
    for appl in applications:
        stud = appl.student
        prof = stud.profile
        cooked_dict = {
                'realname': prof.realname,
                'id': stud.username,
                'gender': xue_choices.GENDER_DICT[prof.gender],
                'klass': unicode(prof.klass),
                'id_number': prof.id_number,
                'political': xue_choices.POLITICAL_BKGND_DICT[prof.political],
                'phone': prof.phone,
                'awards': prof.awards if prof.awards else '--',
                'desc': appl.desc,
                }

        if prof.english_band_type == 0:
            english = '无记录'
        else:
            english = xue_choices.ENGLISH_BAND_DICT[prof.english_band_type]
            if prof.english_band_score:
                english += ' %d 分' % prof.english_band_score

        cooked_dict['english'] = english

        cooked_applications.append(cooked_dict)

    return {
            'applications': cooked_applications,
            }


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
