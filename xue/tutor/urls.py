from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'xue.tutor.views.mainpage_view'),

    url(r'^review/$', 'xue.tutor.views.application_list_view'),
    url(r'^review/all/$', 'xue.tutor.views.applicant_overview_csv_view'),
    url(r'^review/(?P<entry_id>\d+)/$', 'xue.tutor.views.review_view'),

    url(r'^apply/preliminary/$', 'xue.tutor.studentviews.apply_view'),
    url(r'^apply/secondary/$', 'xue.tutor.studentviews.selectproj_view'),

    url(r'^project/$', 'xue.tutor.views.project_list_view'),
    url(r'^project/(?P<proj_id>\d+)/$', 'xue.tutor.views.project_detail_view'),

    url(r'^project/reg/$', 'xue.tutor.projviews.register_view'),

    url(r'^project/admin/$', 'xue.tutor.teacherviews.listpage_view'),
    url(r'^project/(?P<proj_id>\d+)/admin/$', 'xue.tutor.teacherviews.projectpage_view'),
    url(r'^project/(?P<proj_id>\d+)/admin/sel/$', 'xue.tutor.teacherviews.pickinglist_view'),
    url(r'^project/(?P<proj_id>\d+)/admin/sel/(?P<entry_id>\d+)/$', 'xue.tutor.teacherviews.picking_view'),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
