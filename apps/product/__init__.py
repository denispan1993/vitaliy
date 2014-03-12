# coding=utf-8
__author__ = 'Sergey'

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from apps.product.models import Product
from apps.product.models import ItemID
from apps.product.models import IntermediateModelManufacturer
from apps.product.models import Manufacturer


#@receiver(post_save, sender=Product, )
def post_save_Product(instance, **kwargs):
    # print(instance.__class__.__name__)
    # from apps.product.models import Product
    #aaa = instance.bbb
    from apps.product.models import ItemID
    ''' Пытаемся взять все записи из ItemID которые ссылаются на этот Product '''
    ItemsID = instance.ItemID.all()
    ''' Если этих записей нету, то создаём новую запись '''
    if not ItemsID:
        ItemID.objects.create(parent=instance, ItemID=u'%.5d' % instance.id, )
#            print(u'ItemsID: %s' % ItemsID, )

#        try:
#            from apps.product.models import ItemID
#            ItemID = ItemID.objects.get(ItemID=u'%.5d' % instance.pk, )
#        except ItemID.DoesNotExist:
#            print(u'ItemID: None', )
#        else:
#            print(u'ItemID:' % ItemID, )
#        try:
#            from apps.product.models import IntermediateModelManufacturer
#            IntermediateModelManufacturer
    #from django.db.models import get_model
    #model = get_model(instance._meta.app_label, instance.__class__.__name__, )
    #print(model)


#@receiver(post_save, sender=Product, )
#@receiver(post_save, sender=ItemID, )
#@receiver(post_save, sender=IntermediateModelManufacturer, )
#@receiver(post_save, sender=Manufacturer, )
def modification_ItemID(instance, **kwargs):
#    #id_parent = instance.parent.id
#    #
#    #if instance.ItemID == u'%.5s' % id_parent:
#    #    pass
#    #print(instance)
#    #print type(instance)
    print(instance.__class__.__name__)
    if instance.__class__.__name__ == 'ItemID':
        print(instance.ItemID)
    #print(instance._meta)
    #print(instance._meta.app_label)
    #print(instance.__class__.__name__)
#    if instance.__class__.__name__ == 'Product':
#        print(u'Product.pk: %d' % instance.pk, )
#        try:
#            from apps.product.models import Product
#            ItemsID = instance.ItemID.all()
#        except Product.DoesNotExist:
#            from apps.product.models import ItemID
#            ItemID.objects.create(ItemID=u'%.5d' % instance.pk, )
#            print(u'ItemsID: %s' % ItemsID, )

#        try:
#            from apps.product.models import ItemID
#            ItemID = ItemID.objects.get(ItemID=u'%.5d' % instance.pk, )
#        except ItemID.DoesNotExist:
#            print(u'ItemID: None', )
#        else:
#            print(u'ItemID:' % ItemID, )
##        try:
##            from apps.product.models import IntermediateModelManufacturer
##            IntermediateModelManufacturer
#    #from django.db.models import get_model
    #model = get_model(instance._meta.app_label, instance.__class__.__name__, )
    #print(model)


from apps.product.models import AdditionalInformationForPrice


@receiver(m2m_changed, sender=AdditionalInformationForPrice.information.through, )
def m2m_changed_information(sender, instance, action, reverse, model, pk_set, using, signal, **kwargs):
    # print(action)
    if action == 'post_add' and reverse is False:
        # print(sender)
        # print(instance)
        # print(reverse)
        # print(model)
        # print(pk_set)
        from apps.product.models import InformationForPrice
        for pk in pk_set:
            # print(pk)
            information = InformationForPrice.objects.get(pk=pk, )
            # print(information)
            information.product = instance.product
            information.save()
        # print(using)
        # print(signal)
        # for key, value in kwargs.iteritems():
            # print('Key: %s - Value: %s', (key, value, ), )
