# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm, CharField

__author__ = 'AlexStarov'


class OpinionAddForm(Form):
    name = CharField(required=True)
    email = CharField(required=True)
    phone = CharField(required=False)
    title = CharField(required=False)
    comment = CharField(required=True)


class OpinionAddedForm(ModelForm):

    class Meta(object):
        from apps.comment.models import Comment
        model = Comment
        fields = ['name', 'title', 'comment', 'email', 'phone']
