import dryscrape
from bs4 import BeautifulSoup
from soup_request import JSSoupRequestHandler

class WebCrawler(object):

    def __init__(self):
        self.handler = None
        self.url = None
        self.headers = None

    def crawl(self):
        soup = self.handler.send()
        return self.parse(soup)

    def parse(self):
        raise NotImplementedError
