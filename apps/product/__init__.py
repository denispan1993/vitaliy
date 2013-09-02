# coding=utf-8
__author__ = 'Sergey'

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.product.models import ItemID


@receiver(post_save, sender = ItemID, )
def modification_ItemID(instance, **kwargs):
    id_parent = instance.parent.id
    if instance.ItemID == u'%.5s' % id_parent:
        pass
