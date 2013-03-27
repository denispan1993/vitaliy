# coding=utf-8

from models import Profile

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User, dispatch_uid='AutoCreate_Profile', )
def AutoCreate_Profile(sender, instance, created, signal, *args, **kwargs):
    if created:
        # profile, created =
        Profile.objects.get_or_create(user=instance, )

# post_save.connect(receiver=AutoCreate_Profile, sender=User, dispatch_uid='AutoCreate_Profile', )
