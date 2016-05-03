from web_crawlers.roster import RosterCrawler 
from player import RankedPlayer, RankedPlayerList
from team import Team
import emails
import pprint

my_team = Team(1, 3)

for x in my_team.category_rankings:
    print str(x)


print str(my_team.overall_rankings)

print "STREAMERS"
for p in my_team.streamers:
    print p

emails.send_daily_email(my_team)
