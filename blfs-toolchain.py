# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 13:24:57 2016

@author: munir
"""

import networkx as nx
import pydotplus as pd
import matplotlib.pyplot as plt
import matplotlib.image as mim
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
from cStringIO import StringIO
from time import sleep

BASE_URL = 'http://linuxfromscratch.org/blfs/view/systemd/'
pcklist = dict()
colors = {1:'black',2:'blue',3:'yellow'}

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

def build_edge_list(node, neighbor_list):
    e = []
    if len(neighbor_list) <> 0:
        for n in neighbor_list:
            e.append((n,node))
    return e

html = urlopen(BASE_URL).read()
soup = bs(html,'lxml')
sects = soup.findAll("li",{"class" : "sect1"})

for item in sects:
    try:
        if pcklist.has_key(item.contents[1].string):
            print item.contents[1].string + ' already exists.'
            l = lambda x: x if x.strip() <> '' else 'N'
            ovw = l(raw_input('Do you wish to overwrite the URL? (y/N): '))
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
    #print 'Sleeping for 2 secs'
    sleep(1)

G = nx.DiGraph()
G.add_nodes_from(pcklist.keys())

for key in pcklist.iterkeys():
    for i in range(1,4):
        G.add_edges_from(build_edge_list(key,pcklist[key][i]),color=colors[i])

P = nx.nx_pydot.to_pydot(G)
P.write_png('/home/munir/lfs-sources/tree.png')

png_str = P.create_png(prog='dot')
sio = StringIO()
sio.write(png_str)
sio.seek(0)
img = mim.imread(sio)

imgplot = plt.imshow(img)
plt.show(block=False)
