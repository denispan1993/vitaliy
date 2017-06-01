# -*- coding: utf-8 -*-
from applications.coupon.models import Coupon
from applications.utils.captcha.views import key_generator

__author__ = 'AlexStarov'


def coupon_create(name,
                  coupon_group,
                  start_of_the_coupon,
                  end_of_the_coupon,
                  parent=None,
                  number_of_possible_uses=1,
                  percentage_discount=10, ):
    key = key_generator()
    coupon = Coupon.objects.create(name=name,
                                   coupon_group=coupon_group,
                                   key=key,
                                   parent=parent,
                                   number_of_possible_uses=number_of_possible_uses,
                                   percentage_discount=percentage_discount,
                                   start_of_the_coupon=start_of_the_coupon,
                                   end_of_the_coupon=end_of_the_coupon, )
    return coupon
