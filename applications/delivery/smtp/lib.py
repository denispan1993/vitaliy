# Python SMTP via Socks

import smtplib
import socket
import sockschain as socks
from sys import stderr

__author__ = 'Auth0r'
__author_remake__ = 'AlexStarov'
__twitter__ = 'https://twitter.com/vxlab_info/'
__version__ = '28.04.2016'
__version_remake__ = '20.09.2016'


class SMTP(smtplib.SMTP):

    def __init__(self, host='', port=0,
                 proxy=None,
                 local_hostname=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):

        self.timeout = timeout
        self.esmtp_features = {}

        # -------------------------------------------
        self.proxy = proxy
        # -------------------------------------------

        if host:
            (code, msg) = self.connect(host, port)
            if code != 220:
                raise smtplib.SMTPConnectError(code, msg)
        if local_hostname is not None:
            self.local_hostname = local_hostname
        else:
            fqdn = socket.getfqdn()
            if '.' in fqdn:
                self.local_hostname = fqdn
            else:
                addr = '127.0.0.1'
                try:
                    addr = socket.gethostbyname(socket.gethostname())
                except socket.gaierror:
                    pass
                self.local_hostname = '[%s]' % addr

    def _get_socket(self, host, port, timeout):
        if self.debuglevel > 0:
            print>>stderr, 'connect:', (host, port)
        # -------------------------------------------
        socket_proxy = socks.socksocket()
        socket_proxy.setproxy(self.proxy[0], self.proxy[1], self.proxy[2])
        socket_proxy.connect((host, port))
        if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
            socket_proxy.settimeout(timeout)
        return socket_proxy
        # -------------------------------------------

class SMTP_SSL(SMTP):
    pass