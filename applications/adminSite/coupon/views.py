# -*- coding: utf-8 -*-
from datetime import datetime
from string import ascii_lowercase, digits
from django.db import connection, transaction, IntegrityError
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.edit import FormView, CreateView, View, ProcessFormView

from proj.settings import SERVER

from applications.utils.captcha.utils import key_generator
from applications.coupon.forms import CouponCreateEditForm, CouponGroupCreateEditForm
from applications.coupon.models import Coupon, CouponGroup
from applications.coupon.views import coupon_create

__author__ = 'AlexStarov'


@staff_member_required
def coupon_group_search(request,
                        template_name=u'coupon/group_index.jinja2', ):
    error_message = u''
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == u'coupon_group_search':
            coupon_group_id = request.POST.get(u'coupon_group_id', None, )
            if coupon_group_id:
                try:
                    coupon_group_id = int(coupon_group_id, )
                except ValueError:
                    error_message = u'Некорректно введен номер группы купонов.'
                else:
                    try:
                        coupon_group = CouponGroup.objects.get(pk=coupon_group_id, )
                    except CouponGroup.DoesNotExist:
                        error_message = u'Группы купонов с таким номером не существует.'
                    else:
                        coupon_group_id = '%06d' % coupon_group_id
                        return redirect(to='coupon_group_edit', id=coupon_group_id, )
    coupon_groups = CouponGroup.objects.all()
    return render(request=request,
                  template_name=template_name,
                  context={'error_message': error_message,
                           'coupon_groups': coupon_groups, },
                  content_type='text/html', )


#from django.views.generic.list import ListView
#
#
#class CouponGroupManage(ListView, ):
#    template_name = 'member/creative/creatives-manage.html'
#    paginate_by = 10

#    def get_queryset(self):
#        from modules.creative.models import Creative
#        return Creative.objects.all()


class CouponGroupCreateEdit(FormView, ):
    form_class = CouponGroupCreateEditForm
    template_name = u'coupon/coupon_group_edit.jinja2'
    success_url = u'/админ/купон/группа/редактор/добавить/'
    coupon_group = None

    def form_valid(self, form, ):
        # print form
        # print form.cleaned_data
        # print form.cleaned_data.get('POST_NAME', None, )
        if form.cleaned_data.get('name', None, ):
            self.coupon_group = CouponGroup.objects.create(**form.cleaned_data)
            how_much_coupons = form.cleaned_data.get('how_much_coupons', 0, )
            start_of_the_coupon = form.cleaned_data.get('start_of_the_coupon', datetime.now(), )
            # start_of_the_coupon = datetime.strptime(start_of_the_coupon, '%d.%m.%Y %H:%M:%S', )
            start_of_the_coupon = start_of_the_coupon.strftime('%Y-%m-%d %H:%M:%S')
            end_of_the_coupon = form.cleaned_data.get('end_of_the_coupon', datetime.now(), )
            # end_of_the_coupon = datetime.strptime(end_of_the_coupon, '%d.%m.%Y %H:%M:%S', )
            end_of_the_coupon = end_of_the_coupon.strftime('%Y-%m-%d %H:%M:%S')
            cursor = connection.cursor()
            name = form.cleaned_data.get('name', None, )
            number_of_possible_uses = form.cleaned_data.get('number_of_possible_uses', 0, )
            percentage_discount = form.cleaned_data.get('percentage_discount', 0, )
            if SERVER:
                ins = '''insert into Coupon (name, coupon_group_id, `key`, number_of_possible_uses, number_of_uses, percentage_discount, start_of_the_coupon, end_of_the_coupon, created_at, updated_at)
                         values ('%s', %d, '%s', %d, 0, %d, '%s', '%s', NOW(), NOW())'''
            else:
                ins = '''insert into Coupon (name, coupon_group_id, key, number_of_possible_uses, number_of_uses, percentage_discount, start_of_the_coupon, end_of_the_coupon, created_at, updated_at)
                         values ('%s', %d, '%s', %d, 0, %d, '%s', '%s', datetime('now'), datetime('now'))'''
            for i in range(how_much_coupons, ):
                success = 0
                unsuccess = 0
                ok = True
                while ok:
                    # print 'success: %d unsuccess: %d' % (success, unsuccess, )
                    # print 'SERVER: %s' % SERVER
                    key = key_generator(size=6, chars=ascii_lowercase + digits, )
                    insert = ins % (name,
                                    self.coupon_group.id,
                                    key,
                                    int(number_of_possible_uses),
                                    int(percentage_discount),
                                    start_of_the_coupon,
                                    end_of_the_coupon, )
                    print('coupon/view.py(105): ', insert, )
                    try:
                        with transaction.atomic():
                            cursor.execute(insert, )
                            # Captcha_Key.objects.create(image=image, )
                    except IntegrityError as s:
                        print('IntegrityError', ' Key: ', key, )
                        print('coupon/views.py(112): ', type(s,), )
                        print('coupon/views.py(113): ', s, )
                        unsuccess += 1
                    except Exception as inst:
                        print('coupon/views.py(116): ', type(inst, ), )
                        print('coupon/views.py(117): ', inst, )
                        unsuccess += 1
                    else:
                        success += 1
                        ok = False

