# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 13:24:57 2016

@author: Munir Contractor
"""
helpdoc = """
Usage: python blfs-toolchain.py [OPTIONS] [URL|DOTFILE]

URL     : BLFS book URL for which dependency tree is needed.
          Example URL: 'http://linuxfromscratch.org/blfs/view/stable/'
DOTFILE : Pregenerated dot file with the dependency tree

Possible OPTIONS are:
-h, --help            : Print this help document
-o, --outfile=<file>  : File to save dot output
-i, --imgfile=<file>  : File to save dependency tree image (use proper extension)
                        Image format can be any supported pydotplus format
                        Requires good grpahics capability on system
-d, --dependents=<pck>: Get packages which are dependent on pck
-p, --print           : Print all package names.
                        Use this to get names for <pck> for -d
"""

import sys, os, getopt
try:
    import networkx as nx
except ImportError:
    print 'Package networkx not found. Please install.'
    sys.exit(5)
try:
    import pydotplus as pd
except ImportError:
    print 'Package pydotplus not found. Please install.'
    sys.exit(5)

BASE_URL = 'http://linuxfromscratch.org/blfs/view/systemd/'

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
    
def get_deps(G,pck,prnt=True):
    deps_req = []
    deps_rec = []
    deps_opt = []    
    neighbors = G.neighbors_iter(pck)
    for node in neighbors:
        try:
            col = dict(G.get_edge_data(pck,node)[0])['color']
        except KeyError:
            col = ''
        if col == 'black':
            deps_req.append(node)
        elif col == 'blue':
            deps_rec.append(node)
        elif col == 'yellow':
            deps_opt.append(node)
    if prnt:
        print 'Packages for which ' + pck + ' is required are:\n ' + str(deps_req)[1:-1].replace(',','\n')
        print 'Packages for which ' + pck + ' is recommended are:\n ' + str(deps_rec)[1:-1].replace(',','\n')
        print 'Packages for which ' + pck + ' is optional are:\n ' + str(deps_opt)[1:-1].replace(',','\n')
    #return deps_req, deps_rec, deps_opt
    
def print_graph(G,imgfile,fmt):
    P = nx.nx_pydot.to_pydot(G)
    P.write(imgfile, prog='dot', format=fmt)
    print 'Image saved as ' + imgfile

def save_dot(G,outfile):
    print_full_graph(G,outfile,'raw')
    print 'Dependency tree dot file saved as: ' + outfile
    
def read_graph(infile):
    P = pd.graph_from_dot_file(infile)
    G = nx.nx_pydot.from_pydot(P)
    return G

def build_graph(BASE_URL, rest=1):
    try:
        from bs4 import BeautifulSoup as bs
    except ImportError:
        print 'Package bs4 not found. Please install or read graph from dot file.'
        sys.exit(5)
    try:
        from urllib2 import urlopen
    except ImportError:
        print 'Package urllib2 not found. Please install or read graph from dot file.'
        sys.exit(5)
    from time import sleep
    
    pcklist = dict()
    colors = {1:'black',2:'blue',3:'yellow'}
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
        #print 'Sleeping for ' + str(rest) + ' sec(s).'
        sleep(rest)
    
    G = nx.DiGraph()
    G.add_nodes_from(pcklist.keys())
    
    for key in pcklist.iterkeys():
        for i in range(1,4):
            G.add_edges_from(build_edge_list(key,pcklist[key][i]),color=colors[i])
    
    return G

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:i:d:p", ["help","outfile=","imgfile=","dependents=","print"])
    except getopt.GetoptError as err:
        print str(err)
        print helpdoc
        sys.exit(1)
    if len(opts) < 1:
        print 'At least one option is required'
        print helpdoc
        sys.exit(2)
    outfile = ''
    imgfile = ''
    dep = ''
    printing = False
    for o, a in opts:
        if  o == "-h":
            print helpdoc
            sys.exit(0)
        elif o == "-o":
            outfile = a
            if not(os.access(os.path.dirname(outfile),os.W_OK)) or outfile[0] == '-':
                print 'Cannot write to file or bad file name'
                sys.exit(3)
        elif o == "-i":
            imgfile = a
            if not(os.access(os.path.dirname(imgfile))) or imgfile[0] == '-':
                print 'Cannot write to file or bad file name'
                sys.exit(3)
        elif o == "-d":
            dep = a
        elif o == "-p":
            printing = True
        else:
            print 'Unhandled option'
            sys.exit(9)
    if len(args) != 1:
        print 'Too many or too few arguments'
        print helpdoc
        sys.exit(2)
    for a in args:
        try:
            ind = a.index('http://linuxfromscratch.org/blfs/view/')
        except ValueError:
            ind = -1
        try:
            badind = a.index('http')
        except ValueError:
            badind = -1
        if  ind == 0:
            BASEURL = a
            DOTFILE = ''
        elif badind != -1:
            print 'Bad URL'
            sys.exit(4)
        elif os.access(a,os.R_OK):
            DOTFILE = a
            BASEURL = ''
        else:
            print 'Unhandled argument'
            sys.exit(9)
    if BASEURL == '' and len(DOTFILE) > 0:
        print 'Reading data from ' + DOTFILE
        G = read_graph(DOTFILE)
    elif DOTFILE == '' and len(BASEURL) > 0:
        print 'Building data from ' + BASEURL
        G = build_graph(BASEURL)
    if printing:
        print 'Full list of packages: \n ' + str(G.nodes())[1:-1].replace(',','\n')
    if dep != '':
        get_deps(G,dep)
    if outfile != '':
        save_dot(G,outfile)
    if imgfile != '':
        fmt = os.path.splitext(imgfile)[1][1:]
        if fmt == '': fmt = png
        print 'Creating image in ' + fmt + ' format...this will take a while'
        print_graph(G, fmt)
    sys.exit(0)
