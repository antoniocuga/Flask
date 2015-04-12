#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import urllib
from cookielib import CookieJar
import socks
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import settings
import models


socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

domain = "http://apps5.mineco.gob.pe/proveedor/PageTop.aspx"

db_engine = create_engine(
    settings.DATABASE_DSN,
    echo=settings.DEBUG
)

db = sessionmaker(bind=db_engine)()


def scrapper():

    values = {'__EVENTTARGET': '',
              '__EVENTARGUMENT': '',
              '__VIEWSTATE': '/wEPDwUJODA2Mjc5NjYwDxYEHghPcmRlckRpcgEBAB4IU2VhcmNoQnkLKVtwcm92ZWVkb3IuU2VhcmNoQnksIHByb3ZlZWRvciwgVmVyc2lvbj0xLjAuNTI3NS4yNjQ5MywgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsABYCZg9kFgQCCw8PFgQeCFJvd0NvdW50At+nGh4HVmlzaWJsZWdkFgQCCQ8WAh4EVGV4dAUyPGI+MTwvYj4gLSA8Yj4yNTA8L2I+IGRlIDxiPjQzMSwwNzE8L2I+IHJlc3VsdGFkb3NkAg0PFgIfBAUMPGI+MSw3MjU8L2I+ZAINDxYCHwNnFgICAw9kFgJmD2QWAgIHDw8WAh8DaGRkZEIgsWQML4bShDwnYoDqufHkVWdi8DesHGSmS1MpCDVb',
              '__EVENTVALIDATION': '/wEdAA+oy/EtT2tk5Wj9bfH7JVrjQ/XnI9JNF8oTY7w8H74w/LPTnR9fOc03xnlp6oT8D8NAwiWIc3ifkY498zcTyDajL8NI3r2BJTed5JhUovWhgQyif6KZc1ESStxnceVeoJ6nfZhfGvB9pDnYk8R04DlDyf3bBtJAsREOSv6Bv5NrawDTwwPrxtqjWLIH1uyteWYkhML6BNfAbMNMh70eHArj4Invb0MbNvZAoosAssfcaRNQgFrBJLXW9t9Im8DSBQZB75oOuKkKInsq/TeFqNARJNHCZxrfWXDJZ+50rUXWXykeI6z8FCyClAytDBydSh5htRMgF3esqDbacE/0eau57Rirxs/hWcBcunD9X96Ycw==',
              'grp1':'/304228197369.54',
              'hFiltros': '',
              'hAgrupacion': '6',
              'hAntAgrupacion': '0',
              'hHistorico': '0',
              'hPostedBy': '1'}

    data = urllib.urlencode(values)
    response = opener.open(domain, data)
    content = BeautifulSoup(response.read(), 'html.parser').find("table", {'class', 'Data'})

    for r in content.findAll("tr"):

        cells = r.findAll("td")
        d = cells[1].getText().encode('utf-8')
        item = d.split(":")
        id = ((item[0]).strip()).replace('\xc2\xa0', '')
        departamento = ((item[1]).strip())

        if db.query(
            models.Departamento
        ).filter(
            models.Departamento.id == id
        ).count() == 0:
            _entry = models.Departamento()
            _entry.id = id
            _entry.departamento = departamento

            db.add(_entry)

            try:
                db.commit()
            except:
                db.rollback()


if __name__ == '__main__':

    #Get departments
    scrapper()
