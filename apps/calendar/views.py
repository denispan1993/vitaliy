# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


from django.shortcuts import render_to_response, render
from django.template import RequestContext, Context
from apps.product.models import Country
from django.shortcuts import redirect


def all(request,
        template_name=u'all.jinja2', ):
    from apps.calendar.models import Event
    from datetime import datetime
    try:
        """ gte больше или равно """
        events = Event.objects.filter(location_date_time__date_start__gte=datetime.today(), ).distinct()
    except Event.DoesNotExist:
        events = None

    return render(request=request,
                  template_name=template_name,
                  context={'events': events, },
                  content_type='text/html', )


def years(request,
          template_name=u'years.jinja2', ):
    return render(request=request, template_name=template_name, )


def year(request,
         year=None,
         template_name=u'year.jinja2', ):
    return render(request=request, template_name=template_name, )


def month(request,
          year=None,
          month=None,
          template_name=u'month.jinja2', ):
    from apps.calendar.models import Event

    return render(request=request, template_name=template_name, )
