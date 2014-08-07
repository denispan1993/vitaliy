__author__ = 'user'


def update_sessionid(request, sessionid_old, sessionid_now, ):
    # from django.contrib.sessions.models import Session
    # session_new = Session.objects.get(session_key=sessionid, )
    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        from django.contrib.auth.models import User
        try:
            user_id_ = int(user_id_, )
        except ValueError:
            user_object_ = None
        else:
            user_object_ = User.objects.get(pk=user_id_, )
    else:
        user_object_ = None
    from apps.cart.models import Cart
    try:
        Cart.objects.get(sessionid=sessionid_old, ).updated(user=user_object_,
                                                            sessionid=sessionid_now, )
    except Cart.DoesNotExist:
        print 'Cart not Existent.'
        pass
    else:
        print 'Ok.'
    from apps.account.models import Session_ID
    try:
        Session_ID.objects.get(sessionid=sessionid_old, ).updated(user=user_object_,
                                                                  sessionid=sessionid_now, )
    except Session_ID.DoesNotExist:
        print 'Session_ID not Existent.'
        pass
    else:
        print 'Ok.'
    return None
