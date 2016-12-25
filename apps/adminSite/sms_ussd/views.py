# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy

from django.utils import timezone
from django.http import HttpResponseRedirect

from apps.sms_ussd.forms import SendSMSCreateForm
from apps.sms_ussd.models import SMS, USSD
__author__ = 'AlexStarov'


class SMS_USSDPanelView(TemplateView, ):
    template_name = 'sms_ussd/sms_ussd_panel.html'
    success_url = reverse_lazy('admin_page:sms_ussd_send_sms')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SMS_USSDPanelView, self).dispatch(request, *args, **kwargs)


class SendSMSCreateView(CreateView, ):
    form_class = SendSMSCreateForm
    template_name = 'sms_ussd/sendSMS_form.html'
    model = SMS
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
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form, kwargs={'request': request, }, )

        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        """
            If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False, )

        self.object.received_at = timezone.now()
        self.object.direction = 2  # Outgouing

        self.object.user_id = kwargs['kwargs']['request'].user.pk
        self.object.sessionid = kwargs['kwargs']['request'].session.session_key

        self.object.to_phone_char = form.cleaned_data['phone']
        self.object.to_code = form.cleaned_data['to_code']
        self.object.to_phone = form.cleaned_data['to_phone']
        self.object.message = form.cleaned_data['message']

        self.object.save()

        return HttpResponseRedirect(self.get_success_url(), )


class SendUSSDCreateView(CreateView, ):
    form_class = SendSMSCreateForm
    template_name = 'sms_ussd/sendUSSD_form.html'
    model = USSD
    success_url = reverse_lazy('admin_page:sms_ussd_send_ussd')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendSMSCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form, kwargs={'request': request, }, )

        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        """
            If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False, )

        self.object.received_at = timezone.now()
        self.object.direction = 2  # Outgouing

        self.object.user_id = kwargs['kwargs']['request'].user.pk
        self.object.sessionid = kwargs['kwargs']['request'].session.session_key

        self.object.to_phone_char = form.cleaned_data['phone']
        self.object.to_code = form.cleaned_data['to_code']
        self.object.to_phone = form.cleaned_data['to_phone']
        self.object.message = form.cleaned_data['message']

        self.object.save()

        return HttpResponseRedirect(self.get_success_url(), )
