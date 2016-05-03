import fantasy_baseball_settings
from web_crawler import WebCrawler 
from soup_request import SoupRequestHandler

class AvailableStartingPitchersCrawler(WebCrawler):

    def __init__(self):
        self.handler = SoupRequestHandler(self)
        self.url = "http://games.espn.go.com/flb/playertable/prebuilt/freeagency?=undefined&slotCategoryGroup=2&teamId={0}&leagueId={1}&seasonId=2016&gamesInScoringPeriodId=ps&r=43965211".format(fantasy_baseball_settings.team_id, fantasy_baseball_settings.league_id)
        self.headers = {
            'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'COOKIE': 'SWID={{{0}}}; espnAuth={{"swid":"{{{0}}}"}}'.format(fantasy_baseball_settings.espn_swid)
        }

    def parse(self, soup):
      players = soup.find_all('td', class_ = 'playertablePlayerName')
      return [x.find('a').text for x in players]
