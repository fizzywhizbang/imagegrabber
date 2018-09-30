#!/usr/bin/env python3
import requests
try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
from time import sleep
import sys
import re, os
from datetime import datetime
from six.moves.urllib.parse import urljoin, urlsplit, SplitResult


ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

class colorize:
    WARNING="\033[1;0;31m"
    NORMAL="\033[0;0;0m"
    GREEN="\033[1;0;32m"

def imagegrabber(url, fname, dir):

    print("image grab url=%s" % url)
    proxy = getProxy()
    header = {'User-Agent': str(ua.random)}
    data = requests.get(url, headers=header, proxies=proxy)
    if os.path.isfile(fname):
        fname = str(datetime.now()) + fname
        fname = fname.replace(":","")
    if dir == ".":
        open(fname, 'wb').write(data.content)
    else:
        open(dir + "/" + fname, 'wb').write(data.content)



    return "complete"


# Main function
def getProxy():
    # Retrieve latest proxies
    try:
        url = 'https://www.sslproxies.org/'
        header = {'User-Agent': str(ua.random)}
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        proxies_table = soup.find(id='proxylisttable')

        # Save proxies in the array
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
                'ip':   row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string
            })

        # Choose a random proxy
        proxy = random.choice(proxies)
        return proxy
    except:
        #slow down proxy requests
        sleep(2)
        getProxy()


def scanurl(url):
    header = {'User-Agent': str(ua.random)}
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    for link in soup.find_all('a', href=True):
        if link['href'].endswith(fileList):
            fname = getName(link['href'])
            imagegrabber(link['href'], fname, dir)
    return "complete"

def getName(url):
    fields = urlsplit(url)._asdict()  # convert to absolute URLs and split
    fields['path'] = re.sub(r'/$', '', fields['path'])  # remove trailing /
    fname = fields['path'].split("/")
    # figure out which is the last
    last = len(fname) - 1
    return fname[last]

def getDir(url):
    fields = urlsplit(url)._asdict()  # convert to absolute URLs and split
    fields['path'] = re.sub(r'/$', '', fields['path'])  # remove trailing /
    fname = fields['path'].split("/")
    # figure out which is the last
    last = len(fname) - 1
    return fname[last]


def run():
    if len(sys.argv) == 1:
        url = input("Please Enter URL or type quit to quit: ")
        if len(url) < 1:
            url = input("Please Enter URL or type quit to quit: ")
            if url == "quit":
                exit()
        else:
            if url == "quit":
                exit()
            dir = input("Please enter dir or enter to automatically create one: ")

        if len(dir) == 0:
            dir = getDir(url)
            if not os.path.exists(dir):
                os.mkdir(dir)
            else:
                if not os.path.exists(dir):
                    os.mkdir(dir)
    else:
        url = sys.argv[1]

        if len(sys.argv) == 3:
            dir = sys.argv[2]
            if not os.path.exists(dir):
                os.mkdir(dir)
        else:
            dir = getDir(url)
            if not os.path.exists(dir):
                os.mkdir(dir)
    print("Scan complete")
    print("------------------------------------")
    return "complete"

fileList = ('jpg','JPG','jpeg','JPEG','mp4','m4v','mov','wmv')

returnval = run()

while returnval:
    run()
