from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'xue.uniapply.views.index_view'),
    url(r'^list/$', 'xue.uniapply.views.target_list_view'),
    url(r'^my/$', 'xue.uniapply.views.my_view'),

    url(r'^item/(?P<target_id>\d+)/$', 'xue.uniapply.views.target_detail_view'),
    url(r'^item/(?P<target_id>\d+)/apply/$', 'xue.uniapply.views.apply_view'),
    url(r'^item/(?P<target_id>\d+)/entries/$', 'xue.uniapply.views.entry_list_view'),
    url(r'^item/(?P<target_id>\d+)/export/$', 'xue.uniapply.views.target_export_view'),

    url(r'^entry/(?P<entry_id>\d+)/$', 'xue.uniapply.views.entry_detail_view'),
    url(r'^entry/(?P<entry_id>\d+)/audit/(?P<rule_id>\d+)/$', 'xue.uniapply.views.entry_audit_view'),
    url(r'^entry/(?P<entry_id>\d+)/export/$', 'xue.uniapply.views.entry_export_view'),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
