from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'xue.infocenter.views.detail_view'),

    url(r'edit/$', 'xue.infocenter.views.edit_view'),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
