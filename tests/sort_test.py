from web_crawlers.roster import RosterCrawler 
from player import RankedPlayer, RankedPlayerList
import pprint

roster = RosterCrawler().crawl()

def print_players(players):
    for p in players:
        print p

ranked_lists = [RankedPlayerList.build_by_player_attr(roster, x, x) for x in ['avg', 'hr', 'runs', 'rbi', 'sb']]

for x in ranked_lists:
    print str(x)

# Build Overall Rankings
overall_rankings = {}
for ranked_list in ranked_lists:
    for rp in ranked_list.ranked_players:
        if rp.player not in overall_rankings:
            overall_rankings[rp.player] = 0
        overall_rankings[rp.player] += rp.rank

overall_scored_players = [(x, overall_rankings[x]) for x in overall_rankings]

overall_ranked_list = RankedPlayerList.build_by_players_and_score(overall_scored_players, 'OVERALL', False)

print str(overall_ranked_list)
