#from web_crawlers.available_starting_pitchers import AvailableStartingPitchersCrawler
#from web_crawlers.daily_notes import DailyNotes
#from web_crawlers.top_available_batters import TopAvailableBattersCrawler
from web_crawlers.roster import RosterCrawler 

#batters = TopAvailableBattersCrawler().crawl()
roster = RosterCrawler().crawl()

for p in roster:
    print p


#for b in batters:
#  print b
