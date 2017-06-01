# -*- coding: utf-8 -*-

__author__ = 'AlexStarov'

default_app_config = 'applications.ProductConfig'


#@receiver(post_save, sender=Product, )
def post_save_Product(instance, **kwargs):
    # print(instance.__class__.__name__)
    # from applications.product.models import Product
    #aaa = instance.bbb
    from .models import ItemID
    ''' Пытаемся взять все записи из ItemID которые ссылаются на этот Product '''
    ItemsID = instance.ItemID.all()
    ''' Если этих записей нету, то создаём новую запись '''
    if not ItemsID:
        ItemID.objects.create(parent=instance, ItemID=u'%.5d' % instance.id, )
#            print(u'ItemsID: %s' % ItemsID, )

#        try:
#            from applications.product.models import ItemID
#            ItemID = ItemID.objects.get(ItemID=u'%.5d' % instance.pk, )
#        except ItemID.DoesNotExist:
#            print(u'ItemID: None', )
#        else:
#            print(u'ItemID:' % ItemID, )
#        try:
#            from applications.product.models import IntermediateModelManufacturer
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
#            from applications.product.models import Product
#            ItemsID = instance.ItemID.all()
#        except Product.DoesNotExist:
#            from applications.product.models import ItemID
#            ItemID.objects.create(ItemID=u'%.5d' % instance.pk, )
#            print(u'ItemsID: %s' % ItemsID, )

#        try:
#            from applications.product.models import ItemID
#            ItemID = ItemID.objects.get(ItemID=u'%.5d' % instance.pk, )
#        except ItemID.DoesNotExist:
#            print(u'ItemID: None', )
#        else:
#            print(u'ItemID:' % ItemID, )
##        try:
##            from applications.product.models import IntermediateModelManufacturer
##            IntermediateModelManufacturer
#    #from django.db.models import get_model
    #model = get_model(instance._meta.app_label, instance.__class__.__name__, )
    #print(model)
