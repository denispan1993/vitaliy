# coding=UTF-8

from models import Profile

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User, )
def AutoCreate_Profile(sender, instance, created, **kwargs):
    print u"Вход в создание профайла"
    if created:
        print u"Создание профайла"
        profile, created = Profile.objects.get_or_create(user=instance, )
        print(profile)
        print(created)
