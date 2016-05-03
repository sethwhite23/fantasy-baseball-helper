import fantasy_baseball_settings
from web_crawler import WebCrawler 
from soup_request import SoupRequestHandler
from datetime import datetime, timedelta

class DailyNotesCrawler(WebCrawler):

    def __init__(self):
        self.handler = SoupRequestHandler(self)
        est = datetime.now()+timedelta(hours=4)
        yymmdd = est.strftime("%y%m%d")
        month_and_day = est.strftime("%b-%d")

        self.url = "http://espn.go.com/fantasy/baseball/story/_/page/dailynotes{0}/fantasy-baseball-daily-notes-{1}-mlb-matchups".format(yymmdd, month_and_day)

        self.headers = {
          'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        }
    
    def parse(self, soup):
        aside = soup.find('aside')
        pitcher_table = aside.find('tbody')
        pitchers = pitcher_table.find_all('tr')

        ret_pitchers = []

        for p_row in pitchers:
            index = 1
            pitcher = {}
            for col in p_row.find_all('td'):
                if index == 1:
                    pitcher['GD'] = col.find('b').text
                elif index == 3:
                    pitcher['Name'] = col.text
                elif index == 5:
                    pitcher['Opponent'] = col.find('b').text
                elif index == 6:
                    pitcher['W-L'] = col.text
                elif index == 7:
                    pitcher['ERA'] = col.text
                elif index == 8:
                    pitcher['WHIP'] = col.text

                index += 1
            ret_pitchers.append(pitcher)
        return ret_pitchers
