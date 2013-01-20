# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import redirect, get_object_or_404
from django.db import transaction

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from xue.common import choices as xue_choices
from xue.common.decorators import quickview, limit_role

from xue.materials.models import MaterialEntry
from xue.materials.forms import AddMaterialForm, EditMaterialForm


@login_required
@quickview('materials/index.html')
def homepage_view(request):
    return {}


@login_required
@quickview('materials/list.html')
def list_mine_view(request):
    usr = request.user
    entries = MaterialEntry.objects.filter(user=usr)

    return {
            'entries': entries,
            }


@login_required
@quickview('materials/list.html')
def list_view(request, userid):
    usr, entries = request.user, []
    requested_usr = get_object_or_404(User, username=userid)

    # TODO: proper customizable access control
    if not usr.is_staff:
        return redirect('xue.materials.views.list_mine_view')

    entries = MaterialEntry.objects.filter(user=requested_usr)

    return {
            'entries': entries,
            }


@login_required
@quickview('materials/add.html')
def add_view(request):
    usr = request.user

    if request.method == 'POST':
        frm = AddMaterialForm(request.POST)
        if frm.is_valid():
            with transaction.commit_on_success():
                entry = frm.save(commit=False)
                entry.user = usr
                entry.save()

            return redirect('xue.materials.views.homepage_view')
    else:
        frm = AddMaterialForm()

    return {
            'form': frm,
            }


@login_required
@quickview('materials/detail.html')
def detail_view(request, entry_id):
    # this can't be AnonymousUser, so we won't run into int() problems here
    usr = request.user
    entry = get_object_or_404(MaterialEntry, id=entry_id)

    # TODO: proper access control
    if not usr.is_staff and entry.user != usr:
        # not authored by self and user is not staff, deny access
        return {
                'access_granted': False,
                'is_my_material': False,
                'entry': None,
                'paragraphs': None,
                }

    # break content into paragraphs for sake of readability
    content = entry.content
    paragraphs = content.split('\n')

    return {
            'access_granted': True,
            'is_my_material': entry.user == usr,
            'entry': entry,
            'paragraphs': paragraphs,
            }


@login_required
@quickview('materials/edit.html')
def edit_view(request, entry_id):
    usr = request.user
    # ensure only the author him/herself can edit his/her own material
    entry = get_object_or_404(
            MaterialEntry,
            pk=entry_id,
            user=usr,
            # a user cannot edit locked material
            is_locked=False,
            )

    if request.method == 'POST':
        frm = EditMaterialForm(request.POST)
        if frm.is_valid():
            entry.title = frm.cleaned_data['title']
            entry.content = frm.cleaned_data['content']
            entry.save()

            return redirect('xue.materials.views.detail_view', entry.pk)
    else:
        # this is subtly different from AddMaterialForm in that giving
        # initial values is not only possible but mandatory
        frm = EditMaterialForm(
                initial={
                    'title': entry.title,
                    'content': entry.content,
                    },
                )

    return {
            'form': frm,
            }



# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
