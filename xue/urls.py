from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xue.views.home', name='home'),
    # url(r'^xue/', include('xue.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns(
            '',
            url(
                r'^' + settings.MEDIA_URL.lstrip('/'),
                include('appmedia.urls')
                ),
            ) + urlpatterns


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8
