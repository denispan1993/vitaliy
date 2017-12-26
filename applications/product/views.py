# -*- coding: utf-8 -*-
# /apps/product/views.py
from datetime import datetime

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template

from applications.cart.order import get_cart_or_create
from applications.utils.datetime2rfc import datetime2rfc
from proj.settings import SERVER, CACHE_TIMEOUT
from .models import Category, Product
from .utils import debug, get_ids, get_current_category, get_or_create_Viewed

__author__ = 'AlexStarov'


def show_basement_category(request,
                           template_name=u'category/show_basement_category.jinja2', ):
    try:
        basement_categories = Category.objects.basement()
    except Category.DoesNotExist:
        raise Http404

    t = get_template(template_name)
    html = t.render(request=request, context={u'basement_categories': basement_categories, },)
    response = HttpResponse(html, )
    # Мы не можем выяснить когда менялись внутринние подкатегории.
    # Поэтому мы не отдаем дату изменения текущей категории.
    # response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
    return response


def show_category(request,
                  category_url,
                  id,
                  template_name=u'category/category.jinja2', ):

    request.session[u'category'] = True
    try:
        current_category = get_category(pk=id)
        # current_category = Category.objects.get(pk=id, url=category_url, )
        request.session[u'current_category'] = current_category.pk

    except Category.DoesNotExist:
        print(debug())
        print('Error: except Category.DoesNotExist: raise Http404')
        raise Http404

    # Разбираемся с сортировкой элементов на странице
    sorting_items_on_page_GET = request.GET.get('sorting', False)
    print('sorting_items_on_page_GET:', sorting_items_on_page_GET)
    sorting_items_on_page_session = request.session.get('sorting_items_on_page', False)
    print('sorting_items_on_page_session:', sorting_items_on_page_session)

    page = False
    sorting = 'popular'
    if not sorting_items_on_page_GET and not sorting_items_on_page_session:
        request.session['sorting_items_on_page'] = sorting

    elif (sorting_items_on_page_GET and not sorting_items_on_page_session)\
            or (sorting_items_on_page_GET and sorting_items_on_page_session
            and sorting_items_on_page_GET != sorting_items_on_page_session):
        request.session['sorting_items_on_page'] = sorting_items_on_page_GET
        sorting = sorting_items_on_page_GET
        page = 1

    elif not sorting_items_on_page_GET and sorting_items_on_page_session:
        sorting = sorting_items_on_page_session

    if sorting == 'popular':
        sorting = 'price'
    elif sorting == 'price_min_to_max':
        sorting = 'price'
    elif sorting == 'price_max_to_min':
        sorting = '-price'
    elif sorting == 'novelties':
        sorting = 'updated_at'

    # Производим выборку элементов с указаной сортировкой
    products = Product.objects\
        .published(category__in=get_ids(current_category=current_category))\
        .order_by(sorting)\
        .distinct()

    # Разбираемся с количеством эллементов на странице
    items_on_page_GET = request.GET.get('items_on_page', False)
    items_on_page_session = request.session.get('items_on_page', False)

    if items_on_page_GET and items_on_page_session and items_on_page_GET == items_on_page_session:
        items_on_page = items_on_page_GET

    elif items_on_page_GET and (items_on_page_session or not items_on_page_session) and items_on_page_GET != items_on_page_session:
        items_on_page = items_on_page_GET
        request.session['items_on_page'] = items_on_page_GET
        page = 1

    elif not items_on_page_GET and not items_on_page_session:
        items_on_page = 8
        request.session['items_on_page'] = 8

    elif not items_on_page_GET and items_on_page_session:
        items_on_page = items_on_page_session

    if not page:
        page = request.GET.get('page', 1)

    # Начинаем пагинацию
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(products, items_on_page)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    t = get_template(template_name, )

    html = t.render(request=request,
                    context={'current_category': current_category,
                             'products': products, },)

    return HttpResponse(html, )


