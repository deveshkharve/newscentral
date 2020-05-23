from crawlerUtils import scrapeArticle, createRecord
from helpers import utils

STOP = False

def reset():
    global STOP
    STOP = False


def stopAll():
    global STOP
    STOP = True

def writer(writeQueue):
    """
    write the data in a json file, reads from the writing task queues and performs the task
    :param writeQueue: writing task queue
    :return:
    """
    global STOP
    reset()
    while True and not STOP:
        while writeQueue.hasItems() and not STOP:
            req = writeQueue.getItem()
            if not req:
                continue

            if writeQueue.exists(req[0]):
                continue

            utils.logging.debug('writing file: '+req[0])
            createRecord(*req)
            writeQueue.register(req[0], req[1])

        utils.logging.debug('queue empty')
        utils.sleep(5)


def crawl(scrapeQueue, writeQueue):
    """

    :param scrapeQueue: queue for scrapping task
    :param writeQueue: queue for writing task
    :return:
    """
    global STOP
    reset()
    while True and not STOP:
        while scrapeQueue.hasItems and not STOP:
            # get item
            req = scrapeQueue.getItem()
            if not req:
                continue

            # check if task has already been registered before, else register
            if scrapeQueue.exists(req[0]):
                continue

            scrapeQueue.register(req[0], {})
            # scrape the article
            scrapped = scrapeArticle(*req, scrapeQueue)

            if scrapped:
                # relevant data found then put a task in wirting queue
                fileName = '{}_{}.json'.format(scrapped['dir'], scrapped['title'].replace('/', '-'))
                writeQueue.addTask([fileName, scrapped])

        utils.logging.debug('queue empty')
        utils.sleep(5)

