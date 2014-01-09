__author__ = 'user'


def datetime2rfc(dt):
    import time
    from email.utils import formatdate
    dt = time.mktime(dt.timetuple())
    return formatdate(dt, usegmt=True)
