# coding=utf-8
__author__ = 'user'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def coupon_test(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                coupon_key = request.POST.get(u'value', None, )
                if coupon_key:
                    from apps.coupon.models import Coupon
                    try:
                        coupon = Coupon.objects.get(key=coupon_key, )
                    except Coupon.DoesNotExist:
                        response = {'result': 'Bad',
                                    'help_text': u'Номер купона не действительный', }
                    except Coupon.MultipleObjectsReturned:
                        response = {'result': 'Bad',
                                    'help_text': u'Странный какой-то купон', }
                    else:
                        # from datetime import datetime
                        from django.utils.timezone import now
                        if coupon.start_of_the_coupon < now():
                            if now() < coupon.end_of_the_coupon:
                                if coupon.number_of_uses < coupon.number_of_possible_uses:
                                    coupon.number_of_uses += 1
                                    from apps.cart.views import get_cart_or_create
                                    cart = get_cart_or_create(request,
                                                              user_object=None,
                                                              created=False, )
                                    if cart:
                                        coupon.child_cart.add(cart, )
                                    coupon.save()
                                    response = {'coupon_pk': coupon.pk,
                                                'percentage_discount': coupon.percentage_discount,
                                                'result': 'Ok',
                                                'help_text': u'Этот купон предоставляет скидку в %d%% от суммы корзины' % coupon.percentage_discount, }
                                else:
                                    response = {'result': 'Bad',
                                                'help_text': u'Превышен лимит количества использований купона', }
                            else:
                                response = {'result': 'Bad',
                                            'help_text': u'Купон просрочен', }
                        else:
                            response = {'result': 'Bad',
                                        'help_text': u'Время использования этого купона еще не настало', }
                else:
                    response = {'result': 'Bad',
                                'help_text': u'Номер купона не задан', }
                data = dumps(response, )
                mimetype = 'application/javascript'
                return HttpResponse(data, mimetype, )
            else:
                return HttpResponse(status=400, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )