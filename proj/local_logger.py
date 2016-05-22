# -*- coding: utf-8 -*-

__author__ = 'AlexStarov'


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

CELERYD_HIJACK_ROOT_LOGGER = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'all_verbose': {
            'format': '%(asctime)s - %(levelname)s | %(module)s %(process)d %(thread)d | %(name)s - %(filename)s:%(lineno)d | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'main': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'production': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '../logs/keksik_com_ua/logging/production.log',
            'when': 'd',
            'backupCount': 7,
            'formatter': 'main',
            # 'filters': ['require_debug_false'],
        },
        'log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '../logs/keksik_com_ua/logging/log.log',
            'when': 'd',
            'backupCount': 7,
            'formatter': 'main',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '../logs/keksik_com_ua/logging/debug.log',
            'when': 'd',
            'backupCount': 7,
            'formatter': 'main',
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '../logs/keksik_com_ua/logging/celery.log',
            'when': 'd',
            'backupCount': 7,
            'formatter': 'all_verbose',
        },
        #'celery_sentry_handler': {
        #    'level': 'ERROR',
        #    'class': 'core.log.handlers.CelerySentryHandler',
        #    'when': 'd',
        #    'backupCount': 7,
        #    'formatter': 'all_verbose',
        #},
        'null': {
            "class": 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'log', ],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'production', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'debug': {
            'handlers': ['debug', ],
        },
        'celery': {
            'handlers': ['celery', ],
            'level': 'ERROR',
        },
        #'celery': {
        #    'handlers': ['celery_sentry_handler', 'celery', ],
        #    'level': 'ERROR',
        #},
        '': {
            'handlers': ['log', ],
            'level': "DEBUG",
        },
    }
}
