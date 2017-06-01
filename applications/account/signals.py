# -*- coding: utf-8 -*-


def AutoCreate_UserProfileModel(signal, sender, instance, created, *args, **kwargs):
    if created:
        from .models import UserProfileModel
        UserProfileModel(user=instance, ).save()
