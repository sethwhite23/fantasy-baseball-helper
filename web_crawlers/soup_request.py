import dryscrape
from bs4 import BeautifulSoup
import urllib2

class BaseSoupRequestHandler(object):

    def __init__(self, crawler):
        self.crawler = crawler

    def send(self):
      content = self.send_soup_request() 
      soup = BeautifulSoup(content, "lxml")
      return soup

    def send_soup_request(self):
        raise NotImplementedError

class SoupRequestHandler(BaseSoupRequestHandler):

    def send_soup_request(self):
      req = urllib2.Request(self.crawler.url)
        
      for key, value in self.crawler.headers.iteritems():
           req.add_header(key, value)
      r = urllib2.urlopen(req)
      content = r.read()
      return content


class JSSoupRequestHandler(BaseSoupRequestHandler):

    def send_soup_request(self):
      session = dryscrape.Session()

      for key, value in self.crawler.headers.iteritems():
         session.driver.set_header(key, value)
           
      session.visit(self.crawler.url)
      response = session.body()
      return response
