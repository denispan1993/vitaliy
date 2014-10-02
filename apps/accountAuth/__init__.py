# coding=utf-8

#from apps.accountAuth.models import Profile

#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from proj import settings
##from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
#from apps.authModel.models import User

#@receiver(post_save, sender=User, dispatch_uid='AutoCreate_Profile', )
#def AutoCreate_Profile(signal, sender, instance, created, *args, **kwargs):
#    if created:
#        # profile, created =
#        Profile.objects.get_or_create(user=instance, )

#authModel = get_user_model()
#post_save.connect(receiver=AutoCreate_Profile, sender=authModel, dispatch_uid='AutoCreate_Profile', )
