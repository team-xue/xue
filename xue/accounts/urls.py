from __future__ import unicode_literals

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from xue.accounts.forms import SignupFormExtra, LimitedEditProfileForm


urlpatterns = patterns('',
    (r'^signup/$', 'userena.views.signup',
        {'signup_form': SignupFormExtra, },
        ),
    (r'^(?P<username>[\.\w]+)/edit/$', 'userena.views.profile_edit',
        {'edit_profile_form': LimitedEditProfileForm, },
        ),

    (r'^', include('userena.urls')),
)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
