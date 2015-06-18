# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def comment_change(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                comment_pk = request.POST.get(u'comment_pk', None, )
                if comment_pk:
                    try:
                        comment_pk = int(comment_pk, )
                    except ValueError:
                        return HttpResponse(status=400, )
                    else:
                        from apps.comment.models import Comment
                        try:
                            queryset_comment = Comment.objects.get(pk=comment_pk, )
                        except Comment.DoesNotExist:
                            return HttpResponse(status=400, )
                        else:
                            response = {}
                            action = request.POST.get(u'action', None, )
                            if action == 'commenter_name_change':
                                """ Изменение имени "Комментатора"
                                """
                                commenter_name = request.POST.get(u'commenter_name', None, )
                                if commenter_name and commenter_name != u'':
                                    queryset_comment.name = commenter_name
                                    queryset_comment.save()
                                    response = {'comment_pk': comment_pk,
                                                'result': 'Ok', }
                            elif action == 'comment_change':
                                """ Изменение самого "Комментатария"
                                """
                                comment = request.POST.get(u'comment', None, )
                                if comment and comment != u'':
                                    queryset_comment.comment = comment
                                    queryset_comment.save()
                                    response = {'comment_pk': comment_pk,
                                                'result': 'Ok', }
                            elif action == 'comment_pass_moderation_change':
                                """ Изменение статуса модерации "Комментатария"
                                """
                                comment_pass_moderation = request.POST.get(u'comment_pass_moderation', None, )
                                if comment_pass_moderation and comment_pass_moderation != u'':
                                    if comment_pass_moderation == 'true':
                                        comment_pass_moderation = True
                                    else:
                                        comment_pass_moderation = False
                                    queryset_comment.pass_moderation = comment_pass_moderation
                                    queryset_comment.save()
                                    response = {'comment_pk': comment_pk,
                                                'comment_pass_moderation': comment_pass_moderation,
                                                'result': 'Ok', }
                            elif action == 'comment_delete':
                                """ Удаление "Комментатария"
                                """
                                queryset_comment.delete()
                                response = {'comment_pk': comment_pk,
                                            'result': 'Ok', }
                            #--------------------------
                            data = dumps(response, )
                            mimetype = 'application/javascript'
                            return HttpResponse(data, mimetype, )
                else:
                    return HttpResponse(status=400, )
            else:
                return HttpResponse(status=400, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
