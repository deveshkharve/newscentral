import threading
from helpers import utils
from taskQueue import TaskQueue
from workers import writer, crawl, stopAll

registry = {}
linkLimit = 500
counter = 0
linkQueue = []


class Crawler:
    """
    Crawler class, using threading to execute multiple domains in parallel.
    """
    def __init__(self):
        try:
            self.links = []
            self.threads = []
            self.state = 'idle'
            self.queues = {}
        except Exception as e:
            print(e)
            raise e

    def getStatus(self):
        """
        get status of the queues for the tasks
        :return:
        """
        keys = self.queues.keys()
        stat = {}
        for k in self.queues:
            stat[k] = self.queues[k]['crawl'].getSize()

        return {'state': self.state, 'keys': list(keys), 'queue': stat}

    def stop(self):
        """
        stop the execution of all the threads
        :return:
        """
        stopAll()
        for thread in self.threads:
            thread.join()
        self.state = 'stopped'

    def start(self, links):
        # a process utility
        def processRequest(domain, scrapeQueue, writeQueue, concurrency=2):
            """

            Process each target domain is handled by a separate thread and has their own task queue to work on consumed
            by the sub worker threads.

            :param domain: target domain to start with
            :param scrapeQueue: TaskQueue for scrapping workers
            :param writeQueue: TaskQueue to be used by the writer workers
            :param concurrency: Number of workers to spawn. Writer workers will be half of the Scrapping workers. As
            more scrapping is needed to get relevant data as compared to writing
            :return:
            """

            # add the first task in the scrapping queue and start all the threads/workers
            scrapeQueue.addTask([domain, domain])
            crawlerThreads = []
            writerThreads = []

            for i in range(concurrency):
                # start crwaling worker
                myThread = threading.Thread(target=crawl, args=(scrapeQueue, writeQueue))
                crawlerThreads.append(myThread)
                myThread.start()

            for i in range(int(1 + concurrency / 2)):
                # start writing worker
                myThread = threading.Thread(target=writer, args=(writeQueue,))
                writerThreads.append(myThread)
                myThread.start()

        self.links = links
        if self.state != 'running':
            self.state = 'running'

            # process all the domains provided
            while len(self.links):
                domain = self.links.pop(0)

                # a seperate queue for all the domains, single queue will not give change to other domains
                self.queues[domain] = {
                    'crawl': TaskQueue(domain+'crawl'),
                    'write': TaskQueue(domain+'write')
                }

                t = threading.Thread(target=processRequest,
                                     args=(domain, self.queues[domain]['crawl'], self.queues[domain]['write'], 1))
                t.setDaemon(True)
                self.threads.append(t)
                t.start()
        else:
            print(self.threads)
            raise Exception('Already running')

# def start():
#     crawl = Crawler()
#     crawl.start(newsLinks)
#
#
# main = threading.Thread(target=start)
# main.setDaemon(True)
# main.start()
