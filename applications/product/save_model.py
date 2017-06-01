__author__ = 'user'

class AdditionalInformationAndInformationForPrice(models.Model):
    additionalinformation = models.ForeignKey(AdditionalInformationForPrice,
                                              verbose_name=_(u'Информация для прайса', ),
                                              null=False,
                                              blank=False, )
    information = models.ForeignKey(InformationForPrice,
                                    verbose_name=_(u'Информация для прайса', ),
                                    null=False,
                                    blank=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Промежуточная модель: %s <---> %s' % (self.additionalinformation, self.information, )

    def save(self, *args, **kwargs):
        # print(self.additionalinformation)
        # print(self.additionalinformation.product)
        # print(self.information)
        # print(self.information.product)
        self.information.product = self.additionalinformation.product
        self.information.save()
        # print(self.information)
        # print(self.information.product)
#        self.information.save_m2m()
        #all_informations = self.information.all()
        #print(all_informations)
        #print(self.information)
        #for inf in all_informations:
        #    print inf.information
        super(AdditionalInformationAndInformationForPrice, self, ).save(*args, **kwargs)
##        print(u'test1')
##        self.title += u'1'
#        if self.url == u'':
#            self.url = self.title.replace(' ', '_', ).replace('$', '-', ).replace('/', '_', )
#            try:
#                existing_category = Category.objects.get(url=self.url, )
#            except Category.DoesNotExist:
##                print(u'test2')
#                super(Category, self, ).save(*args, **kwargs)
##                print(u'test3')
#                return
##                print(u'test4')
#            else:
#                self.url += '1'
##                print(u'test5')
#                super(Category, self, ).save(*args, **kwargs)
#                return
#        else:
##            print(u'test6')
#            super(Category, self, ).save(*args, **kwargs)
##            print(u'test7')
#            return

    class Meta:
        db_table = 'AdditionalInformationAndInformationForPrice_m2m'
        ordering = ['-created_at', ]
        verbose_name = u'Промежуточная модель AdditionalInformation и Information'
        verbose_name_plural = u'Промежуточная модель AdditionalInformation и Information'
