"""SMTP email backend class."""
#import smtplib
from apps.delivery.smtp import lib as smtplib

from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.utils import DNS_NAME
from django.core.mail.message import sanitize_address

import dkim # http://hewgill.com/pydkim


class DKIMBackend(EmailBackend):

    def __init__(self, proxy=None,
                 host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                 dkim_selector=None, dkim_domain=None, dkim_private_key=None,
                 **kwargs):

        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self.dkim_selector = dkim_selector
        self.dkim_domain = dkim_domain
        self.dkim_private_key = dkim_private_key

    def open(self):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        connection_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
        # If local_hostname is not specified, socket.getfqdn() gets used.
        # For performance, we use the cached FQDN for local_hostname.
        connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout
        if self.use_ssl:
            connection_params.update({
                'keyfile': self.ssl_keyfile,
                'certfile': self.ssl_certfile,
            })
        try:
            self.connection = connection_class(self.host, self.port, **connection_params)

            # TLS/SSL are mutually exclusive, so only attempt TLS over
            # non-secure connections.
            if not self.use_ssl and self.use_tls:
                self.connection.ehlo()
                self.connection.starttls(keyfile=self.ssl_keyfile, certfile=self.ssl_certfile)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise

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
