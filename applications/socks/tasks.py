# -*- coding: utf-8 -*-

import requests
# For Python 3.0 and later
# import urllib.request

import time
from proj.celery import celery_app

import socket
# import sockschain as socks

import applications.utils as utils
import applications.socks.models as models

__author__ = 'AlexStarov'

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}


@celery_app.task()
def socks_server_get_from_internet():

    """ <--- Start ---> http://www.socks-proxy.net/ """

    # req = urllib.request.Request('http://www.socks-proxy.net/', headers=hdr)

    # content = urllib.request.urlopen(req).read()

    # pars = utils.HTMLParser_socks_proxy()
    # content = content.split('<tbody>')[1]
    # content = content.split('</tbody>')[0]
    # pars.feed(data=content)

    """ <--- End ---> http://www.socks-proxy.net/ """
    """ -------------------------------------------------------------------------------------- """
    """ <--- Start ---> http://hideme.ru/ """

    for n in range(0, 2048, 64):
        time.sleep(2)
        site = 'http://hideme.ru/proxy-list/?start={}#list'.format(n)
        # req = urllib.request.Request(site, headers=hdr)

        # content = urllib.request.urlopen(req).read()

        # if "<td class=tdl>" not in content:
        #     break

        # pars = utils.HTMLParser_hideme()
        # content = content.split('<table class=proxy__t>')[1]
        # content = content.split('</table>')[0]
        # pars.feed(data=content)

    """ <--- End ---> http://hideme.ru/ """
    """ -------------------------------------------------------------------------------------- """
    """ <--- Start ---> http://gatherproxy.com/ """

    r = requests.get(
        url='http://gatherproxy.com/ru/subscribe/login',
    )

    content = r.content.split('<span class="blue">')[1]
    content = content.split('</span>')[0]

    # while True:
        # result = utils.crack_captcha_gatherproxy(
        #     first=content.split()[0],
        #     second=content.split()[2],
        #     operation=content.split()[1],
        # )

        # data = {
        #     'Username': 'starov.alex@gmail.com',
        #     'Password': 'l&;33wU|',
        #     'Captcha': result,
        # }
        # r = requests.post(
        #     url='http://gatherproxy.com/ru/subscribe/login',
        #     cookies=r.cookies,
        #     data=data,
        # )

        # if 'The verify code invalid' not in r.content:
        #     break
        # else:
        #     content = r.content.split('<span class="blue">')[1].split('</span>')[0]

    # r = requests.post(
    #     url='http://gatherproxy.com/sockslist/plaintext',
    #     cookies=r.cookies,
    #     data=data,
    # )

    # content = r.content.split()

    # for host in content:
    #     socks_server_test.apply_async(
    #         queue='socks_server_test',
    #         kwargs={'host': host.split(':')[0],
    #                 'port': host.split(':')[1], }, )

    """ <--- End ---> http://gatherproxy.com/ """
    """ -------------------------------------------------------------------------------------- """


@celery_app.task()
def socks_server_test(*args, **kwargs):

    from_whence = int(kwargs.get('from_whence'))
    host = kwargs.get('host')
    port = int(kwargs.get('port'))
    socks4 = kwargs.get('socks4', False)
    socks5 = kwargs.get('socks5', False)

    # types_socks = set(); types_socks.add(socks.PROXY_TYPE_SOCKS4, socks.PROXY_TYPE_SOCKS5, )
    # if socks4 and not socks5:
    #     types_socks = set(socks.PROXY_TYPE_SOCKS4, )
    # elif not socks4 and socks5:
    #     types_socks = set(socks.PROXY_TYPE_SOCKS5, )

    socket.setdefaulttimeout(10)
    # s = socks.socksocket()
    connect = False
    first_type_socks, second_type_socks = None, None

    # for type_socks in types_socks:
    #     s.setproxy(type_socks, host, port)

    #     try:
    #         s.connect(('smtp.yandex.ru', 25))
    #         recv = s.recv(1024)
            # print("Message after connection request:" + recv.decode())

    #         if recv[:3] != '220':
                # print('220 reply not received from server.')
    #             continue

    #         s.send('HELO proxy.keksik.com.ua\r\n'.encode())
    #         recv = s.recv(1024); print("Message after HeLO command:" + recv.decode())

    #         if recv[:3] != '250':
    #             print('250 reply not received from server.')

    #         connect = True

    #         if not first_type_socks and not second_type_socks:
    #             first_type_socks = type_socks
    #         elif first_type_socks and not second_type_socks:
    #             second_type_socks = type_socks

            # print('first_type_socks: ', first_type_socks, ' second_type_socks: ', second_type_socks, )

    #         quit = "QUIT\r\n"
    #         s.send(quit.encode())
            # print(s.recv(1024).decode())
    #         s.close()

    #     except socket.error as e:
            # print('Exception(socket.error): ', e)
    #         continue

    #     except socks.GeneralProxyError as e:
            # print('Exception(socks.GeneralProxyError): ', e)
    #         continue

    #     except (socks.Socks4Error, socks.Socks5Error) as e:
            # print('Exception(socks.Socks4Error or socks.Socks5Error): ', e)
    #         continue

    socks4 = False
    # if first_type_socks == socks.PROXY_TYPE_SOCKS4\
    #         or second_type_socks == socks.PROXY_TYPE_SOCKS4:
    #     socks4 = True

    # socks5 = False
    # if first_type_socks == socks.PROXY_TYPE_SOCKS5\
    #         or second_type_socks == socks.PROXY_TYPE_SOCKS5:
    #     socks5 = True

    # try:
    #     pr_serv = models.ProxyServer.objects.get(host=host, port=port, )

    # except models.ProxyServer.DoesNotExist:
    #     pr_serv = models.ProxyServer(from_whence=from_whence, host=host, port=port, socks4=socks4, socks5=socks5, )

    # except models.ProxyServer.MultipleObjectsReturned:
    #     pr_serv = models.ProxyServer.objects.filter(host=host, port=port, )
    #     pr_serv[1].delete()
    #     pr_serv = pr_serv[0]

    # if connect:
    #     if socks4:
    #         pr_serv.socks4_success += 1
    #     if socks5:
    #         pr_serv.socks5_success += 1

    #     pr_serv.save()

    #     print('pr_serv: ', pr_serv, ' host: ', host, ' port: ', port, ' OK')

    # else:
    #     if pr_serv.failed > 10:
    #         pr_serv.delete()
    #     else:
    #         pr_serv.failed += 1
    #         pr_serv.save()

    # return connect
