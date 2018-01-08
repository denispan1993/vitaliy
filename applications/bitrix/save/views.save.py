# -*- coding: utf-8 -*-
import os
import base64
from celery.utils import uuid
from datetime import datetime, date
from django.views.generic import View
from django.http import QueryDict, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_bitrix_catalog

__author__ = 'AlexStarov'


class ExchangeView(View, ):

    @method_decorator(csrf_exempt, )
    def dispatch(self, request, *args, **kwargs):
        return super(ExchangeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        auth_token_1c = request.META.get('HTTP_AUTHORIZATION', False)
        auth_token_server = 'Basic '\
                            + base64.b64encode('User123:password123'.encode('ascii')).decode('ascii')

        if auth_token_1c == auth_token_server:

            request_COOKIES = request.COOKIES.get('sessionid', False, )
            request_COOKIES_len = len(request.COOKIES, )

            if not request_COOKIES\
                    and request_COOKIES_len == 0\
                    and not request.session.session_key:

                if not request.session.exists(request.session.session_key):
                    request.session.create()

            elif request_COOKIES == request.session.session_key:
                pass
            else:
                return HttpResponse('failure', )
        else:
            return HttpResponse('failure', )

        data = request.GET.copy()
        type = data.get('type', False, )

        if type:
            mode = data.get('mode', False, )

            if type == 'catalog':

                """ type=catalog """
                """ Выгрузка товаров на сайт """

                if mode == 'checkauth':
                    return HttpResponse('success\nsessionid\n{key}'.format(key=request.session.session_key), )

                elif mode == 'init':
                    return HttpResponse('zip=no\nfile_limit=16777216', )

                elif mode == 'import':
                    filename = data.get('filename', False, )
                    if filename == 'import.xml':
                        pass
                    elif filename == 'offers.xml':
                        """ Запуск задачи обработки импортируемых файлов """
                        process_bitrix_catalog\
                            .apply_async(
                                queue='celery',
                                task_id='celery-task-id-{0}'.format(uuid(), ), )

                    return HttpResponse('success', )

            elif type == 'sale':

                """ type=catalog """
                """ Выгрузка заказаов в 1С """

                if mode == 'checkauth':

                    return HttpResponse('success\nsessionid\n{key}'.format(key=request.session.session_key), )

                elif mode == 'query':
                    print('query')
                    response = HttpResponse(export_orders(), content_type="text/xml")
                    # response['Content-Disposition'] = 'attachment; filename=orders.xml'
                    print(response)
                    return response

        return HttpResponse('', )

    def post(self, request, *args, **kwargs):

        auth_token_1c = request.META.get('HTTP_AUTHORIZATION', False)
        auth_token_server = 'Basic '\
                            + base64.b64encode('User123:password123'.encode('ascii')).decode('ascii')

        if auth_token_1c == auth_token_server:

            request_COOKIES = request.COOKIES.get('sessionid', False, )

            if not request_COOKIES == request.session.session_key:
                return HttpResponse('failure', )

        else:
            return HttpResponse('failure', )

        query_string = request.META.get('QUERY_STRING', False, )

        query_string = QueryDict(query_string=query_string, )

        if query_string.get('type', False, ) == 'catalog'\
                and query_string.get('mode', False, ) == 'file'\
                and request.META.get('CONTENT_TYPE', False, ) == 'application/octet-stream':

            filename = query_string.get('filename', False, )

            path = 'storage/{app}/{year}/{month:02d}/{day:02d}/'\
                .format(
                    app='bitrix',
                    year=date.today().year, month=date.today().month, day=date.today().day, )

            path_split = path.split('/', )
            path = ''
            for dir in path_split:

                path += '{dir}/'.format(dir=dir, )
                try:
                    os.stat(path, )
                except Exception as e:
                    print('bitrix/views.py: 113:', e, )
                    os.mkdir(path, )

            filename = '{filename}.{hour:02d}.{minute:02d}.{ext}'\
                .format(
                    filename=filename.split('.')[0],
                    hour=datetime.now().hour,
                    minute=datetime.now().minute,
                    ext=filename.split('.')[1],
                )
            with open('{path}{filename}'.format(path=path, filename=filename, ), 'w') as outfile:
                outfile.write(request.body.decode('utf-8'))

        return HttpResponse('success', )

XML = """<КоммерческаяИнформация ВерсияСхемы="2.03" ДатаФормирования="2007-10-30">
</КоммерческаяИнформация>"""

XML1 = """<КоммерческаяИнформация ВерсияСхемы="2.03" ДатаФормирования="2007-10-30">
<Документ>
<Ид>36</Ид>
<Номер>36</Номер>
<Дата>2007-10-30</Дата>
<ХозОперация>Заказ товара</ХозОперация>
<Роль>Продавец</Роль>
<Валюта>грн</Валюта>
<Курс>1</Курс>
<Сумма>6734.47</Сумма>
<Контрагенты>
<Контрагент>
<Ид>1#admin# admin </Ид>
<Наименование>admin</Наименование>
<Роль>Покупатель</Роль>
<ПолноеНаименование>admin</ПолноеНаименование>
<Фамилия>Иванов</Фамилия>
<Имя>admin</Имя>
<Контакты/>
<Представители>
<Представитель>
<Контрагент>
<Отношение>Контактное лицо</Отношение>
<Ид>b342955a9185c40132d4c1df6b30af2f</Ид>
<Наименование>admin</Наименование>
</Контрагент>
</Представитель>
</Представители>
</Контрагент>
</Контрагенты>
<Время>15:19:27</Время>
<Комментарий/>
<Товары>
<Товар>
<Ид>ORDER_DELIVERY</Ид>
<Наименование>Доставка заказа</Наименование>
<БазоваяЕдиница Код="796" НаименованиеПолное="Штука" МеждународноеСокращение="PCE">шт</БазоваяЕдиница>
<ЦенаЗаЕдиницу>340.00</ЦенаЗаЕдиницу>
<Количество>1</Количество>
<Сумма>340.00</Сумма>
<ЗначенияРеквизитов>
<ЗначениеРеквизита>
<Наименование>ВидНоменклатуры</Наименование>
<Значение>Услуга</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>ТипНоменклатуры</Наименование>
<Значение>Услуга</Значение>
</ЗначениеРеквизита>
</ЗначенияРеквизитов>
</Товар>
<Товар>
<Ид>dee6e19a-55bc-11d9-848a-00112f43529a</Ид>
<ИдКаталога>bd72d8f9-55bc-11d9-848a-00112f43529a</ИдКаталога>
<Наименование>Телевизор &quot;JVC&quot;</Наименование>
<БазоваяЕдиница Код="796" НаименованиеПолное="Штука" МеждународноеСокращение="PCE">шт</БазоваяЕдиница>
<ЦенаЗаЕдиницу>6394.47</ЦенаЗаЕдиницу>
<Количество>1.00</Количество>
<Сумма>6394.47</Сумма>
<ЗначенияРеквизитов>
<ЗначениеРеквизита>
<Наименование>ВидНоменклатуры</Наименование>
<Значение>Товар</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>ТипНоменклатуры</Наименование>
<Значение>Товар</Значение>
</ЗначениеРеквизита>
</ЗначенияРеквизитов>
</Товар>
</Товары>
<ЗначенияРеквизитов>
<ЗначениеРеквизита>
<Наименование>Метод оплаты</Наименование>
<Значение>Наличный расчет</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Заказ оплачен</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Доставка разрешена</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Отменен</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Финальный статус</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Статус заказа</Наименование>
<Значение>[N] Принят</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Дата изменения статуса</Наименование>
<Значение>2007-10-30 15:19:27</Значение>
</ЗначениеРеквизита>
</ЗначенияРеквизитов>
</Документ>
</КоммерческаяИнформация>"""

XML2 = """<КоммерческаяИнформация ВерсияСхемы="2.03" ДатаФормирования="2007-10-30">
<Документ>
<Ид>36</Ид>
<Номер>36</Номер>
<Дата>2007-10-30</Дата>
<ХозОперация>Заказ товара</ХозОперация>
<Роль>Продавец</Роль>
<Валюта>руб</Валюта>
<Курс>1</Курс>
<Сумма>6734.47</Сумма>
<Контрагенты>
<Контрагент>
<Ид>1#admin# admin </Ид>
<Наименование>admin</Наименование>
<Роль>Покупатель</Роль>
<ПолноеНаименование>admin</ПолноеНаименование>
<Фамилия>Иванов</Фамилия>
<Имя>admin</Имя>
<АдресРегистрации>
<Представление>ггг</Представление>
<АдресноеПоле>
<Тип>Почтовый индекс</Тип>
<Значение>1111</Значение>
</АдресноеПоле>
<АдресноеПоле>
<Тип>Улица</Тип>
<Значение>ггг</Значение>
</АдресноеПоле>
</АдресРегистрации>
<Контакты/>
<Представители>
<Представитель>
<Контрагент>
<Отношение>Контактное лицо</Отношение>
<Ид>b342955a9185c40132d4c1df6b30af2f</Ид>
<Наименование>admin</Наименование>
</Контрагент>
</Представитель>
</Представители>
</Контрагент>
</Контрагенты>
<Время>15:19:27</Время>
<Комментарий/>
<Товары>
<Товар>
<Ид>ORDER_DELIVERY</Ид>
<Наименование>Доставка заказа</Наименование>
<БазоваяЕдиница Код="796" НаименованиеПолное="Штука" МеждународноеСокращение="PCE">шт</БазоваяЕдиница>
<ЦенаЗаЕдиницу>340.00</ЦенаЗаЕдиницу>
<Количество>1</Количество>
<Сумма>340.00</Сумма>
<ЗначенияРеквизитов>
<ЗначениеРеквизита>
<Наименование>ВидНоменклатуры</Наименование>
<Значение>Услуга</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>ТипНоменклатуры</Наименование>
<Значение>Услуга</Значение>
</ЗначениеРеквизита>
</ЗначенияРеквизитов>
</Товар>
<Товар>
<Ид>dee6e19a-55bc-11d9-848a-00112f43529a</Ид>
<ИдКаталога>bd72d8f9-55bc-11d9-848a-00112f43529a</ИдКаталога>
<Наименование>Телевизор &quot;JVC&quot;</Наименование>
<БазоваяЕдиница Код="796" НаименованиеПолное="Штука" МеждународноеСокращение="PCE">шт</БазоваяЕдиница>
<ЦенаЗаЕдиницу>6394.47</ЦенаЗаЕдиницу>
<Количество>1.00</Количество>
<Сумма>6394.47</Сумма>
<ЗначенияРеквизитов>
<ЗначениеРеквизита>
<Наименование>ВидНоменклатуры</Наименование>
<Значение>Товар</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>ТипНоменклатуры</Наименование>
<Значение>Товар</Значение>
</ЗначениеРеквизита>
</ЗначенияРеквизитов>
</Товар>
</Товары>
<ЗначенияРеквизитов>
<ЗначениеРеквизита>
<Наименование>Метод оплаты</Наименование>
<Значение>Наличный расчет</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Заказ оплачен</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Доставка разрешена</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Отменен</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Финальный статус</Наименование>
<Значение>false</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Статус заказа</Наименование>
<Значение>[N] Принят</Значение>
</ЗначениеРеквизита>
<ЗначениеРеквизита>
<Наименование>Дата изменения статуса</Наименование>
<Значение>2007-10-30 15:19:27</Значение>
</ЗначениеРеквизита>
</ЗначенияРеквизитов>
</Документ>
</КоммерческаяИнформация>"""

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement
import six
from io import BytesIO

from applications.cart.models import Order


def export_orders():
    root = ET.Element(u'КоммерческаяИнформация')
    root.set(u'ВерсияСхемы', '2.05')
    root.set(u'ДатаФормирования', six.text_type(datetime.now().date()))

    orders = Order.objects.all()[:1]

    for order in orders:
        xml_order = SubElement(root, 'Документ')

        SubElement(xml_order, 'Ид').text = str(order.id)
        SubElement(xml_order, 'Номер').text = str(order.number)

        SubElement(xml_order, 'Дата').text = str(order.created_at.date())
        SubElement(xml_order, 'Время').text = str(order.created_at.time())

        SubElement(xml_order, 'ХозОперация').text = 'Заказ товара'
        SubElement(xml_order, 'Роль').text = 'Продавец'

        SubElement(xml_order, 'Курс').text = '1'
        SubElement(xml_order, 'Сумма').text = '12345'

        SubElement(xml_order, 'Комментарий').text = 'jhbjhbjhb'

        contragents = SubElement(xml_order, 'Контрагенты')
        customer = SubElement(contragents, 'Контрагент')
        SubElement(customer, 'Ид').text = '123454321'
        SubElement(customer, 'Наименование').text = '45679ujj'
        SubElement(customer, 'ПолноеНаименование').text = '8t7676g76g7g'
        SubElement(customer, 'Роль').text = 'Покупатель'

        addr = SubElement(customer, 'АдресРегистрации')
        SubElement(addr, 'Представление').text = 'str.'
        addr_field = SubElement(addr, 'АдресноеПоле')
        SubElement(addr_field, 'Тип').text = 'Страна'
        SubElement(addr_field, 'Значение').text = 'Украина'
        addr_field = SubElement(addr, 'АдресноеПоле')
        SubElement(addr_field, 'Тип').text = 'Регион'
        SubElement(addr_field, 'Значение').text = 'str.'

        contacts = SubElement(customer, 'Контакты')
        contact = SubElement(contacts, 'Контакт')
        SubElement(contact, 'Тип').text = 'Телефон'
        SubElement(contact, 'Значение').text = '+380952886976'
        contact = SubElement(contacts, 'Контакт')
        SubElement(contact, 'Тип').text = 'Почта'
        SubElement(contact, 'Значение').text = 'zakaz@keksik.com.ua'

        xml_props = SubElement(xml_order, 'ЗначенияРеквизитов')
        xml_prop = SubElement(xml_props, 'ЗначениеРеквизита')
        SubElement(xml_prop, 'Наименование').text = 'Статус заказа'
        SubElement(xml_prop, 'Значение').text = '[N] Принят'

    f = BytesIO()
    print(root)
    tree = ET.ElementTree(root)

    tree.write(f, encoding='windows-1251', xml_declaration=True)
    g = f.getvalue()
    print(g)

    return g