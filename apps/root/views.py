# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.shortcuts import render_to_response, render
from django.template import RequestContext


def root_page(request, template_name=u'index.jinja2', ):
    if request.method == 'GET':
        GET_NAME = request.GET.get(u'action', False, )
        if GET_NAME == 'delivery':
            key = request.GET.get(u'id', False, )
            if key:
                from apps.delivery.models import EmailForDelivery, TraceOfVisits
                try:
                    email = EmailForDelivery.objects.get(key=key, )
                except EmailForDelivery.DoesNotExist:
                    print 'Error: E-Mail not found for key: ', key
                else:
                    record = TraceOfVisits(email=email, delivery=email.delivery.delivery, )
                    url = request.GET.get('url', False, )
                    if url:
                        record.url = url.encode('utf8', )
                        record.save()
                        from django.shortcuts import redirect
                        return redirect(to=url, permanent=True, )
                    else:
                        record.save()
                    unsubscribe = request.GET.get('unsubscribe', False, )
                    if unsubscribe == 'True':
                        typedelivery = request.GET.get('typedelivery', False, )
                        if typedelivery:
                            try:
                                typedelivery = int(typedelivery, )
                            except ValueError:
                                pass
                            else:
                                email = email.now_email
                                """
                                (1, _(u'Фэйк рассылка', ), ),
                                (2, _(u'Акция', ), ),
                                (3, _(u'Новинки', ), ),
                                (4, _(u'Рассылка на "SPAM" адреса', ), ),
                                """
                                if typedelivery == 4:
                                    email.delivery_spam = False
                                email.save()

    # from apps.product.models import Category
    # try:
    #     categories_basement = Category.objects.basement()
    # except Category.DoesNotExist:
    #     categories_basement = None

    # try:
    #     categories_first = Category.objects.get(pk=1)
    # except Category.DoesNotExist:
    #     categories_first = None

    # from apps.product.models import Product
    # try:
    #     all_products = Product.objects.published()
    # except Product.DoesNotExist:
    #     all_products = None

    # limit_on_page = request.session.get(u'limit_on_page', None, )
    # try:
    #     limit_on_page = int(limit_on_page, )
    # except ValueError:
    #     limit_on_page = 12
    # finally:
    #     in_main_page = Product.manager.in_main_page(limit_on_page, )
    from apps.product.models import Product
    try:
        in_main_page = Product.objects.in_main_page(no_limit=True, )  # limit_on_page, )
    except Product.DoesNotExist:
        in_main_page = None

    # children_categories = categories_first.children.all()

    #return render_to_response(template_name=template_name,
    #                          #context={'in_main_page': in_main_page, },
    #                          dictionary=locals(),
    #                          context_instance=RequestContext(request, ),
    #                          content_type='text/html', )

    """ Рабочий экземпляр """
#    from django.template.loader import get_template
#    template_name = u'index.jinja2'
#    t = get_template(template_name)
#    html = t.render(request=request, context={'in_main_page': in_main_page, }, )
#    from django.http import HttpResponse
#    response = HttpResponse(html, )
#    # Мы не можем выяснить когда менялись внутринние подкатегории.
#    # Поэтому мы не отдаем дату изменения текущей категории.
##    from apps.utils.datetime2rfc import datetime2rfc
##    response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
#    return response

    """ Тоже рабочий экземпляр """
    return render(request=request,
                  template_name=template_name,
                  context={'in_main_page': in_main_page, },
                  content_type='text/html', )
