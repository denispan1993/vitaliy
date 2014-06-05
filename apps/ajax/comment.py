# coding=utf-8
__author__ = 'user'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def commenter_name_change(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                action = request.POST.get(u'action', None, )
                if action == 'commenter_name_change':
                    """ Изменение имени "Комментатора"
                    """
                    comment_pk = request.POST.get(u'comment_pk', None, )
                    if comment_pk:
                        try:
                            comment_pk = int(comment_pk, )
                        except ValueError:
                            return HttpResponse(status=400, )
                        else:
                            from apps.comment.models import Comment
                            comment = Comment.objects.get(pk=comment_pk, )
                            commenter_name = request.POST.get(u'commenter_name', None, )
                            if commenter_name and commenter_name != u'':
                                comment.name = commenter_name
                                comment.save()
                                response = {'comment_pk': comment_pk,
                                            'result': 'Ok', }
                                data = dumps(response, )
                                mimetype = 'application/javascript'
                                return HttpResponse(data, mimetype, )
                            else:
                                return HttpResponse(status=400, )
                    else:
                        return HttpResponse(status=400, )
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
