# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import View, CreateView
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy

from apps.sms_ussd.forms import SendSMSCreateForm
from apps.sms_ussd.models import SendSMS
__author__ = 'AlexStarov'


class SendSMSCreateView(CreateView, ):
    form_class = SendSMSCreateForm
    template_name = None
    model = SendSMS
    success_url = reverse_lazy('admin_page:sms_ussd_send_sms')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendSMSCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        print 'form_class', form_class
        form = self.get_form(form_class)
        # print 'form', form

        if form.is_valid():
            print 'form_valid(123)'
            return self.form_valid(form)

        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(SendSMSCreateView, self).get_form_kwargs()
        print kwargs
        return kwargs
