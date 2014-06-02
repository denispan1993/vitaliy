# coding=utf-8
__author__ = 'Sergey'


def comment_add(request,
                product_url,
                id,
                template_name=u'show_comment_add.jinja2.html', ):
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'comment_add':
            try:
                product_id = int(id, )
            except ValueError:
                error_message = u'Некорректно значение id продукта.'
            else:
                from apps.product.models import Product
                try:
                    product = Product.objects.get(pk=id, url=product_url, )
                except Product.DoesNotExist:
                    error_message = u'Отсутсвует Продукт с такими данными.'
                else:
                    commenter_name = request.POST.get(u'commenter_name', None, )
                    comment = request.POST.get(u'comment', None, )
                    require_a_response = request.POST.get(u'require_a_response', None, )
                    email_for_response = request.POST.get(u'email_for_response', None, )
                    rating = request.POST.get(u'rating', None, )
                    from apps.comment.models import Comment
                    if request.user.is_authenticated() and request.user.is_active:
                        user_id_ = request.session.get(u'_auth_user_id', None, )
                        from django.contrib.auth.models import User
                        user_obj = User.objects.get(pk=user_id_, )
                        comment = Comment.objects.create(content_type=product.content_type,
                                                         object_id=product.pk,
                                                         user_obj=user_obj,
                                                         sessionid=None, )
                    else:
                        sessionid = request.COOKIES.get(u'sessionid', None, )
                        comment = Comment.objects.create(content_type=product.content_type,
                                                         object_id=product.pk,
                                                         user_obj=None,
                                                         sessionid=sessionid, )


                    from django.shortcuts import redirect
                    return redirect(to='order_edit', id=order_id, )
    else:
        error_message = u''
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
#    from apps.cart.models import Order
#    orders = Order.objects.all()
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message, },
#                                              'orders': orders, },  # 'html_text': html_text, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


from django.contrib.admin.views.decorators import staff_member_required


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