# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

# Django settings for Shop project.

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

ROOT = PROJECT_PATH

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'site@keksik.com.ua'
EMAIL_HOST_PASSWORD = '1q2w3e4r'

DEFAULT_FROM_EMAIL = 'Интернет магазин Кексик <subscribe@keksik.com.ua>'
MANAGERS = ADMINS

SERVER = os.path.isfile(path('server.key', ), )

if SERVER:
    Email_MANAGER = 'zakaz@keksik.com.ua'
else:
    Email_MANAGER = 'alex.starov@keksik.com.ua'

ALLOWED_HOSTS = ['*']
DEBUG = True
TEMPLATE_DEBUG = DEBUG

if os.path.isfile(path('server.mysql', ), ):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'keksik_com_ua',       # Or path to database file if using sqlite3.
            'USER': 'keksik_com_ua',       # Not used with sqlite3.
            'PASSWORD': '5ZqUcJdWzJbsc6pP',  # Not used with sqlite3.
            'HOST': '192.168.1.90',        # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                # Set to empty string for default. Not used with sqlite3.
            'OPTIONS': {
                'charset': 'utf8',
                'use_unicode': True, },
        }
    }
elif os.path.isfile(path('production.mysql', ), ):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'p_keksik_com_ua',    # Or path to database file if using sqlite3.
            'USER': 'p_keksik_com_ua',    # Not used with sqlite3.
            'PASSWORD': 'MbmwjhZeCyHPEX8c',        # Not used with sqlite3.
            'HOST': '192.168.1.12',                # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                        # Set to empty string for default. Not used with sqlite3.
        }
    }
elif os.path.isfile(path('server.pgsql', ), ):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'keksik_com_ua',       # Or path to database file if using sqlite3.
            'USER': 'keksik_com_ua',       # Not used with sqlite3.
            'PASSWORD': '5ZqUcJdWzJbsc6pP',  # Not used with sqlite3.
            'HOST': '192.168.1.12',        # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5432',                # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': path('db/shop_mk_ua.sqlite3', ),  # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

#from sys import platform
#if platform == 'win32':
#    DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#            'NAME': 'shop_mk_ua',            # Or path to database file if using sqlite3.
#            'USER': 'shop_mk_ua',          # Not used with sqlite3.
#            'PASSWORD': 'VTaCjL7vt69MQDfP',  # Not used with sqlite3.
#            'HOST': '192.168.1.88',        # Set to empty string for localhost. Not used with sqlite3.
#            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#        }
#    }
#elif platform == 'linux2':
#    DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2',
#                                             # 'mysql', 'sqlite3' or 'oracle'.
#            'NAME': 'shop_mk_ua',            # Or path to database file if using sqlite3.
#            'USER': 'postgres',                  # Not used with sqlite3.
#            'PASSWORD': 'secret',            # Not used with sqlite3.
#            'HOST': 'localhost',             # Set to empty string for localhost. Not used with sqlite3.
#            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.

#            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#            'NAME': 'shop_mk_ua',            # Or path to database file if using sqlite3.
#            'USER': 'root',                  # Not used with sqlite3.
#            'PASSWORD': 'secret',            # Not used with sqlite3.
#            'HOST': 'localhost',             # Set to empty string for localhost. Not used with sqlite3.
#            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#        }
#    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Kiev'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

#SITE_ID = 1

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

DEFAULT_CHARSET = 'utf-8'
DEFAULT_CONTENT_TYPE = 'text/html'
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = 'C:/Python27/Lib/site-packages/django/contrib/admin'
#import sys
#if sys.platform == 'win32':
#    MEDIA_ROOT = 'C:/Shop/media'
#elif sys.platform == 'linux2':
#    MEDIA_ROOT = 'Shop/media'
#MEDIA_ROOT = '/home/user/Proj/Shop/media'
#MEDIA_ROOT = '/home/user/PycharmProjects/Shop/media'
MEDIA_ROOT = path('media', )

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'C:/PycharmProjects/Shop/static'
#STATIC_ROOT = 'C:/Python27/Lib/site-packages/django/contrib/admin/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # 'C:/PycharmProjects/Shop/VirtEnv/lib/python2.7/site-packages/suit/static',
    # 'C:/Python27/Lib/site-packages/django/contrib/admin',
    # 'C:/Python27/Lib/site-packages/django/contrib/admin/static',
