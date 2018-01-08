# -*- coding: utf-8 -
from __future__ import absolute_import
import os
import logging
import importlib
from io import BytesIO
import six
from datetime import datetime
try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

from applications.cart.models import Order

logger = logging.getLogger(__name__)


class ExportManager(object):

    def __init__(self):
        self.item_processor = ItemProcessor()
        self.root = ET.Element(u'КоммерческаяИнформация')
        self.root.set(u'ВерсияСхемы', '2.05')
        self.root.set(u'ДатаФормирования', datetime.now().date().strftime('%Y-%m-%d'))

    def get_xml(self):
        f = BytesIO()
        tree = ET.ElementTree(self.root)
        tree.write(f, encoding='windows-1251', xml_declaration=True)
        return f.getvalue()

    def export_all(self):
        self.export_orders()

    def export_orders(self):
        for order in Order.objects.all()[:2]:
            order_element = ET.SubElement(self.root, u'Документ')
            ET.SubElement(order_element, u'Ид').text = str(order.id)
            ET.SubElement(order_element, u'Номер').text = str(order.number)
            ET.SubElement(order_element, u'Дата').text = order.date.strftime('%Y-%m-%d')
            ET.SubElement(order_element, u'Время').text = order.time.strftime('%H:%M:%S')
            ET.SubElement(order_element, u'ХозОперация').text = 'Заказ товара'
            ET.SubElement(order_element, u'Роль').text = 'Продавец'
            ET.SubElement(order_element, u'Валюта').text = 'грн'
            ET.SubElement(order_element, u'Курс').text = '1'
            ET.SubElement(order_element, u'Сумма').text = order.order_sum_show()
            ET.SubElement(order_element, u'Комментарий').text = order.comment
            clients_element = ET.SubElement(order_element, u'Контрагенты')
            client_element = ET.SubElement(clients_element, u'Контрагент')
            ET.SubElement(client_element, u'Ид').text = six.text_type(order.client.id)
            ET.SubElement(client_element, u'Наименование').text = six.text_type(order.client.name)
            ET.SubElement(client_element, u'Роль').text = six.text_type(order.client.role)
            ET.SubElement(client_element, u'ПолноеНаименование').text = six.text_type(order.client.full_name)
            ET.SubElement(client_element, u'Фамилия').text = six.text_type(order.client.last_name)
            ET.SubElement(client_element, u'Имя').text = six.text_type(order.client.first_name)
            address_element = ET.SubElement(clients_element, u'АдресРегистрации')
            ET.SubElement(clients_element, u'Представление').text = six.text_type(order.client.address)
            products_element = ET.SubElement(order_element, u'Товары')
            for order_item in order.items:
                product_element = ET.SubElement(products_element, u'Товар')
                ET.SubElement(product_element, u'Ид').text = six.text_type(order_item.id)
                ET.SubElement(product_element, u'Наименование').text = six.text_type(order_item.name)
                sku_element = ET.SubElement(product_element, u'БазоваяЕдиница ')
                sku_element.set(u'Код', order_item.sku.id)
                sku_element.set(u'НаименованиеПолное', order_item.sku.name_full)
                sku_element.set(u'МеждународноеСокращение', order_item.sku.international_abbr)
                sku_element.text = order_item.sku.name
                ET.SubElement(product_element, u'ЦенаЗаЕдиницу').text = six.text_type(order_item.price)
                ET.SubElement(product_element, u'Количество').text = six.text_type(order_item.quant)
                ET.SubElement(product_element, u'Сумма').text = six.text_type(order_item.sum)

    def flush(self):
        self.item_processor.flush_pipeline(Order)


class ItemProcessor(object):

    def __init__(self):
        self._project_pipelines = {}
        self._load_project_pipelines()

    def _load_project_pipelines(self):
        try:
            pipelines_module_name = settings.CML_PROJECT_PIPELINES
        except AttributeError:
            logger.info('Configure CML_PROJECT_PIPELINES in settings!')
            return
        try:
            pipelines_module = importlib.import_module(pipelines_module_name)
        except ImportError:
            return
        for item_class_name in PROCESSED_ITEMS:
            try:
                pipeline_class = getattr(pipelines_module, '{}Pipeline'.format(item_class_name))
            except AttributeError:
                continue
            self._project_pipelines[item_class_name] = pipeline_class()

    def _get_project_pipeline(self, item_class):
        item_class_name = item_class.__name__
        return self._project_pipelines.get(item_class_name, False)

    def process_item(self, item):
        project_pipeline = self._get_project_pipeline(item.__class__)
        if project_pipeline:
            try:
                project_pipeline.process_item(item)
            except Exception as e:
                logger.error('Error processing of item {}: {}'.format(item.__class__.__name__, repr(e)))

    def yield_item(self, item_class):
        project_pipeline = self._get_project_pipeline(item_class)
        if project_pipeline:
            try:
                return project_pipeline.yield_item()
            except Exception as e:
                logger.error('Error yielding item {}: {}'.format(item_class.__name__, repr(e)))
                return []
        return []

    def flush_pipeline(self, item_class):
        project_pipeline = self._get_project_pipeline(item_class)
        if project_pipeline:
            try:
                project_pipeline.flush()
            except Exception as e:
                logger.error('Error flushing pipeline for item {}: {}'.format(item_class.__name__, repr(e)))
