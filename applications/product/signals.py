# -*- coding: utf-8 -*-

from .models import InformationForPrice


def m2m_changed_information(sender, instance, action, reverse, model, pk_set, using, signal, **kwargs):
    if action == 'post_add' and reverse is False:
        for pk in pk_set:
            information = InformationForPrice.objects.get(pk=pk, )
            information.product = instance.product
            information.save()
