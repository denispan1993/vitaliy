# coding=utf-8
__author__ = 'Sergey'


def comment_add(request,
                product_url,
                id,
                template_name=u'show_comment_add.jinja2.html', ):
    from apps.comment.models import Comment
    error_message = None
    comment = None
    sessionid = request.COOKIES.get(u'sessionid', None, )
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
                    product = Product.objects.get(pk=product_id, url=product_url, )
                except Product.DoesNotExist:
                    error_message = u'Отсутсвует Продукт с такими данными.'
                else:
                    commenter_name = request.POST.get(u'commenter_name', None, )
                    if not commenter_name:
                        error_message = u'Отсутсвует имя комментирующего.'
                    else:
                        comment = request.POST.get(u'comment', None, )
                        if not comment:
                            error_message = u'Отсутсвует комментарий'
                        else:
                            require_a_response = request.POST.get(u'require_a_response', None, )
                            if require_a_response:
                                email_for_response = request.POST.get(u'email_for_response', None, )
                                if email_for_response:
                                    if request.user.is_authenticated() and request.user.is_active:
                                        user_id_ = request.session.get(u'_auth_user_id', None, )
                                        from django.contrib.auth.models import User
                                        user_obj = User.objects.get(pk=user_id_, )
                                        comment = Comment.objects.create(content_type=product.content_type,
                                                                         object_id=product.pk,
                                                                         user=user_obj,
                                                                         sessionid=sessionid,
                                                                         name=commenter_name,
                                                                         comment=comment,
                                                                         require_a_response=require_a_response,
                                                                         email_for_response=email_for_response, )

                                    else:
                                        comment = Comment.objects.create(content_type=product.content_type,
                                                                         object_id=product.pk,
                                                                         user=None,
                                                                         sessionid=sessionid,
                                                                         name=commenter_name,
                                                                         comment=comment,
                                                                         require_a_response=require_a_response,
                                                                         email_for_response=email_for_response, )

                            else:
                                rating = request.POST.get(u'rating', None, )
                                print(rating, )
                                if rating == u'':
                                    if request.user.is_authenticated() and request.user.is_active:
                                        user_id_ = request.session.get(u'_auth_user_id', None, )
                                        from django.contrib.auth.models import User
                                        user_obj = User.objects.get(pk=user_id_, )
                                        comment = Comment.objects.create(content_type=product.content_type,
                                                                         object_id=product.pk,
                                                                         user=user_obj,
                                                                         sessionid=sessionid,
                                                                         name=commenter_name,
                                                                         comment=comment, )
                                    else:
                                        comment = Comment.objects.create(content_type=product.content_type,
                                                                         object_id=product.pk,
                                                                         user=None,
                                                                         sessionid=sessionid,
                                                                         name=commenter_name,
                                                                         comment=comment, )
                                else:
                                    try:
                                        rating = int(rating, )
                                    except ValueError:
                                        email_for_response = u'Неправильный рэйтинг товара.'
                                    else:
                                        if request.user.is_authenticated() and request.user.is_active:
                                            user_id_ = request.session.get(u'_auth_user_id', None, )
                                            from django.contrib.auth.models import User
                                            user_obj = User.objects.get(pk=user_id_, )
                                            comment = Comment.objects.create(content_type=product.content_type,
                                                                             object_id=product.pk,
                                                                             user=user_obj,
                                                                             sessionid=sessionid,
                                                                             name=commenter_name,
                                                                             comment=comment,
                                                                             rating=rating, )
                                        else:
                                            comment = Comment.objects.create(content_type=product.content_type,
                                                                             object_id=product.pk,
                                                                             user=None,
                                                                             sessionid=sessionid,
                                                                             name=commenter_name,
                                                                             comment=comment,
                                                                             rating=rating, )
    if isinstance(comment, Comment, ) and not error_message:
        """ Если комментарий добавлен в базу
        Говорим спасибо за оставленный комментарий или вопрос.
        Комментарий к товару появится на сайте после прохождения модерации Администрацией сайта """
        from django.shortcuts import redirect
        return redirect(to='comment_add_successfully', product_url=product_url, id=id, )

    from apps.utils.captcha.views import Captcha
    keys = Captcha(request, )
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message,
                                              'keys': keys, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


def comment_add_successfully(request,
                             product_url,
                             id,
                             template_name=u'show_comment_add_successfully.jinja2.html', ):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  # dictionary={'error_message': error_message, },
                                  #             # 'orders': orders, },  # 'html_text': html_text, },
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