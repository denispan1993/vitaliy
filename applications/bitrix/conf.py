import os
from django.conf import settings
from django.apps import AppConfig


class CMLAppCong(AppConfig):

    name = 'applications.bitrix'
    verbose_name = "Import&Export Bitrix"

    RESPONSE_SUCCESS = 'success'
    RESPONSE_PROGRESS = 'progress'
    RESPONSE_ERROR = 'failure'

    MAX_EXEC_TIME = 60
    USE_ZIP = False
    FILE_LIMIT = 0

    UPLOAD_ROOT = os.path.join(settings.MEDIA_ROOT, 'cml', 'tmp')

    DELETE_FILES_AFTER_IMPORT = True
