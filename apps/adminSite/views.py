# coding=utf-8


from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_panel(request,
                template_name=u'admin_panel.jinja2.html', ):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={# 'error_message': error_message,
                                              # 'orders': orders, },  # 'html_text': html_text, },
                                  },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


@staff_member_required
def order_search(request,
                 template_name=u'order/order_search.jinja2.html', ):
    error_message = u''
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'order_search':
            order_id = request.POST.get(u'order_id', None, )
            if order_id:
                try:
                    order_id = int(order_id, )
                except ValueError:
                    error_message = u'Некорректно введен номер заказа.'
                else:
                    from apps.cart.models import Order
                    try:
                        order = Order.objects.get(pk=order_id, )
                    except Order.DoesNotExist:
                        error_message = u'Заказа с таким номером не существует.'
                    else:
                        order_id = '%06d' % order_id
                        from django.shortcuts import redirect
                        return redirect(to='order_edit', id=order_id, )
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    from apps.cart.models import Order
    orders = Order.objects.all()
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message,
                                              'orders': orders, },  # 'html_text': html_text, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


@staff_member_required
def order_edit_product_add(request,
                           id,
                           template_name=u'order/order_edit_product_add.jinja2.html', ):
    from django.shortcuts import redirect
    if id:
        try:
            order_id = int(id, )
        except ValueError:
            error_message = u'Некорректно введен номер заказа.'
            return redirect(to='order_search', )
        else:
            from apps.cart.models import Order
            try:
                order = Order.objects.get(pk=id, )
            except Order.DoesNotExist:
                error_message = u'В базе отсутсвует заказ с таким номером.'
                return redirect(to='order_search', )
    else:
        error_message = u'Отсутсвует номер заказа.'
        return redirect(to='order_search', )

#    from apps.static.models import Static
#    try:
#        page = Static.objects.get(url=static_page_url, )
#    except Static.DoesNotExist:
#        from django.http import Http404
#        raise Http404
#    import markdown
#    if page:
#        html_text = markdown.markdown(page.text, )
#    else:
#        html_text = None
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'order_id': order_id,
                                              'order': order, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    # from datetime import datetime
    # from apps.utils.datetime2rfc import datetime2rfc
    # response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response


@staff_member_required
def order_edit(request,
               id,
               template_name=u'order/order_edit.jinja2.html', ):
    from django.shortcuts import redirect
    if id:
        try:
            order_id = int(id, )
        except ValueError:
            error_message = u'Некорректно введен номер заказа.'
            return redirect(to='order_search', )
        else:
            from apps.cart.models import Order
            try:
                order = Order.objects.get(pk=id, )
            except Order.DoesNotExist:
                error_message = u'В базе отсутсвует заказ с таким номером.'
                return redirect(to='order_search', )
    else:
        error_message = u'Отсутсвует номер заказа.'
        return redirect(to='order_search', )

#    from apps.static.models import Static
#    try:
#        page = Static.objects.get(url=static_page_url, )
#    except Static.DoesNotExist:
#        from django.http import Http404
#        raise Http404
#    import markdown
#    if page:
#        html_text = markdown.markdown(page.text, )
#    else:
#        html_text = None
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'order_id': order_id,
                                              'order': order, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    # from datetime import datetime
    # from apps.utils.datetime2rfc import datetime2rfc
    # response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response


@staff_member_required
def comment_search(request,
                   template_name=u'comment/comment_search.jinja2.html', ):
    error_message = u''
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'comment_search':
            comment_id = request.POST.get(u'comment_id', None, )
            if comment_id:
                try:
                    comment_id = int(comment_id, )
                except ValueError:
                    error_message = u'Некорректно введен номер Комментария.'
                else:
                    from apps.comment.models import Comment
                    try:
                        comment = Comment.objects.get(pk=comment_id, )
                    except Comment.DoesNotExist:
                        error_message = u'Комментария с таким номером не существует.'
                    else:
                        comment_id = '%06d' % comment_id
                        from django.shortcuts import redirect
                        return redirect(to='comment_edit', id=comment_id, )
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    from apps.comment.models import Comment
    comments = Comment.objects.all()
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message,
                                              'comments': comments, },  # 'html_text': html_text, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


@staff_member_required
def comment_edit(request,
                 id,
                 template_name=u'comment/comment_edit.jinja2.html', ):
    error_message = u''
    from apps.comment.models import Comment
    from django.shortcuts import redirect
    if id:
        try:
            comment_id = int(id, )
        except ValueError:
            error_message = u'Некорректный номер комментария.'
        else:
            try:
                comment = Comment.objects.get(pk=comment_id, )
            except Comment.DoesNotExist:
                error_message = u'В базе отсутсвует комментарий с таким номером.'
            else:
                error_message = u'Отсутсвует номер комментария.'
    if not 'comment_id' in locals() and not 'comment_id' in globals()\
            or not 'comment' in locals() and not 'comment' in globals():
        return redirect(to='comment_search', )
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'comment_dispatch':
            comment_id = request.POST.get(u'comment_id', None, )
            if comment_id:
                try:
                    id = int(comment_id, )
                except ValueError:
                    error_message = u'Некорректный номер комментария. № 2'
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'comment_id': comment_id,
                                              'comment': comment, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


@staff_member_required
def coupon_group_search(request,
                        template_name=u'coupon/coupon_group_search.jinja2.html', ):
    error_message = u''
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'coupon_group_search':
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

#from django.views.generic.edit import FormView


#class CouponGroupCreateEdit(FormView, ):
#    from apps.coupon.forms import CouponGroupCreateEditForm
#    form_class = CouponGroupCreateEditForm
#    template_name = 'coupon/coupon_group_edit.jinja2.html'
#    success_url = '/админ/купон/группа/редактор/'

#    def form_valid(self, form, ):
#        from apps.coupon.models import CouponGroup
#        CouponGroup.objects.create(**form.cleaned_data)
#        return super(CouponGroupCreateEdit, self, ).form_valid(form, )




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
