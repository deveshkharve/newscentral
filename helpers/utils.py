import os
import urllib
import time
import logging
import pickle
import json
logging.basicConfig(level=logging.DEBUG)

def checkIsValidLink(link, domain):

    if not link or link[0] == '#':
        return False

    if not urllib.parse.urlparse(link).hostname:
        link = urllib.parse.urljoin(domain, link)

    if 'video' in link:
        return False

    return urllib.parse.urlparse(link).hostname == urllib.parse.urlparse(domain).hostname

def getAllLinks(soup, domain):
    links = soup.find_all('a')
    linkQueue = []
    for link in links:
        if 'href' in link.attrs and checkIsValidLink(link.attrs['href'], domain):
            link = link.attrs['href']
            if not urllib.parse.urlparse(link).hostname:
                link = urllib.parse.urljoin(domain, link)
            linkQueue.append(link)

    # linkQueue = [l.attrs['href'] for l in links if 'href' in l.attrs and link = checkIsValidLink(l.attrs['href'], domain)]
    return set(linkQueue)

def pathmaker(name):
    path = "./CRAWLED_DATA/{}".format(name)
    try:
        os.makedirs(path)
    except OSError:
        pass
    else:
        pass


def sleep(sec):
    time.sleep(sec)


def stringifyPayload(items: list) -> str:
    items = json.dumps(items)
    return items


def loadPayload(data):
    items = json.loads(data)
    return items


def jsonStringify(data):
    return json.dumps(data)