def show_product(request,
                 product_url,
                 id,
                 template_name=u'product/show_product.jinja2', ):

    current_category = request.session.get(u'current_category', None, )

    request.session[u'product'] = True

    if request.method == 'POST':
        # if request.session.get(u'cookie', False, ):
        # if cookie:
        # if request.session.test_cookie_worked():

        action = request.POST.get(u'action', None, )
        if action == u'addtocard' or action == u'makeanorder':

            product_pk = request.POST.get(u'product_pk', None, )
            product_url = request.POST.get(u'product_url', None, )
            quantity = request.POST.get(u'quantity', None, )

            try:
                product = get_product(pk=id, )
                # product = Product.objects.get(pk=product_pk, url=product_url, )

                add_to_cart(request=request,
                            product=product,
                            int_product_pk=product_pk,
                            quantity=quantity, )

            except Product.DoesNotExist:
                print(debug())
                print('Error: except Product.DoesNotExist: raise Http404')
                raise Http404

            if action == u'makeanorder':
                return redirect(to='cart:show_cart', )

            current_category = get_current_category(current_category=current_category,
                                                    product=product)
            request.session[u'current_category'] = current_category.pk
            return HttpResponseRedirect(current_category.get_absolute_url(), )

        else:
            print(debug())
            print("Error: if action == u'addtocard' or action == u'makeanorder': raise Http404")
            raise Http404
        # else:
        #     raise Http404
    else:
        product = get_product(pk=id, )

        product.get_or_create_ItemID()
        viewed = get_or_create_Viewed(request=request, product=product, )
        # product_is_availability = product.is_availability

        current_category = get_current_category(current_category=current_category, product=product)
        request.session[u'current_category'] = current_category.pk

        quantity_ = product.minimal_quantity
        minimal_quantity_ = product.minimal_quantity
        quantity_of_complete_ = product.quantity_of_complete

    response = render(request=request,
                      template_name=template_name,
                      context=locals(),
                      # context_instance=RequestContext(request, ),
                      content_type='text/html', )
    if SERVER:
        updated_at = product.updated_at
    else:
        updated_at = datetime.now()

    response['Last-Modified'] = datetime2rfc(updated_at, )
    return response


def get_category(pk, ):
    if not pk:
        print(debug())
        print('Error: if pk: raise Http404')
        raise Http404

    if isinstance(pk, str):
        try:
            pk = int(pk, )
        except (TypeError, ValueError, ):
            print(debug())
            print('Error: except (TypeError, ValueError, ): raise Http404')
            raise Http404

    cache_key = 'cat-%06d' % pk
    cat = cache.get(cache_key, )

    if not cat:
        try:
            cat = Category.objects.get(pk=pk, )
            cache.set(cache_key, cat, CACHE_TIMEOUT, )
        except Category.DoesNotExist:
            print(debug())
            print('Error: except Category.DoesNotExist: raise Http404')
            raise Http404

    return cat


def get_product(pk, ):
    if not pk:
        print(debug())
        print('Error: if pk: raise Http404')
        raise Http404

    if isinstance(pk, str):
        try:
            pk = int(pk, )
        except (TypeError, ValueError,):
            print(debug())
            print('Error: except (TypeError, ValueError, ): raise Http404')
            raise Http404

    cache_key = 'prod-%06d' % pk
    prod = cache.get(cache_key, )

    if not prod:
        try:
            prod = Product.objects.get(pk=pk, )
            cache.set(cache_key, prod, CACHE_TIMEOUT, )
        except Product.DoesNotExist:
            print(debug())
            print('Error: except Product.DoesNotExist: raise Http404')
            raise Http404

    return prod


def add_to_cart(request,
                product=None,
                int_product_pk=None,
                quantity=None, ):
    if not product:
        product = get_product(int_product_pk, )

    """ Взятие корзины, или создание если её нету """
    product_cart, created = get_cart_or_create(request, created=True, )
    from applications.cart import models as models_cart
    try:
        """ Присутсвие конкретного продукта в корзине """
        product_in_cart = product_cart.cart.get(product_id=product.pk, )
    except models_cart.Product.DoesNotExist:

        """ Занесение продукта в корзину если его нету """
        if not quantity:
            quantity = product.minimal_quantity  # Минимальное количество заказа

        """ Временная хрень.
            Так как потом возможно нужно будет перейти на количество с дробной частью. """
        try:
            quantity = int(quantity, )
        except ValueError:
            if '.' in quantity:
                quantity = quantity.split('.')[0]
            elif ',' in quantity:
                quantity = quantity.split(',')[0]
            else:
                quantity = 1

            try:
                quantity = int(quantity, )
            except ValueError:
                quantity = 1

        print('key=', product_cart,
              'product=', product,
              'price=', product.price / 2 if product.is_availability == 2 else product.price,
              'percentage_of_prepaid=', 50 if product.is_availability == 2 else 100,
              'quantity=', quantity, )

        product_in_cart = models_cart.Product.objects.create(
            key=product_cart,
            product=product,
            price=product.price / 2 if product.is_availability == 2 else product.price,
            # True - Товар доступен под заказ.
            available_to_order=True if product.is_availability == 2 else False,
            # 50% - предоплата.
            percentage_of_prepaid=50 if product.is_availability == 2 else 100,
            quantity=quantity, )
    else:
        if not quantity:
            quantity = product.quantity_of_complete  # Количество единиц в комплекте
        product_in_cart.sum_quantity(quantity, )  # quantity += exist_cart_option.quantity
        product_in_cart.update_price_per_piece()

    return product_cart, product_in_cart
