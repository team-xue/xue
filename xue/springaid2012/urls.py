from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'springaid2012.views.application_view'),
    url(r'^ok/$', 'springaid2012.views.submitted_view'),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
