# -*- coding: utf-8 -*-
try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json
from django.http import HttpResponse

from django.utils.timezone import now

from apps.cart.utils import get_cart_or_create
from apps.coupon.models import Coupon

__author__ = 'AlexStarov'


def coupon_test(request, ):
    if request.is_ajax() and request.method == 'POST':

        response = {'result': 'Bad', }
        coupon_key = request.POST.get(u'value', None, )
        if coupon_key:
            try:
                coupon = Coupon.objects.get(key=coupon_key, )
            except Coupon.DoesNotExist:
                response.update({'help_text': u'Номер купона не действительный', }, )

            except Coupon.MultipleObjectsReturned:
                response.update({'help_text': u'Странный какой-то купон', }, )

            else:
                if not coupon.start_of_the_coupon < now():
                    response.update({'help_text': u'Время использования этого купона еще не настало', }, )

                else:
                    if not now() < coupon.end_of_the_coupon:
                        response.update({'help_text': u'Купон просрочен', }, )

                    else:
                        if not coupon.number_of_uses < coupon.number_of_possible_uses:
                            response.update({'help_text': u'Превышен лимит количества использований купона', }, )

                        else:
                            ''' Берем текущую корзину '''
                            cart = get_cart_or_create(request,
                                                      user_object=None,
                                                      created=False, )
                            if cart:
                                ''' Указывают, ли купоны на эту корзину? '''
                                coupons = cart.Cart_child.all()
                                if not coupons:
                                    ''' Если НЕТ
                                        Ставим указатель этого купона на эту корзину '''
                                    coupon.child_cart.add(cart, )
                                    coupon.number_of_uses += 1
                                    coupon.save()
                                    response.update({'result': 'Ok',
                                                     'coupon_pk': coupon.pk,
                                                     'percentage_discount': coupon.percentage_discount,
                                                     'help_text': u'Этот купон предоставляет скидку в %d%% от суммы корзины' % coupon.percentage_discount, }, )

                                else:
                                    response.update({'help_text': u'К этой корзине уже привязан купон со скидкой %d%%' % coupons[0].percentage_discount, }, )

        else:
            response.update({'help_text': u'Номер купона не задан', }, )

        return HttpResponse(data=dumps(response, ),
                            mimetype='application/javascript', )

    return HttpResponse(status=400, )
