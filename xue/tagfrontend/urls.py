from __future__ import unicode_literals

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', 'xue.tagfrontend.views.tag_list_view'),
    url(r'^(?P<tag_id>\d+)/$', 'xue.tagfrontend.views.tag_view'),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
