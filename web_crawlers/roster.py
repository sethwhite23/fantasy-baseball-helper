import dryscrape
from bs4 import BeautifulSoup
import fantasy_baseball_settings
from player import OffensivePlayer
from player import PitcherPlayer
from web_crawler import WebCrawler 
from soup_request import JSSoupRequestHandler
import re
import pprint

class RosterCrawler(WebCrawler):

    def __init__(self):
        self.handler = JSSoupRequestHandler(self)
        self.url = "http://games.espn.go.com/flb/playertable/prebuilt/manageroster?leagueId={0}&teamId={1}&seasonId=2016&scoringPeriodId=18&view=stats&context=clubhouse&version=currSeason&ajaxPath=playertable/prebuilt/manageroster&managingIr=false&droppingPlayers=false&asLM=false&r=21581975".format(fantasy_baseball_settings.league_id, fantasy_baseball_settings.team_id)
        self.headers = {
            'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'COOKIE': 'SWID={{{0}}}; espnAuth={{"swid":"{{{0}}}"}}'.format(fantasy_baseball_settings.espn_swid)
        }

    def player_search(self, tag):
       return re.compile("pncPlayerRow").search(str(tag)) and not re.compile("emptyRow").search(str(tag))

    def parse_batters_table(self, player_table_soup):
        player_rows = player_table_soup.find_all(self.player_search)
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
                    position = col.text
                elif index == 2:
                    name = col.find('a').text
                elif index == 4:
                   if col.find('a') is not None:
                       opponent = col.find('a').text
                elif index == 8:
                    runs = col.text
                elif index == 9:
                    hr = col.text
                elif index == 10:
                    rbi = col.text
                elif index == 11:
                    sb = col.text
                elif index == 12:
                    avg = col.text
                index += 1
        
            player = OffensivePlayer(name, position, avg, hr, runs, rbi, sb, opponent)
            players.append(player)
        return players

    def parse_pitchers_table(self, player_table_soup):
        print "IN PARSE PITCHER TABLE"
        player_rows = player_table_soup.find_all(self.player_search)
        players = []
        
        for p_row in player_rows:
            index = 1
            name = None
            ip = None
            hits = None
            er = None
            bb = None
            ks = None
            ws = None
            saves = None
            era = None
            whip = None
        
            for col in p_row.find_all('td'):
                if index == 1:
                    position = col.text
                elif index == 2:
                    name = col.find('a').text
                elif index == 4:
                   if col.find('a') is not None:
                       opponent = col.find('a').text
                elif index == 7:
                    ip = col.text
                elif index == 8:
                    hits = col.text
                elif index == 9:
                    er = col.text
                elif index == 10:
                    bb = col.text
                elif index == 11:
                    ks = col.text
                elif index == 12:
                    ws = col.text
                elif index == 13:
                    saves = col.text
                elif index == 14:
                     era = col.text
                elif index == 15:
                     whip = col.text

                index += 1
        
            player = PitcherPlayer(name, ip, hits, er, bb, ks, ws, saves, era, whip)
            players.append(player)
        return players
      
    def parse(self, soup):
        players = []
        player_tables =  soup.find_all('table', class_ = 'playerTableTable')
        index = 1
        for pt in player_tables:
            if index == 1:
                players = players + self.parse_batters_table(pt)
            #else:
            #    players = players + self.parse_pitchers_table(pt)
            index += 1

        return players

