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


class OpinionAddedView(CreateView):
    from apps.comment.models import Comment
    model = Comment
    success_url = '/ok/vse/good/'


class OpinionAddingView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        response = super(OpinionAddingView, self).render_to_response(context, **response_kwargs)
        print response
        response.template_name = 'opinion_added.jinja2'
        print response
        return response
