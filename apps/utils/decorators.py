# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.contrib.auth.decorators import user_passes_test


def member_required(view):
    func = lambda u: u.is_active and not u.is_staff
    return user_passes_test(func)(view)


def manager_required(view):
    func = lambda u: u.is_active and u.is_staff
    return user_passes_test(func)(view)
