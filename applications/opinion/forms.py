# -*- coding: utf-8 -*-
from django.forms import ModelForm

__author__ = 'AlexStarov'


class OpinionAddForm(ModelForm):

    class Meta(object):
        from applications.comment.models import Comment
        model = Comment
        fields = ['type', 'name', 'title', 'comment', 'email', 'phone']
