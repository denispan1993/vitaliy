# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SendSMS

code_provider = dict((key, value) for key, value in SendSMS.CODE_PROVIDER)

__author__ = 'AlexStarov'


class SendSMSCreateForm(forms.ModelForm, ):

    phone = forms.CharField(
        max_length=32,
        min_length=9,
        label=_(u'Номер телефона', ),
        help_text=_(u'Номер телефона', ),
    )

    def clean(self):
        cleaned_data = super(SendSMSCreateForm, self).clean()
        phone = cleaned_data.get('phone', None, )

        phone = phone\
            .strip('+')\
            .replace('(', '')\
            .replace(')', '')\
            .replace(' ', '')\
            .replace('-', '')\
            .lstrip('380')\
            .lstrip('38')\
            .lstrip('80')\
            .lstrip('0')

        try:
            int_phone = int(phone)

            if not len(str(int_phone)) == 9:
                raise forms.ValidationError(
                    "Короткий номер телефона"
                )

        except ValueError:
            raise forms.ValidationError(
                "В номере телефона присутствуют недопустимые символы"
            )

        code = int(phone[:2])

        if code in code_provider.keys():
            cleaned_data['code'] = code
        else:
            raise forms.ValidationError(
                "Код оператора не принадлежит не одному мобильному оператору"
            )

        cleaned_data['phone'] = int(phone[2:])
        return cleaned_data

    class Meta:
        model = SendSMS
        fields = ['message', ]
