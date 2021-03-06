from web_crawlers.available_starting_pitchers import AvailableStartingPitchersCrawler
from web_crawlers.daily_notes import DailyNotesCrawler


from enum import Enum
import emails
import pprint

class StreamerRankings(Enum):
  RANK_1 = "EA8487" # > 55
  RANK_2 = "FDB8BA" # 51 - 54
  RANK_3 = "ADDCAB" # 48 - 50
  RANK_4 = "A1DA9E" # 45 - 47
  RANK_5 = "70BF6C" # < 45

  @classmethod
  def get_rank(cls, gd):
      gd = int(gd)
      if gd > 55:
          return cls.RANK_5
      elif gd >= 50 and gd <= 54:
          return cls.RANK_4
      elif gd >= 48 and gd <= 50:
          return cls.RANK_3
      elif gd >= 45 and gd <= 47:
          return cls.RANK_2
      else:
          return cls.RANK_1

daily_notes = DailyNotesCrawler().crawl()
available_starting_pitchers = AvailableStartingPitchersCrawler().crawl()

#print "Daily Notes"
#pprint.pprint(daily_notes)

#print "AVAILABLE STARTERS"
#pprint.pprint(available_starting_pitchers)

streamers = []
for p in daily_notes:
    try: 
        if int(p['GD']) >= 0:
           for a_p in available_starting_pitchers:
               if p['Name'] == a_p:
                   s = p
                   s['rank'] = StreamerRankings.get_rank(s['GD'])
                   streamers.append(s)
    except:
        # For some reason there is a 'N/A' rank
        pass

for p in streamers:
    print p

#emails.send_daily_email(streamers)