#    '/home/user/Proj/Shop/media',
#    '/home/user/Proj/media',
#    '/home/user/Proj/Shop/media',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # 'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^p()7zbza81@&amp;!bra3fvugv$=+zf*7&amp;$c)e(wpkl7=qg!vfx@$'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    # ('coffin.template.loaders.JinjaCachedLoader',
#    ('django.template.loaders.cached.Loader',
#     (
#         'jingo.Loader',
#         'django_jinja.loaders.AppLoader',
#         'django_jinja.loaders.FileSystemLoader',
         # 'django.template.loaders.app_directories.Loader',
         # 'django.template.loaders.filesystem.Loader',
         # 'django.template.loaders.filesystem.Loader',
         # 'django.template.loaders.app_directories.Loader',
         # 'django.template.loaders.eggs.Loader',
#     ),
#     ),
#)

#JINJA2_TEMPLATE_LOADERS = (
#    ('django.template.loaders.cached.Loader',
#     (
#         'django.template.loaders.app_directories.Loader',
#         'django.template.loaders.filesystem.Loader',
#     ),
#    ),
#)

#TEMPLATE_LOADERS = (
#    'coffin.template.loaders.JinjaCachedLoader',
#)


#DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja2'

JINGO_INCLUDE_PATTERN = r'\.jingo.html'

JINGO_EXCLUDE_APPS = ('debug_toolbar',
                      'django.contrib.admin',
                      'django.contrib.admindocs', )

#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
##    'django.template.loaders.eggs.Loader',
#)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS_ = TCP + (
    'django.core.context_processors.request',
)

TEMPLATE_CONTEXT_PROCESSORS_ += (
    'django.core.context_processors.csrf',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    # 'django.core.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    # Мой context processor
    'proj.context_processor.context',
    # 'compressor',
)

#JINJA2_EXTENSIONS = [
#    'compressor.contrib.jinja2ext.CompressorExtension',
#]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
    # Мой middleware
    'proj.processor_Middleware.Process_SessionIDMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'compat.midlewareHTMLCompress.SpacelessMiddleware',
)

SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 31622400  # 3600 * 24 * 366
#SESSION_COOKIE_DOMAIN = u'.shop.mk.ua'
#SESSION_ENGINE = 'cache_db'
#SESSION_ENGINE = 'db'
#SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

if SERVER:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '127.0.0.1:11211',
                # '172.19.26.240:11211',
                # '172.19.26.242:11211',
                # '172.19.26.244:11213',
                # 'LOCATION': 'unix:/tmp/memcached.sock',
            ]
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

CACHE_TIMEOUT = 30

ROOT_URLCONF = 'proj.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'proj.wsgi.application'


#TEMPLATE_DIRS = ('templates',
#                 'templates/jinja2',
#                 'jinja2', )

#DIRS = ['templates', ]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # 'nested_inlines',
    # 'nested_inlines', -> Вместо это установка пропатченого django
    # https://github.com/stefanklug/django/tree/nested-inline-support-1.5.x
    # Uncomment the next line to enable the admin:
    'suit',
    'suit_ckeditor',
#    'filebrowser',
    'django.contrib.admin',
    # 'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.admindocs',
    # 'django.contrib.markup', depricated in v. 1.6
    # 'south',
    'mptt',
    'django_mptt_admin',
    'django_jinja',
    #'bootstrap',
    #'bootstrap3',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'coffin',
    'apps.root',
    'apps.product',
    'apps.ajax',
    'apps.cart',
    'apps.comment',
    'apps.currency',
    # 'apps.extended_price',
    'apps.slide',
    'apps.static',
    'apps.calendar',
    'apps.search',
    'apps.utils',
    'apps.utils.setting',
    'apps.utils.captcha',
    'apps.utils.mediafile',
    'apps.handlers',
    'apps.adminSite',
    'apps.discount',
    'apps.coupon',
    'apps.callback',
    'apps.feedback',
    'apps.delivery',
    'paypal.standard.ipn',
    'apps.payment',
    # 'static_sitemaps',
)

