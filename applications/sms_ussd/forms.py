# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SMS

code_provider = dict((key, value) for key, value in SMS.CODE_PROVIDER)

__author__ = 'AlexStarov'


class SendSMSCreateForm(forms.ModelForm, ):

    phone = forms.CharField(
        max_length=32,
        min_length=9,
        label=_('Номер телефона', ),
        help_text=_('Номер телефона', ),
    )

    def clean(self):
        cleaned_data = super(SendSMSCreateForm, self).clean()
        phone = cleaned_data.get('phone', False, )

        if not phone:
            raise forms.ValidationError(
                "Введите номер телефона"
            )

        else:
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

            phone_code = int(phone[:2])

            if phone_code in code_provider.keys():
                cleaned_data['to_code'] = phone_code
            else:
                raise forms.ValidationError(
                    "Код оператора не принадлежит не одному мобильному оператору"
                )

            cleaned_data['to_phone'] = int(phone[2:])
            cleaned_data['phone'] = '0{phone_code}{phone_number}'\
                .format(
                    phone_code=phone_code,
                    phone_number=int(phone[2:]),
                )
        return cleaned_data

    class Meta:
        model = SMS
        fields = ['message', ]
