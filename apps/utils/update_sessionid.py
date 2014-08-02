__author__ = 'user'


def update_sessionid(request, sessionid_old, sessionid, ):
    from django.contrib.sessions.models import Session
    session_new = Session.objects.get(session_key=sessionid, )
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
    print sessionid_old, sessionid
    from apps.cart.models import Cart
    try:
#        cart1 = Cart.objects.get(session=sessionid_old, ).updated(user=user_object_,
#                                                                 session=session_new, )
        cart1 = Cart.objects.get(session=sessionid_old, )
    except Cart.DoesNotExist:
        pass
    else:
        print cart1
    try:
#        cart1 = Cart.objects.get(session=sessionid_old, ).updated(user=user_object_,
#                                                                 session=session_new, )
        cart_all = Cart.objects.all()
    except Cart.DoesNotExist:
        pass
    else:
        print cart_all
        try:
            print cart_all[0]
            print cart_all[0].session
        except IndexError:
            pass
    return None
