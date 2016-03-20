# -*- coding: utf-8 -*-
from django import forms

__author__ = 'AlexStarov'


class OpinionAddForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    title = forms.CharField()
    comment = forms.CharField()
