# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView

__author__ = 'AlexStarov'


class OpinionListView(ListView):
    from apps.comment.models import Comment
    queryset = Comment.objects.filter(type=1, pass_moderation=True)
    context_object_name = 'opinion_list'
    template_name = 'opinion_list.jinja2'


class OpinionDetailView(DetailView):
    from apps.comment.models import Comment
    queryset = Comment.objects.filter(type=1, pass_moderation=True)
    context_object_name = 'opinion_list'
    template_name = 'opinion_list.jinja2'


class OpinionAddView(FormView):
    template_name = 'opinion_add.jinja2'
    from apps.opinion.forms import OpinionAddForm
    form_class = OpinionAddForm


class OpinionAddingView(CreateView):
    from apps.opinion.forms import OpinionAddedForm
    form_class = OpinionAddedForm
    from apps.comment.models import Comment
    model = Comment
    success_url = '/ok/vse/good/'

    def post(self, request, *args, **kwargs):
        response = super(OpinionAddingView, self).post(request, *args, **kwargs)

        form = self.form_class(request.POST)

        print request.POST

        if form.is_valid():
            data = form.cleaned_data
            print data

        return response


class OpinionAddedView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        response = super(OpinionAddedView, self).render_to_response(context, **response_kwargs)
        print response
        response.template_name = 'opinion_added.jinja2'
        print response
        return response
