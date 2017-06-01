# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def update_sessionid(request, sessionid_old, sessionid_now, ):
    # from django.contrib.sessions.models import Session
    # session_new = Session.objects.get(session_key=sessionid, )
    user_object_ = None
    try:
        if request.user.is_authenticated():
            if request.user.is_active:
                user_id_ = request.session.get(u'_auth_user_id', None, )
                # from django.contrib.auth.models import User
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user_id_ = int(user_id_, )
                except ValueError:
                    user_object_ = None
                else:
                    user_object_ = User.objects.get(pk=user_id_, )
    except AttributeError:
        """ Пользователь 100% в первый раз """
        pass
    from applications.cart.models import Cart
    try:
        cart = Cart.objects.get(sessionid=sessionid_old, )
    except Cart.DoesNotExist:
        # print 'Cart not Existent.'
        pass
    else:
        # print user_object_
        cart.user = user_object_
        cart.sessionid = sessionid_now
        cart.save()
        # print cart.user, 'User - Ok.'
    from applications.account.models import Session_ID
    try:
        session_id = Session_ID.objects.get(sessionid=sessionid_old, )
    except Session_ID.DoesNotExist:
        # print 'Session_ID not Existent.'
        pass
    else:
        # session_id.__dict__.update(user=user_object_, sessionid=sessionid_now, )
        session_id.user = user_object_
        session_id.sessionid = sessionid_now
        session_id.save()
        # print 'Ok.'
    return None
