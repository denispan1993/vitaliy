# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import View, CreateView
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy

from django.http import HttpResponseRedirect

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
        # print 'form_class', form_class
        form = self.get_form(form_class)
        # print 'form', form

        if form.is_valid():
            # print 'form_valid(123)'
            return self.form_valid(form, kwargs={'request': request, }, )

        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        """
            If the form is valid, save the associated model.
        """

        self.object = form.save(commit=False, )

        self.object.user_id = kwargs['kwargs']['request'].user.pk
        self.object.sessionid = kwargs['kwargs']['request'].session.session_key

        data = form.cleaned_data

        #for key, value in data.iteritems():
        #    self.object[key] = data[key]

        self.object.phone = data['phone']
        self.object.code = data['code']
        self.object.message = data['message']

        self.object.save()

        return HttpResponseRedirect(self.get_success_url(), )


def get_form_kwargs(self, ):
    kwargs = super(SendSMSCreateView, self).get_form_kwargs()
    data = kwargs.get('data', False, )

    if data:
        data = data.copy()
        phone = data.get('phone', False, )

        if phone:
            data['code'] = 95
            data['phone'] = 2886976

        kwargs['data'] = data

    print 'data', kwargs.get('data')
    print kwargs
    return kwargs
