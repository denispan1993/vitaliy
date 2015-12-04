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
        events = False

    leadings_courses = []
    if events:
        for event in events:
            leading_course = event.leading_course
            if leading_course not in leadings_courses:
                leadings_courses.append(leading_course, )
    subjects = []
    if events:
        for event in events:
            subject = event.subject
            if subject not in subjects:
                subjects.append(subject, )
    cityes = []
    if events:
        for event in events:
            locations_date_time = event.location_date_time.filter(date_start__gte=datetime.today(), )
            print locations_date_time
            for location_date_time in locations_date_time:
                print location_date_time
                city = location_date_time.city
                if city not in cityes:
                    print city
                    cityes.append(city, )
    return render(request=request,
                  template_name=template_name,
                  context={'leadings_courses': leadings_courses,
                           'cities': cityes,
                           'subjects': subjects,
                           'events': events, },
                  content_type='text/html', )


def leading_course(request,
        template_name=u'leading_course.jinja2', ):
    from apps.calendar.models import Event
    from datetime import datetime
    try:
        """ gte больше или равно """
        events = Event.objects.filter(location_date_time__date_start__gte=datetime.today(), ).distinct()
    except Event.DoesNotExist:
        events = False

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
