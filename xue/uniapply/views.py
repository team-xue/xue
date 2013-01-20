# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.db import transaction
from django.contrib.auth.decorators import login_required

from ..common import choices as xue_choices
from ..common.decorators import quickview

from ..impexp.utils import render_object_to_response

from .models import *
from .forms import *
from .auditing import *


@login_required
@quickview('uniapply/index.html')
def index_view(request):
    usr = request.user
    usr_role = usr.profile.role
    return {}


@login_required
@quickview('uniapply/target-list.html')
def target_list_view(request):
    user = request.user
    visible_targets = (
            i for i in Target.objects.all()
            if check_target_user(i, user)[0]
            )

    return {
            'targets': visible_targets,
            }


@login_required
@quickview('uniapply/entry-list.html')
def entry_list_view(request, target_id):
    user = request.user
    target = get_object_or_404(
            Target,
            pk=target_id,
            )

    is_visible, is_auditer = check_target_user(target, user)
    if not is_auditer:
        raise Http404

    entries = UniApplicationEntry.objects.filter(
            target=target,
            ).order_by('ctime')

    return {
            'entries': entries,
            }


@login_required
@quickview('uniapply/my.html')
def my_view(request):
    user = request.user
    entries = UniApplicationEntry.objects.filter(
            user=user,
            )

    return {
            'entries': entries,
            }


@login_required
@quickview('uniapply/target-detail.html')
def target_detail_view(request, target_id):
    user = request.user
    target = get_object_or_404(Target, pk=target_id)

    is_visible, is_auditer = check_target_user(target, user)
    if not is_visible:
        # user doesn't have the right to view the detail
        return {
                'is_allowed': False,
                }

    # convert newlines in desc...
    desc_lines = target.desc.splitlines()

    paras, tmp = [], []
    for ln in desc_lines:
        ln_stripped = ln.rstrip()
        if len(ln_stripped) > 0:
            tmp.append(ln_stripped)
            continue
        # another paragraph...
        paras.append(tmp)
        tmp = []

    # don't silently chew off the last paragraph...
    # common gotcha
    if tmp:
        paras.append(tmp)

    return {
            'is_allowed': True,
            'target': target,
            'desc_paras': paras,
            'user_is_auditer': is_auditer,
            }


@login_required
@quickview('uniapply/apply.html')
def apply_view(request, target_id):
    user = request.user
    target = get_object_or_404(Target, pk=target_id)

    try:
        UniApplicationEntry.objects.get(user=user, target=target)
        # repeat application, deny
        return {
                'is_allowed': False,
                'is_repeat': True,
                }
    except UniApplicationEntry.DoesNotExist:
        pass

    if request.method == 'POST':
        # We MUST provide user and target here, or ALL materials
        # would leak in case validation failed!!
        frm = UniApplyForm(
                request.POST,
                initial={
                    'user': user,
                    'target': target,
                    },
                )
        if frm.is_valid():
            with transaction.commit_on_success():
                entry = frm.save(commit=False)
                entry.user = user
                entry.target = target
                entry.save()
                frm.save_m2m()

            return redirect(my_view)
    else:
        frm = UniApplyForm(
                initial={
                    'user': user,
                    'target': target,
                    },
                )

    return {
            'is_allowed': True,
            'form': frm,
            }


@login_required
@quickview('uniapply/entry-detail.html')
def entry_detail_view(request, entry_id):
    user = request.user

    # XXX FIXME: target creator needs to be able to view entries!
    if not user.is_staff:
        entry_kwargs = {'user': user, }
    else:
        entry_kwargs = {}

    entry = get_object_or_404(
            UniApplicationEntry,
            pk=entry_id,
            **entry_kwargs
            )

    status, results, next_rule = get_auditing_status(entry)
    return {
            'user': user,
            'entry': entry,
            'a_status': status,
            'a_results': results,
            'a_next': next_rule,
            }


@login_required
@quickview('uniapply/entry-audit.html')
def entry_audit_view(request, entry_id, rule_id):
    user = request.user
    entry = get_object_or_404(
            UniApplicationEntry,
            pk=entry_id,
            )
    target = entry.target
    rule = get_object_or_404(
            AuditingRule,
            pk=rule_id,
            target=target,
            )

    if not is_auditer([rule, ], user):
        raise Http404

    if request.method == 'POST':
        frm = AuditForm(request.POST)
        if frm.is_valid():
            with transaction.commit_on_success():
                outcome = frm.save(commit=False)
                outcome.entry = entry
                outcome.rule = rule
                outcome.save()
            return redirect(entry_list_view, target.pk)
    else:
        frm = AuditForm()

    return {
            'user': user,
            'entry': entry,
            'form': frm,
            }


###
### EXPORT VIEWS
###

@login_required
@quickview('uniapply/export-target.html')
def target_export_view(request, target_id):
    user = request.user
    if not user.is_staff:
        target = get_object_or_404(Target,
                user=user,
                pk=target_id,
                )
    else:
        target = get_object_or_404(Target,
                pk=target_id,
                )

    entries = UniApplicationEntry.objects.filter(
            target=target,
            )

    render_agg_args = (request, target.identifier, )

    return {
            'entries': entries,
            'agg_args': render_agg_args,
            }


@login_required
def entry_export_view(request, entry_id):
    user = request.user

    # enable admins to export anyone's entry
    if user.is_staff:
        entry = get_object_or_404(
                UniApplicationEntry,
                pk=entry_id,
                )
    else:
        entry = get_object_or_404(
                UniApplicationEntry,
                pk=entry_id,
                user=user,
                )

    return render_object_to_response(
            request,
            entry,
            entry.target.template,
            aggregate=False,
            )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
