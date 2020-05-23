import redis
from helpers import utils

class TaskQueue:
    def __init__(self, name):
        self.name = name
        self.redisQueue = redis.Redis()
        self.redisQueue.delete(self.name)
        self.registry = {}

    def hasItems(self):
        return len(self.redisQueue.lrange(self.name, 0, 2147483648))

    def getItem(self):
        item = self.redisQueue.blpop(self.name)
        if item:
            item = utils.loadPayload(bytes.decode(item[1]))
            return item

    def addTask(self, args):
        self.redisQueue.rpush(self.name, utils.stringifyPayload(args))

    def addBatch(self, links, domain):
        for link in links:
            self.addTask((link, domain))

    def clear(self):
        return self.redisQueue.delete(self.name)

    def exists(self, key):
        return key in self.registry

    def register(self, key, info):
        self.registry[key] = info

    def getSize(self):
        return len(self.redisQueue.lrange(self.name, 0, 2147483648))
