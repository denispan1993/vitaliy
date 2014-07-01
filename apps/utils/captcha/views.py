# coding=utf-8
__author__ = 'Sergey'

# Create your views here.
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


class Captcha_Image(object, ):
    def __init__(self, filename=None, ):
        # self._chek_store_dir()
        if filename:
            from apps.utils.captcha.models import Captcha_Key
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
    from django.http import HttpResponse
    response = HttpResponse(mimetype='image/jpg', )
    captcha_image = Captcha_Image(filename, )
    captcha_image.draw(response, )
    return response

import string
import random


def key_generator(size=8, chars=string.ascii_letters + string.digits, ):
    return ''.join(random.choice(chars) for _ in range(size))


def Captcha(request=None, ):
    from apps.utils.captcha.models import Captcha_Images, Captcha_Key
    # len_Image_Type = len(Captcha_Images.Image_Type, )
    from random import randint, choice
    """ Выясняем какой ТИП картинки будет являтся "правдой" """
    # true = randint(1, len_Image_Type, )
    true = choice(Captcha_Images.Image_Type, )[0]
    # import datetime
    # timedelta = datetime.datetime.now() + datetime.timedelta(3600)
    from datetime import datetime
    """ Пытаемся взять все ключи которые соответсвуют выбранному нами ТИПА картинки
    и доступные в этот период времени """
    # __lte - меньше или равно
    qs_true = Captcha_Key.objects.filter(image_type=true, next_use__lte=datetime.now(), )
    """ Если нет, то генерим ключи """
    if not qs_true:
        qs_true = Captcha_Key_Generates(true=true, )
    if len(qs_true, ) < 100:
        Captcha_Key_Generates()
    """ Выбираем случайным образом "правильную" картинку """
    # len_qs_true = len(qs_true, )
    # true = randint(0, len_qs_true, )
    # true = qs_true[true]
    true = choice(qs_true, )
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
        keys[0] = choice(not_true, )
        not_true = not_true.exclude(image_type=keys[0].image_type, )
        if len(not_true, ) > 2:
            keys[1] = choice(not_true, )
    """ Формируем словарь с 3-мя ключами - 1-ним "правильным" и 2-мя "неправильными" """
    true_rand = randint(0, 2, )
    i = 0
    for n in range(0, 3, ):
        if n == true_rand:
            dict[n] = true
        else:
            dict[n] = keys[i]
            i = +1
    return dict


def Captcha_Key_Generates(what_return=None, ):
    from apps.utils.captcha.models import Captcha_Images, Captcha_Key
    all_images = Captcha_Images.objects.all()
    len_all_images = len(all_images, )
    from random import randint
    for n in range(1, 100, ):
        choice = randint(1, len_all_images, )
        # print(n, choice, len_all_images)
        image = all_images[choice - 1]
        Captcha_Key.objects.create(image=image, )
    # import datetime
    from datetime import datetime
    # time_to_next_use = datetime.datetime.now() - datetime.timedelta(3600)
    # __lte - меньше или равно
    if what_return:
        return Captcha_Key.objects.filter(image_type=what_return, next_use__lte=datetime.now(), )
    else:
        return None