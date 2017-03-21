# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test

__author__ = 'AlexStarov'


def member_required(view):
    func = lambda u: u.is_active and not u.is_staff
    return user_passes_test(func)(view)


def manager_required(view):
    func = lambda u: u.is_active and u.is_staff
    return user_passes_test(func)(view)
