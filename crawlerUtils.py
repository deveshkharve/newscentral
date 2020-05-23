import requests
from bs4 import BeautifulSoup
from helpers.utils import getAllLinks, jsonStringify
from parser import parseYahoo, parseTimeofindia, parseReuters
import logging
logging.basicConfig(level=logging.DEBUG)


def scrapeArticle(url, domain, scrapeQueue):
    """
    scrape the url and check if article is found, else add all the links from the similar domain
    :param url: url paring
    :param domain: valid domain url
    :param scrapeQueue: scrapping task queue
    :return:
    """
    try:
        r = requests.get(url)
        source = BeautifulSoup(r.text, 'html.parser')
        # get all the links
        linksAll = getAllLinks(source, domain)

        if linksAll:
            scrapeQueue.addBatch(linksAll, domain)

        dir = ''
        if 'timesofindia' in domain:
            if '.cms' in url:
                dir = 'toi'
                title, time, story, author, category = parseTimeofindia(source)
        elif 'reuters' in domain:
            dir = 'reuters'
            title, time, story, author, category = parseReuters(source)
        elif 'yahoo' in domain:
            dir = 'yahoo'
            title, time, story, author, category = parseYahoo(source)

        return {
            'title': title.strip(), 'time': str(time),
            'url': url.strip(), 'story': story.strip(),
            'author': author, 'category': category, 'dir': dir}
    except Exception as e:
        print('unable to parse', url, e)
        pass


def createRecord(fileName, data):
    try:
        global counter, linkLimit, registry
        textfile = open('./CRAWLED_DATA/' + fileName, 'w')
        textfile.write(jsonStringify(data))
        textfile.close()
    except Exception as e:
        print(e)


