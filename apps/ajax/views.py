__author__ = 'user'


def resolution(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            width = request.POST.get(u'width', None, )
            if width:
                try:
                    width = int(width, )
                except ValueError:
                    response = {u'result': u'Bad', }
                    request.session[u'width'] = 1024
                else:
                    response = {u'result': u'Ok', }
                    request.session[u'width'] = width
            else:
                response = {u'result': u'Bad', }
                request.session[u'width'] = 1024
            from datetime import datetime
            request.session[u'datetime_width'] = datetime.now()
            format = 'json'
            from django.core import serializers
            data = serializers.serialize(format, response, )
            mimetype = 'application/javascript'
            from django.http import HttpResponse
            return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)
