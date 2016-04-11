from bs4 import BeautifulSoup
import urllib2

class SoupRequest(object):

    @classmethod
    def send(cls, soup_request):
      req = urllib2.Request(soup_request.URL)
      
      for key, value in soup_request.HEADERS.iteritems():
          req.add_header(key, value)

      r = urllib2.urlopen(req)
      content = r.read()
      soup = BeautifulSoup(content, "lxml")
      return soup_request.parse(soup)
