# -*- coding: utf-8 -*-
# /apps/product/utils.py
from django.http import Http404
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from proj.settings import SERVER

from .models import Category

__author__ = 'AlexStarov'


def debug() -> str:
    """
        Debug information

    :return: str of debug information
    """
    import inspect
    previous_frame = inspect.currentframe().f_back
    (filename, line_number,
     function_name, lines, index) = inspect.getframeinfo(previous_frame)
    return 'Debug: filename: {filename} | function_name: {function_name} | line number: {line_number}'.\
        format(filename=filename, line_number=line_number, function_name=function_name)


def get_ids(current_category: Category) -> set:
    """
        Get and return id's of all referring categories to the current category

    :param current_category: current user category
    :return: set of id referring categories to the current category
    """

    ids = set()
    ids.add(current_category.id)

    ids_children = set()
    ids_children.add(current_category.id)

    while True:
        # Берем все подкатегории входящие в текущюю
        # TODO: Дописать процедуру в базу даннх которая бы одним запросом отдавала все id нижестоящих категорий

        qs_list = Category.objects\
            .filter(parent_id__in=ids_children)\
            .values_list('id', flat=True, )

        if len(qs_list) > 0:
            ids_children = set(id for id in qs_list)
            ids.update(ids_children)
        else:
            break

    return ids


def get_current_category(current_category, product):
    """ Вернуть "текущую" категорию """

    if current_category:
        categories_of_product = product.category.all()

        categories_of_product_pk = [category.pk for category in categories_of_product]

        try:
            current_category = int(current_category)

            if current_category in categories_of_product_pk:
                return categories_of_product.get(pk=current_category)

        except (TypeError, ValueError):
            pass

    """ Ищем главные категории """
    main_category_of_product = product.producttocategory_set.filter(is_main=True)
    # main_category_of_product = categories_of_product.filter(is_main=True)

    if len(main_category_of_product) == 1:
        return main_category_of_product[0].category

    elif len(main_category_of_product) > 1:
        # send_error_manager(product=product, error_id=1, )
        return main_category_of_product[0].category

    elif len(main_category_of_product) == 0:
        # send_error_manager(product=product, error_id=1, )
        print(debug())
        print('Error: if len(main_category_of_product) == 0: product id:', product.pk)

    """ Если не одна из категорий не назнчена главная """
    all_category_of_product = product.producttocategory_set.all()

    if len(all_category_of_product) == 1:
        all_category_of_product[0].is_main = True
        all_category_of_product[0].save()
        return all_category_of_product[0].category

    elif len(all_category_of_product) > 1:
        # send_error_manager(product=product, error_id=1, )
        return all_category_of_product[0].category

    elif len(all_category_of_product) == 0:
        # send_error_manager(product=product, error_id=1, )
        print(debug())
        print('Error: if len(all_category_of_product) == 0: raise Http404: product id:', product.pk)

        raise Http404


def send_error_manager(product=None, error_id=None, ):
    """ Отправка ошибки мэнеджеру """
    subject = u'В товаре № %d ошибка' % product.pk
    html_content = render_to_string('error_email/error_email.jinja2.html',
                                    {'product': product, 'error_id': error_id, })
    text_content = strip_tags(html_content, )
    from_email = u'site@keksik.com.ua'
#                to_email = u'mamager@keksik.com.ua'
    if SERVER:
        to_email = u'manager@keksik.com.ua'
    else:
        to_email = u'alex.starov@keksik.com.ua'

    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                             fail_silently=False, )
    msg = EmailMultiAlternatives(subject=subject,
                                 body=text_content,
                                 from_email=from_email,
                                 to=[to_email, ],
                                 connection=backend, )
    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )
    msg.send(fail_silently=False, )
    return None


def get_or_create_Viewed(request,
                         product=None,
                         product_pk=None,
                         user_obj=None,
                         sessionid=None, ):
    """ Взять последние просмотренные товары """

    if request.user.is_authenticated()\
            and request.user.is_active\
            and not user_obj:
        user_id_ = request.session.get(u'_auth_user_id', None, )

        from django.contrib.auth import get_user_model

        user_obj = get_user_model().objects.get(pk=user_id_, )

    if not sessionid:
        sessionid = request.COOKIES.get(u'sessionid', None, )

    if not product and product_pk:
        from .views import get_product
        product = get_product(product_pk, )

    content_type = None
    product_pk = None

    from .models import Viewed
    if product:
        content_type = product.content_type
        product_pk = product.pk
        from django.core.exceptions import MultipleObjectsReturned
        try:
            viewed, created = Viewed.objects.get_or_create(content_type=content_type,
                                                           object_id=product_pk,
                                                           user_obj=user_obj,
                                                           sessionid=sessionid, )
        except MultipleObjectsReturned:
            viewed = Viewed.objects.filter(content_type=content_type,
                                           object_id=product_pk,
                                           user_obj=user_obj,
                                           sessionid=sessionid, )
            viewed.delete()
        else:
            if not created and viewed is not []:
                from django.utils import timezone
                viewed.last_viewed = timezone.now()
                viewed.save()

    try:
        viewed = Viewed.objects.filter(user_obj=user_obj,
                                       sessionid=sessionid, )\
            .order_by('-last_viewed', )\
            .exclude(content_type=content_type, object_id=product_pk, )

        if len(viewed) > 9:
            viewed[viewed.count() - 1].delete()  # .latest('last_viewed', )

        return viewed

    except Viewed.DoesNotExist:
        return None
