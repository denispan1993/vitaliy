# coding=utf-8
__author__ = 'Alex Starov'

from django import forms
# from django.forms import ModelForm  # , forms  # ModelMultipleChoiceField
from apps.coupon.models import CouponGroup
from django.utils.translation import ugettext_lazy as _


class CouponGroupCreateEditForm(forms.ModelForm, ):

    messages = {
        'required': 'This field is required.',
    }
    error_messages = {
        'required': 'Это поле должно быть заполнено.',
    }
    # from apps.cart.models import Order
    # authors = ModelMultipleChoiceField(queryset=Order.objects.all(), )

    def __init__(self, *args, **kwargs):
        super(CouponGroupCreateEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        # self.fields['name'].required = True
        # self.fields['name'].widget.is_required = True
        # self.fields['how_much_coupons'].required = True
        # self.fields['how_much_coupons'].widget.is_required = True
        # self.fields.required = False

        # instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     self.fields['name'].widget.attrs['readonly'] = True

    class Meta():
#        fields = ('username', 'pool', 'is_active', 'password1', 'password2')
        model = CouponGroup
        fields = '__all__'
        # labels = {
        #     'name': _(u'Именование группы купонов', ),
        # }
        # widgets = {
        #     'name': forms.TextInput(attrs={'size': 64, }, )
        # }

    # name = forms.CharField(label=_(u'Именование группы купонов'), )

#    def clean_username(self):
#        try:
#            username = self.cleaned_data["username"]
#            User.objects.get(username=username)
#        except User.DoesNotExist:
#            return username
#        raise forms.ValidationError(
#            self.error_messages['duplicate_username'])


class CouponCreateEditForm(forms.ModelForm, ):

    def __init__(self, *args, **kwargs):
        super(CouponCreateEditForm, self).__init__(*args, **kwargs)

    class Meta():
        from apps.coupon.models import Coupon
        model = Coupon
        fields = '__all__'
