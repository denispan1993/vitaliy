# -*- coding: utf-8 -*-
from django import forms

from .models import SendSMS

__author__ = 'Alex Starov'


class SendSMSCreateForm(forms.ModelForm, ):

    messages = {
        'required': 'This field is required.',
    }
    error_messages = {
        'required': 'Это поле должно быть заполнено.',
    }

    def __init__(self, *args, **kwargs):
        super(CouponGroupCreateEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    class Meta():
        model = CouponGroup
        fields = '__all__'


class CouponCreateEditForm(forms.ModelForm, ):

    def __init__(self, *args, **kwargs):
        super(CouponCreateEditForm, self).__init__(*args, **kwargs)

    class Meta():
        model = Coupon
        fields = '__all__'
