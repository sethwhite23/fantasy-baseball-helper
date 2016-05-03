from web_crawlers.roster import RosterCrawler 
from player import RankedPlayer, RankedPlayerList
from streamers import Streamers

class Team(object):

    def __init__(self, league_id, team_id):
        self.league_id = league_id
        self.team_id = team_id
        self.roster = self.build_roster()
        self.category_rankings = self.build_category_rankings()
        self.overall_rankings = self.overall_rankings()
        self.streamers = self.build_streamers()

    def build_roster(self):
        return RosterCrawler().crawl()

    def build_category_rankings(self):
        return [RankedPlayerList.build_by_player_attr(self.roster, x, x) for x in ['avg', 'hr', 'runs', 'rbi', 'sb']]

    def overall_rankings(self):
        overall_rankings = {}
        for ranked_list in self.category_rankings:
            for rp in ranked_list.ranked_players:
                if rp.player not in overall_rankings:
                    overall_rankings[rp.player] = 0
                overall_rankings[rp.player] += rp.rank
        
        overall_scored_players = [(x, overall_rankings[x]) for x in overall_rankings]
        
        return RankedPlayerList.build_by_players_and_score(overall_scored_players, 'OVERALL', False)

    def build_streamers(self):
        return Streamers().get_streamers()
