# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

from apps.account.models import UserProfileModel

from django.db.models.signals import post_save
from django.dispatch import receiver
from proj.settings import AUTH_USER_MODEL
##from django.contrib.auth.models import User
#from apps.authModel.models import User

from django.contrib.auth import get_user_model
authModel = get_user_model()

@receiver(post_save, sender=authModel, dispatch_uid='AutoCreate_UserProfileModel', )
def AutoCreate_UserProfileModel(signal, sender, instance, created, *args, **kwargs):
    if created:
        # profile, created =
        UserProfileModel(user=instance, ).save()
        #UserProfileModel.objects.get_or_create(user=instance, )

#from django.contrib.auth import get_user_model
#authModel = get_user_model()
#post_save.connect(receiver=AutoCreate_UserProfileModel, sender=authModel, dispatch_uid='AutoCreate_UserProfileProfile', )
