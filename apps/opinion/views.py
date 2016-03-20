# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.views.generic import DetailView, ListView


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
