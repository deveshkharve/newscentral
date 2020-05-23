# NewsCentral
A crawler application that will take the domain of the news websites
and then keep crawling all the links in a BFS approach.

#### Prequisites

- [Python3](https://www.python.org/downloads/)
- need a to setup and start [redis-server](https://redis.io/topics/quickstart).


#### Installation
Run the following command in the project directory

```pip3 install -r requirements.txt```

#### Run
once above two checks are in place. Start the application with the following commaind
```python3 server.py ```
and open the application in the web brower at
```http://127.0.0.1:8080/```

#### application structure

```crawler.py``` The Crawler is the main service which is being executed.
It takes a list of domains to work on. And creates one master thread for each
of these domains.

```TaskQueue.py```The master thread is provided with a separate scrapping task and writing task queue from the class.
Each master in turn spawns multiple thread to for scrapping and writing data to the file. 

```workers.py``` The workers uses the crawlingUtils to parse and write the file.

```crawlerutils.py``` utilities to work with scrapping and dumping the data into .json file.

```newspaper3k``` newspaper package to parse the articles

``redis`` to handle the queue.  

