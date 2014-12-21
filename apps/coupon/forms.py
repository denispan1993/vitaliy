# coding=utf-8
__author__ = 'Alex Starov'

from django.forms import ModelForm, ModelMultipleChoiceField
from apps.coupon.models import CouponGroup


class CouponGroupCreateEditForm(ModelForm, ):

    # from apps.cart.models import Order
    # authors = ModelMultipleChoiceField(queryset=Order.objects.all(), )

    def __init__(self, *args, **kwargs):
        super(CouponGroupCreateEditForm, self).__init__(*args, **kwargs)
        #self.fields['pool'].required = True
        #self.fields['pool'].widget.is_required = True

    class Meta():
#        fields = ('username', 'pool', 'is_active', 'password1', 'password2')
        model = CouponGroup

#    def clean_username(self):
#        try:
#            username = self.cleaned_data["username"]
#            User.objects.get(username=username)
#        except User.DoesNotExist:
#            return username
#        raise forms.ValidationError(
#            self.error_messages['duplicate_username'])
