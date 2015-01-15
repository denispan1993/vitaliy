# coding=utf-8
__author__ = 'user'

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def coupon_group_search(request,
                        template_name=u'coupon/coupon_group_search.jinja2.html', ):
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
                    from apps.coupon.models import CouponGroup
                    try:
                        coupon_group = CouponGroup.objects.get(pk=coupon_group_id, )
                    except CouponGroup.DoesNotExist:
                        error_message = u'Группы купонов с таким номером не существует.'
                    else:
                        coupon_group_id = '%06d' % coupon_group_id
                        from django.shortcuts import redirect
                        return redirect(to='coupon_group_edit', id=coupon_group_id, )
    from apps.coupon.models import CouponGroup
    coupon_groups = CouponGroup.objects.all()
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message,
                                              'coupon_groups': coupon_groups, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


#from django.views.generic.list import ListView
#
#
#class CouponGroupManage(ListView, ):
#    template_name = 'member/creative/creatives-manage.html'
#    paginate_by = 10

#    def get_queryset(self):
#        from modules.creative.models import Creative
#        return Creative.objects.all()

from django.views.generic.edit import FormView, CreateView, View, ProcessFormView


class CouponGroupCreateEdit(FormView, ):
    from apps.coupon.forms import CouponGroupCreateEditForm
    form_class = CouponGroupCreateEditForm
    template_name = 'coupon/coupon_group_edit.jingo.html'
    success_url = '/админ/купон/группа/редактор/добавить/'
    coupon_group = None

    def form_valid(self, form, ):
        #print form
        #print form.cleaned_data
        #print form.cleaned_data.get('POST_NAME', None, )
        if form.cleaned_data.get('name', None, ):
            from apps.coupon.models import CouponGroup
            self.coupon_group = CouponGroup.objects.create(**form.cleaned_data)
            from apps.coupon.models import Coupon
            how_much_coupons = form.cleaned_data.get('how_much_coupons', 0, )
            from datetime import datetime
            from apps.utils.captcha.views import key_generator
            from string import ascii_lowercase, digits
            for i in range(how_much_coupons, ):
                name = form.cleaned_data.get('name', None, )
                number_of_possible_uses = form.cleaned_data.get('number_of_possible_uses', 0, )
                percentage_discount = form.cleaned_data.get('percentage_discount', 0, )
                start_of_the_coupon = form.cleaned_data.get('start_of_the_coupon', datetime.now(), )
                end_of_the_coupon = form.cleaned_data.get('end_of_the_coupon', datetime.now(), )
                Coupon.objects.create(name=name,
                                      key=key_generator(size=6, chars=ascii_lowercase + digits, ),
                                      coupon_group=self.coupon_group,
                                      number_of_possible_uses=number_of_possible_uses,
                                      percentage_discount=percentage_discount,
                                      start_of_the_coupon=start_of_the_coupon,
                                      end_of_the_coupon=end_of_the_coupon, )
        return super(CouponGroupCreateEdit, self, ).form_valid(form, )

    def get_success_url(self, **kwargs):
        url = super(CouponGroupCreateEdit, self).get_success_url()
        if self.coupon_group:
            return '/админ/купон/группа/редактор/%.6d/' % int(self.coupon_group.pk, )
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
                from apps.coupon.models import CouponGroup
                try:
                    coupon_group = CouponGroup.objects.get(pk=pk_int, )
                except CouponGroup.DoesNotExist:
                    pass
                else:
                    from apps.coupon.models import Coupon
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
        #print context
        return context

    def post(self, request, *args, **kwargs):
        list_POST_NAME = ['coupon_group_search', 'coupon_group_edit', ]
        get_POST_NAME = request.POST.get('POST_NAME', None, )
        if get_POST_NAME in list_POST_NAME:
            return super(CouponGroupCreateEdit, self, ).post(self, request, *args, **kwargs)
        else:
            from django.http import Http404
            raise Http404

@staff_member_required
def coupon_group_edit(request,
                      coupon_group_id=0,
                      template_name=u'coupon/coupon_group_edit.jinja2.html', ):
    error_message = u''
    coupon_group = None
    from apps.coupon.models import CouponGroup
    if coupon_group_id:
        print coupon_group_id
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
            from datetime import datetime
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
            from apps.coupon.views import coupon_create
            for n in range(how_much_coupons):
                coupon_create(name=name,
                              coupon_group=coupon_group,
                              number_of_possible_uses=number_of_possible_uses,
                              percentage_discount=percentage_discount,
                              start_of_the_coupon=start_of_the_coupon,
                              end_of_the_coupon=end_of_the_coupon, )
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    return render_to_response(template_name=template_name,
                              dictionary={'comment_id': coupon_group_id,
                                          'comment': coupon_group,
                                          'error_message': error_message, },
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )


class CouponCreateEdit(FormView, ):
    from apps.coupon.forms import CouponCreateEditForm
    form_class = CouponCreateEditForm
    template_name = 'coupon/coupon_edit.jingo.html'
    success_url = '/админ/купон/редактор/добавить/'

