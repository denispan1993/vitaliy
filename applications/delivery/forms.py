# coding=utf-8
__author__ = 'Alex Starov'

from django import forms
from django.utils.translation import ugettext_lazy as _


class DeliveryCreateEditForm(forms.ModelForm, ):

    def __init__(self, *args, **kwargs):
        super(DeliveryCreateEditForm, self).__init__(*args, **kwargs)

    class Meta:
        from applications.delivery.models import Delivery
        model = Delivery
        fields = '__all__'
