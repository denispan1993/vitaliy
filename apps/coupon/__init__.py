# coding=utf-8
__author__ = 'Alex Starov'

from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.coupon.models import CouponGroup


def my_pre_save(sender, instance, raw, using, update_fields, *args, **kwargs):
    from django.utils.timezone import now
    if not instance.created_at:
        instance.created_at = now()
    instance.updated_at = now()
    if instance.pk is None:
        print 'Created == False'
    else:
        print 'Instance.pk: ', instance.pk, 'Created == True'
    # print kwargs['created']
    # print kwargs['instance']

pre_save.connect(receiver=my_pre_save,
                 sender=CouponGroup,
                 dispatch_uid='coupon_group_pre_save_dispatch', )