#                Coupon.objects.create(name=name,
#                                      key=key_generator(size=6, chars=ascii_lowercase + digits, ),
#                                      coupon_group=self.coupon_group,
#                                      number_of_possible_uses=number_of_possible_uses,
#                                      percentage_discount=percentage_discount,
#                                      start_of_the_coupon=start_of_the_coupon,
#                                      end_of_the_coupon=end_of_the_coupon, )
        return super(CouponGroupCreateEdit, self, ).form_valid(form, )

    def get_success_url(self, **kwargs):
        url = super(CouponGroupCreateEdit, self).get_success_url()
        if self.coupon_group:
            return u'/админ/купон/группа/редактор/%.6d/' % int(self.coupon_group.pk, )
        else:
            return url

    def get_context_data(self, **kwargs):
        context = super(CouponGroupCreateEdit, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        # print context
        # print kwargs
        # print self.kwargs
        #for k, i in kwargs:
        #print kwargs
        #    # print k, i
        #pk = self.kwargs['coupon_group_id']
        pk = self.kwargs.get('coupon_group_id', None, )
        context['disable'] = False
        context['coupons'] = False
        context['coupon_group_pk'] = False
        if pk:
            try:
                pk_int = int(pk, )
            except ValueError:
                pass
            else:
                context['disable'] = True
                context['coupon_group_pk'] = pk_int
                try:
                    coupon_group = CouponGroup.objects.get(pk=pk_int, )
                except CouponGroup.DoesNotExist:
                    pass
                else:
                    context['coupon_group'] = coupon_group
                    try:
                        coupons = Coupon.objects.filter(coupon_group=coupon_group, )
                    except Coupon.DoesNotExist:
                        pass
                    else:
                        context['coupons'] = coupons
        #print pk
        #print form.fields
        #print context['form']
        ## print context['form'].get('pk')
        #context['disable'] = True
        # print context
        return context

    def post(self, request, *args, **kwargs):
        list_POST_NAME = ['coupon_group_search', 'coupon_group_edit', ]
        get_POST_NAME = request.POST.get('POST_NAME', None, )
        if get_POST_NAME in list_POST_NAME:
            return super(CouponGroupCreateEdit, self, ).post(self, request, *args, **kwargs)
        else:
            raise Http404


class CouponCreateEdit(FormView, ):
    form_class = CouponCreateEditForm
    template_name = u'coupon/coupon_edit.jinja2'
    success_url = u'/админ/купон/редактор/добавить/'

    def get_context_data(self, **kwargs):
        context = super(CouponCreateEdit, self).get_context_data(**kwargs)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        context['form'] = form
        pk = self.kwargs.get('coupon_id', None, )

        context['disable'] = False
        context['coupons'] = False
        context['coupon_pk'] = False

        try:
            coupon = Coupon.objects.get(pk=pk, )
            context['coupon'] = coupon
            context['disable'] = True
            context['coupon_pk'] = pk

        except Coupon.DoesNotExist:
            pass

        return context


@staff_member_required
def coupon_group_edit(request,
                      coupon_group_id=0,
                      template_name=u'coupon/coupon_group_edit.jinja2', ):
    error_message = u''
    coupon_group = None
    if coupon_group_id:
        print('coupon/views.py(229): ', coupon_group_id, )
        try:
            coupon_group_id = int(coupon_group_id, )
        except ValueError:
            error_message = u'Некорректный номер группы купонов.'
        else:
            try:
                coupon_group = CouponGroup.objects.get(pk=coupon_group_id, )
            except CouponGroup.DoesNotExist:
                error_message = u'В базе отсутсвует группа купонов с таким номером.'
            else:
                error_message = u'Отсутсвует номер группы купонов.'
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'coupon_group_dispatch':
            name = request.POST.get(u'name', None, )
            how_much_coupons = request.POST.get(u'how_much_coupons', None, )
            try:
                how_much_coupons = int(how_much_coupons, )
            except ValueError:
                error_message = u'Некорректный номер комментария.'
            number_of_possible_uses = request.POST.get(u'number_of_possible_uses', None, )
            try:
                number_of_possible_uses = int(number_of_possible_uses, )
            except ValueError:
                error_message = u'Некорректный номер комментария.'
            percentage_discount = request.POST.get(u'percentage_discount', None, )
            try:
                percentage_discount = int(percentage_discount, )
            except ValueError:
                error_message = u'Некорректный номер комментария.'
            start_of_the_coupon = request.POST.get(u'start_of_the_coupon', None, )
            start_of_the_coupon = datetime.strptime(start_of_the_coupon, '%d/%m/%Y %H:%M:%S', )
            end_of_the_coupon = request.POST.get(u'end_of_the_coupon', None, )
            end_of_the_coupon = datetime.strptime(end_of_the_coupon, '%d/%m/%Y %H:%M:%S', )
            coupon_group = CouponGroup.objects.create(name=name,
                                                      how_much_coupons=how_much_coupons,
                                                      number_of_possible_uses=number_of_possible_uses,
                                                      percentage_discount=percentage_discount,
                                                      start_of_the_coupon=start_of_the_coupon,
                                                      end_of_the_coupon=end_of_the_coupon, )
            for n in range(how_much_coupons):
                coupon_create(name=name,
                              coupon_group=coupon_group,
                              number_of_possible_uses=number_of_possible_uses,
                              percentage_discount=percentage_discount,
                              start_of_the_coupon=start_of_the_coupon,
                              end_of_the_coupon=end_of_the_coupon, )
    return render(request=request,
                  template_name=template_name,
                  context={'comment_id': coupon_group_id,
                           'comment': coupon_group,
                           'error_message': error_message, },
                  content_type='text/html', )
