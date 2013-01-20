# -*- coding: utf-8 -*-
from cms.utils.i18n import get_default_language
from django.conf import settings
from django.core.urlresolvers import reverse
from django.middleware.locale import LocaleMiddleware
from django.utils import translation
import re
import urllib

class DummyMultilingualURLMiddleware(object):
    def get_language_from_request (self,request):
        return 'zh_cn'
    
    def process_request(self, request):
        language = self.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = language

    def process_response(self, request, response):
        return response