PAYPAL_RECEIVER_EMAIL = "simagina.svetlana@gmail.com"
#SOUTH_MIGRATION_MODULES = {
#    'easy_thumbnails': 'easy_thumbnails.south_migrations',
#}
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'filters': {
#        'require_debug_false': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        }
#    },
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'filters': ['require_debug_false'],
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
#!!!=============== Python Social Auth =========================
INSTALLED_APPS += (
    'social.apps.django_app.default',
)

#try:
#    from proj.social_settings import *
#except:
#    pass

AUTHENTICATION_BACKENDS = (
    # 'social_auth.backends.twitter.TwitterBackend',
    # 'social_auth.backends.facebook.FacebookBackend',
    # 'social_auth.backends.google.GoogleOAuthBackend',
    # 'social_auth.backends.contrib.google.
    'social.backends.google.GoogleOAuth2',
    # 'social_auth.backends.yahoo.YahooBackend',
    # 'social_auth.backends.browserid.BrowserIDBackend',
    # 'social_auth.backends.contrib.linkedin.LinkedinBackend',
    # 'social_auth.backends.contrib.disqus.DisqusBackend',
    # 'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    # 'social_auth.backends.contrib.orkut.OrkutBackend',
    # 'social_auth.backends.contrib.foursquare.FoursquareBackend',
    # 'social_auth.backends.contrib.github.GithubBackend',
    'social.backends.yandex.YandexOAuth2',
    # 'social_auth.backends.contrib.yandex.YandexBackend',
    # 'social_auth.backends.contrib.yandex.YaruBackend',
    # 'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    # 'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiAppBackend',
    'social.backends.vk.VKOAuth2',
    # 'social_auth.backends.contrib.vkontakte.VKontakteOAuth2Backend',
    ####'social_auth.backends.contrib.vkontakte.VKontakteBackend',
    # 'social_auth.backends.contrib.live.LiveBackend',
    # 'social_auth.backends.contrib.skyrock.SkyrockBackend',
    # 'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    # 'social_auth.backends.contrib.readability.ReadabilityBackend',
    # 'social_auth.backends.OpenIDBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    # 'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS_ += (
    'social.apps.django_app.context_processors.backends',  # context_processors.social_auth_by_type_backends',
)

TWITTER_CONSUMER_KEY              = ''
TWITTER_CONSUMER_SECRET           = ''
FACEBOOK_APP_ID                   = ''
FACEBOOK_API_SECRET               = ''
LINKEDIN_CONSUMER_KEY             = ''
LINKEDIN_CONSUMER_SECRET          = ''
SKYROCK_CONSUMER_KEY              = ''
SKYROCK_CONSUMER_SECRET           = ''
ORKUT_CONSUMER_KEY                = ''
ORKUT_CONSUMER_SECRET             = ''
#OAuth2
GOOGLE_OAUTH2_CLIENT_ID = '442207703537.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'R6RYIo1b6w8oQvtR-duuGRPo'
GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
#
SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = True
SOCIAL_AUTH_DEFAULT_USERNAME = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
LOGIN_ERROR_URL = '/login/error/'
#OpenAPI
VKONTAKTE_APP_ID = ''  # '3474809'
VKONTAKTE_APP_SECRET = ''  # 'BapEJeIg9oRgfXRQABor'
# Usage for applications auth: {'key': application_key, 'user_mode': 0 (default) | 1 (check) | 2 (online check) }
# 0 means is_app_user request parameter is ignored, 1 - must be = 1, 2 - checked via VK API request (useful when user
# connects to your application on app page and you reload the iframe)
VKONTAKTE_APP_AUTH = None
ODNOKLASSNIKI_OAUTH2_CLIENT_KEY = '163445760'
ODNOKLASSNIKI_OAUTH2_APP_KEY = 'CBANPOLKABABABABA'
ODNOKLASSNIKI_OAUTH2_CLIENT_SECRET = '5E0652D81620317290DED086'
MAILRU_OAUTH2_CLIENT_KEY   		  = ''
MAILRU_OAUTH2_APP_KEY      		  = ''
MAILRU_OAUTH2_CLIENT_SECRET       = ''
#SOCIAL_AUTH_USER_MODEL           = 'app.CustomUser'
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
GITHUB_APP_ID                     = ''
GITHUB_API_SECRET                 = ''
FOURSQUARE_CONSUMER_KEY           = ''
FOURSQUARE_CONSUMER_SECRET        = ''
DOUBAN_CONSUMER_KEY               = ''
DOUBAN_CONSUMER_SECRET            = ''
YANDEX_OAUTH2_CLIENT_KEY = '9827973f694743c493d9d3b0ca75ef9a'
YANDEX_OAUTH2_CLIENT_SECRET = '9fd1bd404b25435b951b95a28ed96ed6'
YANDEX_OAUTH2_API_URL = 'https://api-yaru.yandex.ru/me/'  # http://api.moikrug.ru/v1/my/ for Moi Krug
DAILYMOTION_OAUTH2_KEY            = ''
DAILYMOTION_OAUTH2_SECRET         = ''
SHOPIFY_APP_API_KEY               = ''
SHOPIFY_SHARED_SECRET             = ''
STOCKTWITS_CONSUMER_KEY           = ''
STOCKTWITS_CONSUMER_SECRET        = ''
READABILITY_CONSUMER_KEY          = ''
READABILITY_CONSUMER_SECRET       = ''

# Backward compatibility
#YANDEX_APP_ID = YANDEX_OAUTH2_CLIENT_KEY
#YANDEX_API_SECRET = YANDEX_OAUTH2_CLIENT_SECRET

#OAuth2
VK_APP_ID = '3474809'
VK_API_SECRET = 'BapEJeIg9oRgfXRQABor'
VK_EXTRA_DATA = ['city', 'country', 'contacts', 'home_phone', 'mobile_phone', ]

#VK_APP_ID = VKONTAKTE_APP_ID
#VK_API_SECRET = VKONTAKTE_APP_SECRET
# VKONTAKTE_APP_AUTH={'key':'iframe_app_secret_key', 'user_mode': 2, 'id':'iframe_app_id'}

#SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    # 'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    # 'social_auth.backends.pipeline.misc.save_status_to_session',
    # 'app.pipeline.redirect_to_form',
    # 'app.pipeline.username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)
#!!!--------------- Widget ---------------------------------
INSTALLED_APPS += (
    'compat.social_auth_widget',
)
SOCIAL_AUTH_PROVIDERS = [
    {'id': p[0], 'name': p[1], 'position': {'width': p[2][0], 'height': p[2][1], }}
    for p in (
        ('github', u'Login via GitHub', (0, -70), ),
        ('facebook', u'Login via Facebook', (0, 0), ),
        ('twitter', u'Login via Twitter', (0, -35), ),
    )
]
#!!!=============== Django Userena =========================
AUTH_USER_MODEL = 'authModel.User'
#AUTH_USER_MODEL = 'auth.User'
INSTALLED_APPS += (
    'userena',
    'guardian',
    'easy_thumbnails',
    'apps.account',
    'apps.authModel',
)
AUTHENTICATION_BACKENDS += (
    'django.contrib.auth.backends.ModelBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
)
USERENA_DISABLE_PROFILE_LIST = True
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'account.UserProfileModel'
USERENA_DEFAULT_PRIVACY = 'closed'
#USERENA_SIGNIN_REDIRECT_URL = '/accounts/%(username)s/signin/'
USERENA_SIGNIN_REDIRECT_URL = '/'
#LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
#!!!=============== Django Userena uMessages =========================
INSTALLED_APPS += (
    'userena.contrib.umessages',
)
USERENA_USE_MESSAGES = True
#!!!=============== Django ToolBar ===================================
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.panel.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
)
#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.version.VersionDebugPanel',
#    'debug_toolbar.panels.timer.TimerDebugPanel',
##    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#    'debug_toolbar.panels.cache.CacheDebugPanel',
#    'debug_toolbar.panels.signals.SignalDebugPanel',
##    'debug_toolbar.panels.logger.LoggingPanel',
#)

