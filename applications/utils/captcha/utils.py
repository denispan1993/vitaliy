# -*- coding: utf-8 -*-
import string
import random

__author__ = 'AlexStarov'


def key_generator(size=8, chars=string.ascii_letters + string.digits, ):
    return ''.join(random.choice(chars, ) for _ in range(size, ), )
