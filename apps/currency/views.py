# coding=utf-8

from django.http import HttpResponseRedirect


def currency_change(request, ):
    if request.method == 'POST':
        if request.session.get(u'cookie', None, ):
            action = request.POST.get(u'action', None, )
            if action == u'CurrencyChange':
                change_currency = request.POST.get(u'currency', None, )
                if change_currency:
                    try:
                        change_currency = int(change_currency, )
                    except ValueError:
                        request.session[u'currency_pk'] = 1
                    else:
                        from apps.product.models import Currency
                        try:
                            Currency.objects.get(pk=change_currency, )
                        except Currency.DoesNotExist:
                            request.session[u'currency_pk'] = 1
                        else:
                            request.session[u'currency_pk'] = change_currency
                else:
                    request.session[u'currency_pk'] = 1
                redirect_url = request.POST.get(u'redirect_url', None, )
                if redirect_url:
                    return HttpResponseRedirect(redirect_url, )
    return HttpResponseRedirect('/', )