DEBUG_TOOLBAR_PANELS += (
    'debug_toolbar.panels.profiling.ProfilingPanel',
)

#INSTALLED_APPS += (
#    'debug_toolbar_htmltidy',
#)

#DEBUG_TOOLBAR_PANELS += (
#    'debug_toolbar_htmltidy.panels.HTMLTidyDebugPanel',
#)

#INSTALLED_APPS += (
#    'debug_toolbar_autoreload',
#)

#DEBUG_TOOLBAR_PANELS += (
#    'debug_toolbar_autoreload.AutoreloadPanel',
#)

DEBUG_TOOLBAR_FILTER_URL = ('^admin/', )

INSTALLED_APPS += (
    'template_timings_panel',
)

DEBUG_TOOLBAR_PANELS += (
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
)

IGNORED_TEMPLATES = ["debug_toolbar/*"]

#INSTALLED_APPS += (
#    'memcache_toolbar',
#)

#DEBUG_TOOLBAR_PANELS += (
#    'memcache_toolbar.panels.memcache.MemcachePanel',
#)

#    'debug_toolbar.panels.version.VersionDebugPanel',
#    'debug_toolbar.panels.timer.TimerDebugPanel',
#    'debug_toolbar.panels.settings.SettingsPanel',
##    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.profiling.ProfilingPanel',
#    'debug_toolbar.panels.redirects.RedirectsPanel',
#    'debug_toolbar.panels.request.RequestPanel',
#    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#    'debug_toolbar.panels.cache.CacheDebugPanel',
#    'debug_toolbar.panels.signals.SignalDebugPanel',
#    'debug_toolbar.panels.logging.LoggingPanel',


