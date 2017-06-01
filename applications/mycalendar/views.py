# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render_to_response, render
from django.views.generic import FormView, View
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.utils import get_app_template_dirs
from django.views.generic.edit import ProcessFormView
from django.template import RequestContext, Context
from applications.product.models import Country
from django.shortcuts import redirect
from applications.mycalendar.models import Event

__author__ = 'AlexStarov'


class AllViews(View, ):
    template_name = 'all.jinja2'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        template = get_template(template_name=self.template_name)

        html = template.render(request=request, context=context,)
        response = HttpResponse(html, )

        return response
        #return render_to_response(template_name=self.template_name,
        #                          context=context,
        #                          context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            context = self.get_context_data(**kwargs)
            template = get_template(template_name='load/all.jinja2')

            html = template.render(request=request, context=context,)
            response = HttpResponse(html, )

            return response
        else:
            return HttpResponse('Request method POST and AJAX()', )

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self

        query = Event.objects\
            .filter(location_date__date_start__gte=datetime.today(), )

        try:
            """ gte больше или равно """
            events = query.distinct()
        except Event.DoesNotExist:
            events = False

        leadings_courses = []
        sections = []
        cityes = []
        if events:
            for event in events:

                leading_course = event.leading_course
                if leading_course not in leadings_courses:
                    leadings_courses.append(leading_course, )

                section = event.section
                if section not in sections:
                    sections.append(section, )

                locations_date = event.location_date.filter(date_start__gte=datetime.today(), )
                for location_date in locations_date:
                    city = location_date.city
                    if city not in cityes:
                        cityes.append(city, )

        kwargs['leadings_courses'] = leadings_courses
        kwargs['sections'] = sections
        kwargs['cityes'] = cityes

        try:
            select_section = int(self.request.POST.get('select_section'))
            if not select_section == 0:
                query = query.filter(subject_id=select_section)
        except (ValueError, TypeError):
            pass

        try:
            leading_course = int(self.request.POST.get('leading_course'))
            if not leading_course == 0:
                query = query.filter(leading_course_id=leading_course)
        except (ValueError, TypeError):
            pass

        try:
            select_city = int(self.request.POST.get('select_city'))
            if not select_city == 0:
                query = query.filter(location_date__city_id=select_city)
        except (ValueError, TypeError):
            pass

        kwargs['events'] = query.distinct()

        return kwargs


def leading_course(request,
        template_name=u'leading_course.jinja2', ):
    from applications.mycalendar.models import Event
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
    from applications.calendar.models import Event

    return render(request=request, template_name=template_name, )
