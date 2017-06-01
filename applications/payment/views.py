# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def root(request,
         id=None,
         template_name=u'payment.jinja2', ):

    try:
        id = int(id, )
    except ValueError:
        id = False
    from applications.cart.models import Order
    order = False
    if id:
        try:
            order = Order.objects.get(pk=id, )
        except Order.DoesNotExist:
            pass
    from proj.settings import PAYPAL_RECEIVER_EMAIL
    from django.core.urlresolvers import reverse
    # What you want the button to do.
    paypal_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "notify_url": "http://kekesik.com.ua" + reverse('payment:paypal-ipn'),
        "return_url": "http://keksik.com.ua/оплата/совершена/",
        "cancel_return": "http://keksik.com.ua/оплата/отменена/",
        # "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }
    if order:
        paypal_dict["amount"] = "%d" % order.order_sum(calc_or_show='calc', )
        paypal_dict["item_name"] = "Заказ № %d" % order.pk
        paypal_dict["invoice"] = "%d" % order.pk
    else:
        paypal_dict["amount"] = False
        paypal_dict["item_name"] = False
        paypal_dict["invoice"] = False

    # Create the instance.
    from paypal.standard.forms import PayPalPaymentsForm
    form = PayPalPaymentsForm(initial=paypal_dict)


    from django.template.loader import get_template
    if 'template_name' not in locals() or 'template_name' not in globals():
        template_name = u'payment.jinja2'
    t = get_template(template_name)
    html = t.render(request=request, context={'form': form,
                                              'order': order, }, )  # 'in_main_page': in_main_page, }, )
    from django.http import HttpResponse
    response = HttpResponse(html, )
    # Мы не можем выяснить когда менялись внутринние подкатегории.
    # Поэтому мы не отдаем дату изменения текущей категории.
#    from applications.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
    return response
