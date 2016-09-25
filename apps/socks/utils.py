# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import models

__author__ = 'AlexStarov'

gl_ip, gl_port, gl_type = False, False, False
gl_start_div, gl_start_em = False, False

number = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Zero': 0,
}


class HTMLParser_hideme(HTMLParser):
    """ http://hideme.ru/ """

    def handle_starttag(self, tag, attrs):
        global gl_ip, gl_port, gl_type, gl_start_div, gl_start_em

        if gl_ip and tag=='td':
            gl_port = True
        for attr in attrs:
            if tag == 'td' and len(attr) > 1 and attr[1] == 'tdl':
                gl_ip = True

        if tag == 'div':
            gl_start_div = True

        if gl_start_div and tag == 'span':
            gl_ip, gl_port = False, False

        if tag == 'em':
            gl_start_em = True

        if gl_start_em and tag == 'td':
            gl_type = True

    def handle_data(self, data):
        global gl_ip, gl_port, gl_type, gl_start_div, gl_start_em
        global pr_serv

        if gl_ip and not gl_port:
            gl_start_div, gl_start_em = False, False

            try:
                pr_serv = models.ProxyServer.objects.get(host = data, )
            except models.ProxyServer.DoesNotExist:
                pr_serv = models.ProxyServer(from_whence=1, host=data, )
            except models.ProxyServer.MultipleObjectsReturned:
                pr_serv = models.ProxyServer.objects.filter(host = data, )
                pr_serv[1].delete()
                pr_serv = pr_serv[0]

        elif gl_ip and gl_port:
            pr_serv.port = data

        elif gl_type:
            gl_start_em, gl_type = False, False

            if 'HTTPS' in data:
                data = data.split('HTTPS')
                pr_serv.https = True
                data = ''.join(data)

            if 'HTTP' in data:
                pr_serv.http = True

            if '4' in data:
                pr_serv.socks4 = True

            if '5' in data:
                pr_serv.socks5 = True

            pr_serv.save()

gl_tag_td = 0


class HTMLParser_socks_proxy(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global gl_tag_td
        if tag == 'tr':
            gl_tag_td = 0
        if tag == 'td':
            gl_tag_td += 1

    def handle_data(self, data):
        global gl_tag_td
        global pr_serv

        if gl_tag_td == 1:

            try:
                pr_serv = models.ProxyServer.objects.get(host=data, )
            except models.ProxyServer.DoesNotExist:
                pr_serv = models.ProxyServer(from_whence=2, host=data, )
            except models.ProxyServer.MultipleObjectsReturned:
                pr_serv = models.ProxyServer.objects.filter(host=data, )
                pr_serv[1].delete()
                pr_serv = pr_serv[0]

        elif gl_tag_td == 2:
            pr_serv.port = data

        elif gl_tag_td == 5:
            if '4' in data:
                pr_serv.socks4 = True
            if '5' in data:
                pr_serv.socks5 = True
            pr_serv.save()


def crack_captcha_gatherproxy(first, second, operation, ):
    """ http://gatherproxy.com/ru/subscribe/login """

    try:
        first = int(first, )
    except ValueError as e:
        # print('ValueError: ', e, ' first: ', first)
        first = number[first]

    try:
        second = int(second)
    except ValueError as e:
        # print('ValueError: ', e, ' second: ', second)
        second = number[second]

    if 'plus' in operation or '+' in operation:
        return first + second

    elif 'minus' in operation or '-' in operation:
        return first - second

    elif 'multiplied' in operation or 'X' in operation:
        return first * second
