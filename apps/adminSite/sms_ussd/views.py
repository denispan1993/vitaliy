# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import View, CreateView

__author__ = 'AlexStarov'


class SendSMSCreateView(CreateView, ):
    form_class = None
    template_name = None
    queryset = None

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendSMSCreateView, self).dispatch(request, *args, **kwargs)
