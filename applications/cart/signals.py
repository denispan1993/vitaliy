# -*- coding: utf-8 -*-

from django.utils import timezone


def my_pre_save(sender, instance, raw, using, update_fields, *args, **kwargs):
    if not instance.created_at:
        instance.created_at = timezone.now()
    instance.updated_at = timezone.now()
    if instance.pk is None:
        print 'Created == False'
    else:
        print 'Instance.pk: ', instance.pk, 'Created == True'
    # print kwargs['created']
    # print kwargs['instance']

#pre_save.connect(receiver=my_pre_save,
#                 sender=CouponGroup,
#                 dispatch_uid='coupon_group_pre_save_dispatch', )