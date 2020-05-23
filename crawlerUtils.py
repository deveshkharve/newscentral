import requests
from bs4 import BeautifulSoup
from helpers.utils import getAllLinks, jsonStringify, getUrlDomain
import logging
logging.basicConfig(level=logging.DEBUG)
from newspaper import Article

def scrapeArticle(url, domain, scrapeQueue):
    """
    scrape the url and check if article is found, else add all the links from the similar domain
    :param url: url paring
    :param domain: valid domain url
    :param scrapeQueue: scrapping task queue
    :return:
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        # r = requests.get(url)
        source = BeautifulSoup(article.html, 'html.parser')
        # get all the links
        linksAll = getAllLinks(source, domain)

        if linksAll:
            scrapeQueue.addBatch(linksAll, domain)

        # if 'timesofindia' in domain:
        #     if '.cms' in url:
        #         dir = 'toi'
        #         title, time, story, author, category = parseTimeofindia(source)
        # elif 'reuters' in domain:
        #     dir = 'reuters'
        #     title, time, story, author, category = parseReuters(source)
        # elif 'yahoo' in domain:
        #     dir = 'yahoo'
        #     title, time, story, author, category = parseYahoo(source)
        if article.title and article.text:
            return {
                'title': article.title, 'time': str(article.publish_date),
                'url': article.url, 'story': article.text,
                'author': ','.join(article.authors), 'category': str(article.tags), 'dir': getUrlDomain(article.source_url),
                'source_url': article.source_url
            }
    except Exception as e:
        print('unable to parse', url, e)
        pass


def createRecord(fileName, data):
    try:
        textfile = open('./CRAWLED_DATA/' + fileName, 'w')
        textfile.write(jsonStringify(data))
        textfile.close()
    except Exception as e:
        print(e)


# scrapeArticle('https://in.finance.yahoo.com/news/reliance-jiomart-officially-rolls-across-093117746.html', 'yahoo', '')