#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Project Xue
# Production settings
# XXX same as debug setting atm

from os.path import abspath, dirname
from os.path import join as pathjoin

gettext = lambda s: s
PROJECT_PATH = abspath(dirname(__file__))

# Site settings separated from main settings module
from sitesettings import *


SOUTH_DATABASE_ADAPTERS = {
        'default': 'south.db.postgresql_psycopg2',
        }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

LANGUAGES = [
    ('zh_cn', 'Chinese (Simplified)'),
     ('en', 'English'),
]

DEFAULT_LANGUAGE = 1

CMS_LANGUAGE_CONF = {
    'en':['zh_cn'],
    'zh_cn':['en'],
}

CMS_SITE_LANGUAGES = {
    1:['zh_cn', 'en'],
}

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'xue.middleware.timing.TimingMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # django-cms
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    # XXX toolbar has security risk!! it exposes template dir's real path..
    # Let's restrict its visibility then...
    # UPDATE: It won't let toolbar show if not user.is_staff(), so I'd
    # re-enable it for sake of convenience
    # XXX AGAIN not the case... it's been VERY annoying at times, plus
    # its .button class interfered with my CSS. Disable. Period.
#    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
#    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.dummylang.DummyMultilingualURLMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'xue.urls'

TEMPLATE_DIRS = (
    pathjoin(PROJECT_PATH, 'templates').replace('\\', '/'),
)

# django-cms templates
CMS_TEMPLATES = (
    # format: ('<filename>', '<template name>'),
    (pathjoin(PROJECT_PATH, 'templates/homepage.html').replace('\\', '/'),
     'Homepage'),

    (pathjoin(PROJECT_PATH, 'templates/section.html').replace('\\', '/'),
     'Section'),

    (pathjoin(PROJECT_PATH, 'templates/article.html').replace('\\', '/'),
     'Article'),

    (pathjoin(PROJECT_PATH, 'templates/gallery.html').replace('\\', '/'),
     'Photo Gallery'),

    (pathjoin(PROJECT_PATH, 'templates/tech-dept.html').replace('\\', '/'),
     'Tech Department'),

    (pathjoin(PROJECT_PATH, 'templates/art-dept.html').replace('\\', '/'),
     'Art Department'),
)

# Limit the various specialized pages' placeholder content
CMS_PLACEHOLDER_CONF = {
        'gallery-photos': {
                           'plugins': ('PicturePlugin', ),
                           },
        }

# django-cms template processors...
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'cms.context_processors.media',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'accounts.DMUserProfile'

ANONYMOUS_USER_ID = -1

USERENA_HIDE_EMAIL = True
USERENA_ACTIVATION_REQUIRED = True

# Comment system
COMMENTS_APP = 'xue.limitedcomment'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin interface is needed by django-cms.
    'django.contrib.admin',

    # Comments for various interactive features
    'django.contrib.comments',

    # django-cms apps
    'cms',
    'mptt',
    'menus',
    'south',
    'appmedia',
    'tinymce',

    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.flash',
    'cms.plugins.video',

    'userena',
    'easy_thumbnails',
    'guardian',

    'accounts',
    'xue.springaid2012',
    'xue.tutor',
    'xue.common',
    'xue.classes',
    'xue.scores',

    'xue.infocenter',
    'xue.materials',
    'xue.bandexams',
    'xue.impexp',

    'xue.uniapply',
    'xue.auditlock',

    # tag frontend...
    'xue.tagfrontend',

    # limited comment
    'xue.limitedcomment',
)

# Page title and other SEO things...
CMS_SEO_FIELDS = True

# homebrew tagging support...
CMS_TAGS = True

# disable tinymce to restrict usual editor's tendency to use colors, etc
# seems the leaders are not particularly fond of simplicity...
CMS_USE_TINYMCE = True

# show_{start,end}_date, may be useful so enable these early
CMS_SHOW_START_DATE = CMS_SHOW_END_DATE = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8
