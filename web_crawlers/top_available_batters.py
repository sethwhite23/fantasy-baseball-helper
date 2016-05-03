import dryscrape
from bs4 import BeautifulSoup
import fantasy_baseball_settings
from player import OffensivePlayer
from web_crawler import WebCrawler 
from soup_request import JSSoupRequestHandler
import re
import pprint

class TopAvailableBattersCrawler(WebCrawler):

    def __init__(self):
        self.handler = JSSoupRequestHandler(self)
        self.url = "http://games.espn.go.com/flb/playertable/prebuilt/freeagency?leagueId={0}&teamId={1}&seasonId=2016&view=stats&context=freeagency&avail=1&r=20298621".format(fantasy_baseball_settings.league_id, fantasy_baseball_settings.team_id)
        self.headers = {
            'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'COOKIE': 'SWID={{{0}}}; espnAuth={{"swid":"{{{0}}}"}}'.format(fantasy_baseball_settings.espn_swid)
        }

    @classmethod
    def player_search(cls, tag):
       return re.compile("pncPlayerRow").search(str(tag)) and not re.compile("emptyRow").search(str(tag))

    @classmethod
    def parse(cls, soup):

        player_table =  soup.find('table', class_ = 'playerTableTable')
        #player_rows = player_table.find_all(cls.player_search)
        player_rows = player_table.find_all('tr', class_ = 'pncPlayerRow')
        players = []
        
        for p_row in player_rows:
            index = 1
            name = None
            position = None
            opponent = None
            runs = None
            hr = None
            rbi = None
            sb = None
            avg = None
        
            for col in p_row.find_all('td'):
                if index == 1:
                    name_link = col.find('a')
                    name = name_link.text
                    print "Next Sibing"
                    x = name_link.nextSibling
                    x = x.split(', ', 1)[1]
                    x = x.split(' ')
                    team = x[0]
                    print x
                    position = x[1:-1]
                    print x
                elif index == 10:
                    runs = col.text
                elif index == 11:
                    hr = col.text
                elif index == 12:
                    rbi = col.text
                elif index == 13:
                    sb = col.text
                elif index == 14:
                    avg = col.text
                index += 1
        
            player = OffensivePlayer(name, position, avg, hr, runs, rbi, sb)
            players.append(player)
        return players
