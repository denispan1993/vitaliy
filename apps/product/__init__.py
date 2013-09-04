# coding=utf-8
__author__ = 'Sergey'

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.product.models import Product
from apps.product.models import ItemID
from apps.product.models import IntermediateModelManufacturer
from apps.product.models import Manufacturer


@receiver(post_save, sender=Product, )
@receiver(post_save, sender=ItemID, )
@receiver(post_save, sender=IntermediateModelManufacturer, )
@receiver(post_save, sender=Manufacturer, )
def modification_ItemID(instance, **kwargs):
    #id_parent = instance.parent.id
    #
    #if instance.ItemID == u'%.5s' % id_parent:
    #    pass
    #print(instance)
    #print type(instance)
    print(instance.__class__)
    #print(instance._meta)
    #print(instance._meta.app_label)
    #print(instance.__class__.__name__)
    #from django.db.models import get_model
    #model = get_model(instance._meta.app_label, instance.__class__.__name__, )
    #print(model)
