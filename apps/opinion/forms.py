# -*- coding: utf-8 -*-
from django import forms

__author__ = 'AlexStarov'


class OpinionAddForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    title = forms.CharField(required=False)
    comment = forms.CharField(required=True)
