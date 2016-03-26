# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 13:24:57 2016

@author: munir
"""

from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
#from time import sleep

BASE_URL = 'http://linuxfromscratch.org/blfs/view/systemd/'
pcklist = dict()

def deps_list(deps):
    l = []
    for item in deps:
        for c in item.contents:
            try:
                l.append(c.attrs['title'])
            except AttributeError:
                pass
            except KeyError:
                pass
    return l

html = urlopen(BASE_URL).read()
soup = bs(html,'lxml')
sects = soup.findAll("li",{"class" : "sect1"})

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

    pcklist[k][1] = deps_list(reqs)
    pcklist[k][2] = deps_list(recs)
    pcklist[k][3] = deps_list(opts)
    
    print 'Finished page: ' + soup2.title.string.strip()
    #print 'Sleeping for 5 secs'
    #sleep(5)
