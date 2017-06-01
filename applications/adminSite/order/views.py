# -*- coding: utf-8 -*-
import celery
import math
from datetime import datetime, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
import proj.settings

from applications.cart.models import Order
from applications.sms_ussd.tasks import send_template_sms

__author__ = 'AlexStarov'


@staff_member_required
def order_search(request,
                 template_name=u'order/order_search.jinja2', ):

    error_message = u''

    if request.method == 'POST' and request.POST.get(u'POST_NAME', False, ) == 'order_search':

            order_id = request.POST.get(u'order_id', None, )
            if order_id:
                try:
                    order_id = int(order_id, )

                    try:
                        Order.objects.get(pk=order_id, )
                        return redirect(to='admin_page:order_edit', order_id='%06d' % order_id, )
                    except Order.DoesNotExist:
                        error_message = u'Заказа с таким номером не существует.'
                except ValueError:
                    error_message = u'Некорректно введен номер заказа.'

    #filter_datetime = datetime.now() - timedelta(days=15, )
    orders = Order.objects.filter(created_at__gte=datetime.now() - timedelta(days=15, ), )
    #orders = Order.objects.all()
    return render(request=request,
                  template_name=template_name,
                  context={'error_message': error_message,
                           'orders': orders, },
                  content_type='text/html', )


@staff_member_required
def order_edit_product_add(request,
                           order_id,
                           template_name=u'order/order_edit_product_add.jinja2', ):
    if order_id:
        try:
            order_id = int(order_id, )

            try:
                order = Order.objects.get(pk=order_id, )
            except Order.DoesNotExist:
                ''' В базе отсутсвует заказ с таким номером '''
                return redirect(to='admin_page:order_search', )

        except ValueError:
            ''' Некорректно введен номер заказа '''
            return redirect(to='admin_page:order_search', )

    else:
        ''' Отсутсвует номер заказа '''
        return redirect(to='admin_page:order_search', )

    return render(request=request,
                  template_name=template_name,
                  context={'order_id': order_id,
                           'order': order, },
                  content_type='text/html', )


@staff_member_required
def order_edit(request,
               order_id,
               template_name=u'order/order_edit.jinja2', ):

    if not order_id:
        ''' Отсутсвует номер заказа '''
        return redirect(to='admin_page:order_search', )
    else:

        try:
            order_id = int(order_id, )

            try:
                order = Order.objects.get(pk=order_id, )
            except Order.DoesNotExist:
                ''' В базе отсутсвует заказ с таким номером '''
                return redirect(to='admin_page:order_search', )

        except ValueError:
            ''' Некорректно введен номер заказа '''
            return redirect(to='admin_page:order_search', )

    if request.method == 'POST' and request.POST.get(u'POST_NAME', False, ) == 'order_dispatch':

        order_pk = request.POST.get(u'order_pk', None, )
        if order_pk:
            try:
                order_pk = int(order_pk, )

                if order_pk == order_id:

                    """ Расчитываем сумму заказа """
                    # * 1.01 --> добавляем 1 % банка
                    # math.ceil - округление до ближайшего большего числа
                    # Дважды откругляем до ближайшего
                    # БОЛЬШЕГО целого, чтобы была вероятность увеличить сумму
                    order.sent_out_sum = int(
                        math.ceil(
                            math.ceil(
                                order.order_sum(calc_or_show='show', ),
                            ) * 1.01,
                        ),
                    )

                    ''' Отправка e-mail письма и SMS с суммой и реквизитами на оплату '''

                    #delivery_order.apply_async(
                    #    queue='delivery_send',
                    #    kwargs={'order_pk': order.pk, },
                    #    task_id='celery-task-id-delivery_order-{0}'.format(celery.utils.uuid(), ),
                    #)

                    phone = order.phone \
                        .lstrip('+') \
                        .replace('(', '').replace(')', '').replace(' ', '') \
                        .replace('-', '').replace('.', '').replace(',', '') \
                        .lstrip('380').lstrip('38').lstrip('80').lstrip('0')

                    if len(phone, ) == 9:
                        send_template_sms.apply_async(
                            queue='delivery_send',
                            kwargs={
                                'sms_to_phone_char': '+380%s' % phone[:9],
                                'sms_template_name': proj.settings.SMS_TEMPLATE_NAME['SEND_AMOUNT'],
                                'sms_order_sum': int(order.sent_out_sum, ),
                            },
                            task_id='celery-task-id-send_template_sms-{0}'.format(celery.utils.uuid(), ),
                        )

                        return redirect(to='admin_page:order_search', )

            except ValueError:
                ''' Некорректно введен номер заказа '''
                return redirect(to='admin_page:order_search', )

    """ Записываем сумму которую мы отослали заказчику """
    order.save()

    return render(request=request,
                  template_name=template_name,
                  context={'order_id': order_id,
                           'order': order, },
                  content_type='text/html', )
