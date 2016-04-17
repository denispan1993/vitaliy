# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.core.urlresolvers import reverse_lazy

__author__ = 'AlexStarov'


class OpinionAddView(FormView):
    template_name = 'opinion_add.jinja2'
    from apps.opinion.forms import OpinionAddForm
    form_class = OpinionAddForm
    from apps.comment.models import Comment
    model = Comment
    success_url = reverse_lazy('opinion_ru:added_successfully_ru')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            return super(OpinionAddView, self).post(self, request, *args, **kwargs)

        from django.shortcuts import render
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = 1
        self.object.save()
        return super(OpinionAddView, self).form_valid(form)

    def form_invalid(self, form):
        return super(OpinionAddView, self).form_invalid(form)


class OpinionAddedView(TemplateView):
    template_name = 'opinion_added.jinja2'


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
