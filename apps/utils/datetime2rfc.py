# coding=utf-8
__author__ = 'Alex Starov'


def datetime2rfc(dt):
    import time
    from email.utils import formatdate
    dt = time.mktime(dt.timetuple())
    return formatdate(dt, usegmt=True)
