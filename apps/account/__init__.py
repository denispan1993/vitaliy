# coding=utf-8

from models import Profile

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# from django.dispatch import dispatcher

# @receiver(post_save, sender=User, dispatch_uid='AutoCreate_Profile', )
def AutoCreate_Profile(sender, instance, created, signal, *args, **kwargs):
    print 'Enter to create Profile'
    if created:
        print 'Create Profile'
        # profile, created =
        try:
            print 'All OK!!!'
            print sender
            print instance
            print instance.username
            user = User.objects.get(pk=instance.pk)
            profile = Profile(user=user)
            print profile
#            profile.user = instance
            print 'profile.user = instance'
            profile.save()
#            Profile.objects.create(user=instance, )
            print 'All Good!!!!'
        except Profile.DoesNotExist:
            print 'Help!!!!!!'
        # except TypeError:
            # print 'My TypeError!!!!!!!#'
        else:
            print'All Very GOOOOOOOOODDDDDDDDDDD!!!!!!!!!!!!!'
        finally:
            print 'Finita Lya Comedy ;-('
        #Profile.objects.get_or_create(user=instance, )
        # print(profile)
        # print(created)

#dispatcher.connect(AutoCreate_Profile, signal=post_save, sender=User, )
post_save.connect(receiver=AutoCreate_Profile, sender=User, dispatch_uid='AutoCreate_Profile', )
