"""SMTP email backend class."""
import smtplib
import ssl
import threading

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.utils import DNS_NAME
from django.core.mail.message import sanitize_address

import dkim # http://hewgill.com/pydkim


class DKIMBackend(EmailBackend):

    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                 dkim_selector=None, dkim_domain=None, dkim_private_key=None,
                 **kwargs):

        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self.dkim_selector = dkim_selector
        self.dkim_domain = dkim_domain
        self.dkim_private_key = dkim_private_key

    def _send(self, email_message):
        """A helper method that does the actual sending + DKIM signing."""
        if not email_message.recipients():
            return False

        from_email = sanitize_address(email_message.from_email, email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]

        message_string = email_message.message().as_string()

        signature = ''
        if self.dkim_selector and self.dkim_domain and self.dkim_private_key:
            signature = dkim.sign(message_string,
                                  self.dkim_selector,
                                  self.dkim_domain,
                                  self.dkim_private_key)

        try:
            self.connection.sendmail(from_email,
                                     recipients,
                                     signature+message_string.as_bytes(linesep='\r\n'))
        except:
            if not self.fail_silently:
                raise
            return False
        return True