#def show_toolbar(request):
#    return not request.is_ajax() and request.user and request.user.username == "admin"

DEBUG_TOOLBAR_CONFIG = {
    'EXCLUDE_URLS': ('/admin/', ),  # данная опция находится в разработке
    'HIDE_FILTER_URL': '^/admin/',  # данная опция находится в разработке
    'INTERCEPT_REDIRECTS': False,
#    'SHOW_TOOLBAR_CALLBACK': 'proj.settings.show_toolbar',
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = ('213.227.250.34/32', '172.22.0.0/16', '192.168.0.0/16', '10.0.0.0/8', '217.77.210.70', '127.0.0.1', )
#                '46.33.254.179', )
#!!!=============== Django ToolBar ===================================
#INSTALLED_APPS = (
#    'static_sitemaps',
#)
#
#STATICSITEMAPS_ROOT_SITEMAP = 'media.sitemap'

from django_jinja.builtins import DEFAULT_EXTENSIONS

TEMPLATES = [
    {
        # "BACKEND": "django.template.backends.jinja2.Jinja2",
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [os.path.join(PROJECT_PATH, 'jinja2', ), ],
        "APP_DIRS": True,
        "OPTIONS": {
            # 'environment': 'proj.jinja2.environment',
            "match_extension": ".jinja2",
            "match_regex": r"^(?!admin/).*",  # this is additive to match_extension
            "context_processors": TEMPLATE_CONTEXT_PROCESSORS_,
            "extensions": DEFAULT_EXTENSIONS + [
                # Your extensions here...
                "apps.utils.templatetags.cache.DjangoJinjaCacheExtension"
            ]
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_PATH, 'templates', ), ],
        "APP_DIRS": True,
        "OPTIONS": {
            #'loaders': [
            #    ('django.template.loaders.cached.Loader',
            #     [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #     ],
            #     ),
            #],
            # "match_extension": ".html",
            "context_processors": TEMPLATE_CONTEXT_PROCESSORS_,
        }
    },
]


try:
    from local_settings import *
except ImportError:
    pass

try:
    from keksik import *
except ImportError:
    pass

try:
    from chipdip import *
except ImportError:
    pass
