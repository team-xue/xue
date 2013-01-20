from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'xue.materials.views.homepage_view'),
    url(r'^list/$', 'xue.materials.views.list_mine_view'),
    url(
        r'^list/(?P<userid>[A-Za-z0-9_.]+)/$',
        'xue.materials.views.list_view',
        ),

    url(r'^add/$', 'xue.materials.views.add_view'),
    url(r'^(?P<entry_id>\d+)/$', 'xue.materials.views.detail_view'),
    url(r'^(?P<entry_id>\d+)/edit/$', 'xue.materials.views.edit_view'),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
