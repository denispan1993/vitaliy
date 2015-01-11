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
