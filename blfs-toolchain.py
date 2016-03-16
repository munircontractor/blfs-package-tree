# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 13:24:57 2016

@author: munir
"""

from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
#from time import sleep

BASE_URL = 'http://linuxfromscratch.org/blfs/view/systemd/'

html = urlopen(BASE_URL).read()
soup = bs(html,'lxml')
sects = soup.findAll("li",{"class" : "sect1"})

pcklist = dict()

for item in sects:
    try:
        if pcklist.has_key(item.contents[1].string):
            print item.contents[1].string + ' already exists.'
            l = lambda x: x if x.strip() <> '' else 'N'
            ovw = l(raw_input('Do you wish to overwrite the URL? (y/N) '))
            if ovw[0].lower == 'y':
                pcklist[item.contents[1].string] = [item.contents[1].attrs['href'],'','','']
        else:
            pcklist[item.contents[1].string] = [item.contents[1].attrs['href'],'','','']
    except KeyError:
        print item.contents[1].string + ' has no href attribute.'

for k in pcklist.iterkeys():
    PCK_URL = BASE_URL + pcklist[k][0]
    html2 = urlopen(PCK_URL).read()
    soup2 = bs(html2,'lxml')
    reqs = soup2.findAll('p',{'class':'required'})
    recs = soup2.findAll('p',{'class':'recommended'})
    opts = soup2.findAll('p',{'class':'optional'})
    
    reqpcks = []
    recpcks = []
    optpcks = []

    for item in reqs:
        for c in item.contents:
            try:
                reqpcks.append(c.attrs['title'])
            except AttributeError:
                pass
            except KeyError:
                pass

    for item in recs:
        for c in item.contents:
            try:
                recpcks.append(c.attrs['title'])
            except AttributeError:
                pass
            except KeyError:
                pass

    for item in opts:
        for c in item.contents:
            try:
                optpcks.append(c.attrs['title'])
            except AttributeError:
                pass
            except KeyError:
                pass

    pcklist[k][1] = reqpcks
    pcklist[k][2] = recpcks
    pcklist[k][3] = optpcks
    
    print 'Finished page: ' + soup2.title.string.strip()
    #print 'Sleeping for 5 secs'
    #sleep(5)
