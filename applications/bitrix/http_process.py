from __future__ import absolute_import
import os
import logging
from celery.utils import uuid
from datetime import datetime, date
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile

from proj import settings
from .status_process import error, success
from .tasks import process_bitrix_import_xml, process_bitrix_offers_xml

logger = logging.getLogger(__name__)


def get_filename(request):
    try:
        return request.GET['filename']
    except KeyError:
        return error(request, 'Need a filename param!')


def file_path():
    return '{root}/{app}/{year}/{month:02d}/{day:02d}/' \
        .format(root=settings.CML_UPLOAD_ROOT,
                app=settings.CML_APP,
                year=date.today().year, month=date.today().month, day=date.today().day, )


def get_filename_from_storage(request):
    filename = get_filename(request).split('.')

    path = file_path()

    for name in os.listdir(path, ):
        path_and_filename = os.path.join(path, name)

        if os.path.isfile(path_and_filename, )\
                and name.split('.')[0] == filename[0]\
                and name.split('.')[-1] == filename[-1]:
            yield path_and_filename


def set_filename(request):
    filename = get_filename(request).split('.')
    return '{filename}.{hour:02d}.{minute:02d}.{ext}' \
        .format(filename=filename[0],
                hour=datetime.now().hour,
                minute=datetime.now().minute,
                ext=filename[1], )


def init(request):
    result = 'zip={}\nfile_limit={}'.format('yes' if settings.CML_USE_ZIP else 'no',
                                            settings.CML_FILE_LIMIT)
    print(result)
    return HttpResponse(result)


def upload_file(request):
    if request.method != 'POST':
        return error(request, 'Wrong HTTP method!')

    filename = set_filename(request)
    path = file_path()
    print(filename)
    print(path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            return error(request, 'Can\'t create upload directory!')

    filename = os.path.basename(filename)
    print(filename)
    temp_file = SimpleUploadedFile(filename, request.read(), content_type='text/xml')
    print(temp_file)
    with open(os.path.join(path, filename), 'wb') as f:
        for chunk in temp_file.chunks():
            f.write(chunk)

    return success(request)


def import_file(request):

    filename = get_filename(request)
    print('filename', filename)
    for path_and_filename in get_filename_from_storage(request):

        print(path_and_filename)

        if not os.path.exists(path_and_filename):
            return error(request, 'File does\'nt exists!')

        if filename == 'import.xml':
            """ Запуск задачи обработки импортируемых файлов """
            process_bitrix_import_xml \
                .apply_async(queue='celery',
                             kwargs={'path_and_filename': path_and_filename, },
                             task_id='celery-task-id-{0}'.format(uuid(), ),
                             countdown=5, )

        elif filename == 'offers.xml':

            # import_manager = ImportManager(file_path, )
            # try:
            #     import_manager.import_all()
            # except Exception as e:
            #     return error(request, str(e))

            # if settings.CML_DELETE_FILES_AFTER_IMPORT:
            #     try:
            #         os.remove(path)
            #     except OSError:
            #         logger.error('Can\'t delete file after import: {}'.format(path))
            # Exchange.log('import', request.user, filename)

            """ Запуск задачи обработки импортируемых файлов """
            # process_bitrix_offers_xml \
            #     .apply_async(queue='celery',
            #                  path_and_filename=path_and_filename,
            #                  task_id='celery-task-id-{0}'.format(uuid(), ),
            #                  countdown=60, )

    return success(request)


def export_query(request):
    # export_manager = ExportManager()
    # export_manager.export_all()
    return HttpResponse(  # export_manager.get_xml(),
        content_type='text/xml')


def export_success(request):
    # export_manager = ExportManager()
    # Exchange.log('export', request.user)
    # export_manager.flush()
    return success(request)
