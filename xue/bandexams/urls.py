from __future__ import unicode_literals

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', 'xue.bandexams.views.my_view'),
    url(r'add/$', 'xue.bandexams.views.add_view'),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
