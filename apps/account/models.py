# coding=utf-8
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile, UserenaLanguageBaseProfile


class Profile(UserenaBaseProfile):
    # Пользователь
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_(u'Пользователь'),
                                related_name='profile',
                                blank=False,
                                null=False, )
#    favourite_snack = models.CharField(_('favourite snack'),
#                                       max_length=5, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Профайл: %s' % (self.user, )

    class Meta:
        db_table = u'Profile'
        ordering = [u'-created_at', ]
        verbose_name = u'Профайл'
        verbose_name_plural = u'Профайлы'

#User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
