import dateutil.parser as dparser

'''
we can add as many parser as required. On studying different portals
we got to know that there is not a RSS feed available always
and all the websites have structured their websites differently 
'''

def parseRss(soup):
    config = {
        'title': {'element': 'title'},
        'time': {'element': 'div', 'attrs': {'class': '_3Mkg- byline'}},
        'text': {'element': 'div', 'attrs': {'class': '_3WlLe clearfix'}}
    }
    title = soup.find('title').contents[0]  # .split('|')[0]
    time = soup.find(config['time']['element'], attrs=config['time']['attrs']).contents[0]  # .split("| ")[1]
    time = dparser.parse(time, fuzzy=True)
    full_text = soup.find(config['text']['element'], attrs=config['text']['attrs']).contents
    full_text = ' '.join([str(t) for t in full_text])
    author = 'author'
    category = 'category'
    return (title, time, full_text, author, category)


def parseTimeofindia(soup):
    config = {
        'title': {'element': 'title'},
        'time': {'element': 'div', 'attrs':{'class': '_3Mkg- byline'}},
        'text': {'element': 'div', 'attrs': {'class': '_3WlLe clearfix'}},
        'author': {'element': 'a', 'attrs': {'class': 'auth_detail'}},
        'category': {'element': 'div', 'attrs': {'class': 'ArticleHeader_channel'}}
    }
    title = soup.find('title').contents[0]  # .split('|')[0]
    time = soup.find(config['time']['element'], attrs=config['time']['attrs'])
    if not time:
        time = soup.find('span', attrs={'class': 'time_cptn'})
    if time:
        time = dparser.parse(time.text, fuzzy=True)
    full_text = soup.find(config['text']['element'], attrs=config['text']['attrs'])
    if not full_text:
        full_text = soup.find('div', attrs={'class': 'article_content clearfix'})
    full_text = full_text.text

    author = soup.find(config['author']['element'], attrs=config['author']['attrs'])
    author = author.text if author else ''
    category = 'category'
    return (title, time, full_text, author, category)


def parseYahoo(soup):
    config = {
        'title': {'element': 'h1', 'attrs': {'class': 'ArticleHeader_headline'}},
        'time': {'element': 'time'},
        'text': {'element': 'article'},
        'author': {'element': 'div', 'attrs': {'class': 'author-name'}},
        'category': {'element': 'div', 'attrs': {'class': 'ArticleHeader_channel'}}
    }
    title = soup.find('title').text
    time = soup.find('time').attrs['datetime']
    time = dparser.parse(time, fuzzy=True)
    full_text = soup.find(config['text']['element']).text
    author = soup.find(config['author']['element'], attrs=config['author']['attrs']).text
    category = ''
    return (title, time, full_text, author, category)


def parseReuters(soup):
    config = {
        'title': {'element': 'h1', 'attrs': {'class': 'ArticleHeader_headline'}},
        'time': {'element': 'div', 'attrs': {'class': 'ArticleHeader_date'}},
        'text': {'element': 'div', 'attrs': {'class': 'StandardArticleBody_body'}},
        'author': {'element': 'div', 'attrs': {'class': 'BylineBar_byline'}},
        'category': {'element': 'div', 'attrs': {'class': 'ArticleHeader_channel'}}
    }
    title = soup.find('title').text
    time = soup.find(config['time']['element'], attrs=config['time']['attrs']).text
    time = dparser.parse(time, fuzzy=True)
    full_text = soup.find(config['text']['element'], attrs=config['text']['attrs']).text
    author = soup.find(config['author']['element'], attrs=config['author']['attrs']).text
    category = soup.find(config['category']['element'], attrs=config['category']['attrs']).text
    return (title, time, full_text, author, category)

