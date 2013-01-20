# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.db import transaction

from xue.common.decorators import quickview

@quickview('tutor/proj_reg.html')
def register_view(request):
    return {
             }

@quickview('tutor/proj_list.html')
def list_view(request):
    return {
             }

@quickview('tutor/proj_detail.html')
def detail_view(request, proj_id):
    return {
             }

@quickview('tutor/proj_apply.html')
def apply_view(request, proj_id):
    return {
             }


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
