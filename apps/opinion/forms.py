# -*- coding: utf-8 -*-
from django.forms import ModelForm

__author__ = 'AlexStarov'


class OpinionAddForm(ModelForm):

    class Meta(object):
        from apps.comment.models import Comment
        model = Comment
        fields = ['name', 'title', 'comment', 'email', 'phone']
