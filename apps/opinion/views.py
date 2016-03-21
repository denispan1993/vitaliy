# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView
from django.core.urlresolvers import reverse, reverse_lazy

__author__ = 'AlexStarov'


class OpinionAddView(FormView):
    template_name = 'opinion_add.jinja2'
    from apps.opinion.forms import OpinionAddForm
    form_class = OpinionAddForm


class OpinionAddingView(CreateView):
    from apps.comment.models import Comment
    model = Comment
    http_method_names = [u'post', ]
    success_url = reverse_lazy('opinion_ru:added_successfully_ru')

    def form_invalid(self, form):
        # response = super(OpinionAddingView, self).form_invalid(form)
        from django.shortcuts import redirect
        return redirect(reverse('opinion_ru:added_not-successfully_ru'))


class OpinionAddedView(CreateView):
    template_name = 'opinion_added.jinja2'

    def render_to_response(self, context, **response_kwargs):
        response = super(OpinionAddedView, self).render_to_response(context, **response_kwargs)
        print response
        print response
        return response


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
