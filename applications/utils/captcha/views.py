# coding=utf-8

import random
from datetime import datetime
from django.db import connection, transaction, IntegrityError
from django.http import HttpResponse

from proj.settings import SERVER

from .models import Captcha_Images, Captcha_Key
from .utils import key_generator
from django.conf import settings
#from jinja2 import Environment, FileSystemLoader
#template_dirs = getattr(settings, 'TEMPLATE_DIRS', )
#env = Environment(loader=FileSystemLoader(template_dirs, ), )

#default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE', )
#def render_to_response(request, filename, context={}, mimetype=default_mimetype, ):
#    template = env.get_template(filename, )
#    if request:
#        context['request'] = request
#        context['user'] = request.user
#    rendered = template.render(**context)
#    from django.http import HttpResponse
#    return HttpResponse(rendered, mimetype=mimetype, )

#def greater_than_fifty(x, ):
#    return x > 50
#env.tests['gtf'] = greater_than_fifty

# from django.shortcuts import render_to_response
# from django.template import RequestContext
# import settings
# import os

__author__ = 'Sergey'
# Create your views here.


class Captcha_Image(object, ):
    def __init__(self, filename=None, ):
        # self._chek_store_dir()
        if filename:
            from applications.utils.captcha.models import Captcha_Key
            key = Captcha_Key.objects.get(key=filename, )
            # Находим как называется настоящий файл.
            self.filename = key.image.image.path
            self.key = key.update
            # self.img = self._read()

    # def _check_store_dir(self):
    #     if not os.path.isdir(settings.CAPTCHA_STORE):
    #         os.mkdir(settings.CAPTCHA_STORE, 755)

    # def _read(self):
    #     try:
    #         path = os.path.join(settings.CAPTCHA_STORE, self.filename, )
    #         return ''.join(file(path, 'r', ), )
    #     except Exception:
    #         return None

    def draw(self, response, ):
        from PIL import Image
        # filename = self.filename
        # Foreign_Key_image = filename.image
        # image = Foreign_Key_image.image
        # path = image.path
        # name = image.name
        # print(self.filename.image, self.filename.image.path, self.filename.image.name, )
        img = Image.open(self.filename, mode="r", )
        img.save(response, 'JPEG', )


def captcha_image_show(request, filename=None, ):
    response = HttpResponse(mimetype='image/jpg', )
    captcha_image = Captcha_Image(filename, )
    captcha_image.draw(response, )
    return response


def Captcha(request=None, ):
    # len_Image_Type = len(Captcha_Images.Image_Type, )
    """ Выясняем какой ТИП картинки будет являтся "правдой" """
    # true = randint(1, len_Image_Type, )
    true = random.choice(Captcha_Images.Image_Type, )[0]
    # import datetime
    # timedelta = datetime.datetime.now() + datetime.timedelta(3600)
    """ Пытаемся взять все ключи которые соответсвуют выбранному нами ТИПА картинки
    и доступные в этот период времени """
    # __lte - меньше или равно
    qs_true = Captcha_Key.objects.filter(image_type=true, next_use__lte=datetime.now(), )
    """ Если нет, то генерим ключи """
    if not qs_true:
        qs_true = Captcha_Key_Generates(what_return=true, )
    if len(qs_true, ) < 100:
        Captcha_Key_Generates()
    """ Выбираем случайным образом "правильную" картинку """
    # len_qs_true = len(qs_true, )
    # true = randint(0, len_qs_true, )
    # true = qs_true[true]
    true = random.choice(qs_true, )
    # print(true.key)
    """ сохраняем "правильный код" в Session """
    if request:
        request.session['capcha'] = true.key
    """ Начинаем формировать "ответ" """
    dict = {}
    """ Берем "не правильные ключи" исключая ключи с "правильным" типом картинки """
    not_true = Captcha_Key.objects.filter(next_use__lte=datetime.now(), ).exclude(image_type=true.image_type, )
    keys = {}
    if len(not_true, ) > 12:
        keys[0] = random.choice(not_true, )
        not_true = not_true.exclude(image_type=keys[0].image_type, )
        if len(not_true, ) > 2:
            keys[1] = random.choice(not_true, )
    """ Формируем словарь с 3-мя ключами - 1-ним "правильным" и 2-мя "неправильными" """
    true_rand = random.randint(0, 2, )
    i = 0
    for n in range(0, 3, ):
        if n == true_rand:
            dict[n] = true
        else:
            dict[n] = keys[i]
            i = +1
    return dict


@transaction.atomic
def Captcha_Key_Generates(what_return=None, ):
    all_images = Captcha_Images.objects.all()
    len_all_images = len(all_images, )
    # from django.db import transaction
    # with transaction.atomic():
    # datetime_start = datetime.now()
    # print datetime_start
    if SERVER:
        ins = '''insert into Captcha_Keys (`key`, image_id, image_type, next_use, created_at, updated_at)
               values ('%s', %d, %d, NOW(), NOW(), NOW())'''
    else:
        ins = '''insert into Captcha_Keys (key, image_id, image_type, next_use, created_at, updated_at)
               values ('%s', %d, %d, datetime('now'), datetime('now'), datetime('now'))'''
    cursor = connection.cursor()

    success = 0
    unsuccess = 0

    for n in range(1, 100, ):
        choice = random.randint(1, len_all_images, )
        # print(n, choice, len_all_images)
        image = all_images[choice - 1]
        """
            Создаем новую запись ключа подставляя в эту запись только реальный путь к картинке.
            Ключ при этом генерится автоматически в самой модели.
        """
        ok = True
        while ok:
            """
                IntegrityError:
            """
            key = key_generator(size=8, )
            # print success, unsuccess, n, choice, type(image.pk), image.pk, type(image.image_type), image.image_type, key
            insert = ins % (  # Captcha_Key.model._meta.db_table,
                            key,
                            image.pk,
                            image.image_type, )
            try:
                with transaction.atomic():
#                    print insert
                    cursor.execute(insert, )
                    # Captcha_Key.objects.create(image=image, )
            except IntegrityError:
                print('IntegrityError', ' Key: ', key, )
                unsuccess += 1
            except Exception as inst:
                print('captcha/views.py: 175: ', type(inst, ), )
                print('captcha/views.py: 175: ', inst, )
                unsuccess += 1
            else:
                success += 1
                ok = False
    # datetime_end = datetime.now()
    # print datetime_start, ' - ', datetime_end
    # time_to_next_use = datetime.datetime.now() - datetime.timedelta(3600)
    # __lte - меньше или равно
    if what_return:
        return Captcha_Key.objects.filter(image_type=what_return, next_use__lte=datetime.now(), )
    else:
        return None


def Captcha_Key_Deletes(key=None, datetime=None, ):
    if key:
        try:
            Captcha_Key.objects.get(key=key).delete()
        except Captcha_Key.DoesNotExist:
            return None
    elif datetime:
        try:
            Captcha_Key.objects.filter(created_at__lte=datetime, ).delete()
        except Captcha_Key.DoesNotExist:
            return None
    else:
        try:
            Captcha_Key.objects.all().delete()
        except Captcha_Key.DoesNotExist:
            return None
    return None
