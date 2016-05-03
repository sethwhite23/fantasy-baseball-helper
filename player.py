class Player(object):
    def __init__(self, name):
        self.name = name

class OffensivePlayer(Player):
    def __init__(self, name, pos, avg, hr, runs, rbi, sb, opponent = None):
        #super(Player, self).__init__(name)
        self.name = name
        self.pos = pos
        self.avg = avg
        self.hr = hr
        self.runs = runs
        self.rbi = rbi
        self.sb = sb
        self.opponent = opponent

    def __str__(self):
        s = """*****************************
Name:  {name}
Position: {pos}
AVG: {avg}
HR: {hr}
Runs: {runs} 
RBI: {rbi} 
SB: {sb}
Current Opponent: {current_opponent}""".format(name=self.name, pos = self.pos, avg=self.avg, hr=self.hr, runs = self.runs, rbi=self.rbi, sb = self.sb, current_opponent = self.opponent)

        return s

class PitcherPlayer(Player):
    def __init__(self, name, ip, hits, er, bb, ks, ws, sv, era, whip,  opponent = None):
        #super(Player, self).__init__(name)
        self.name = name
        self.ip = ip
        self.hits = hits
        self.er = er
        self.bb = bb
        self.ks = ks
        self.ws = ws
        self.sv = sv
        self.era = era
        self.whip= whip
        self.opponent = opponent

    def __str__(self):
        s = """*****************************
Name:  {name}
Innings Pitched: {ip}
H: {hits}
ER: {er} 
BB: {bb} 
K: {ks}
W: {ws}
SV: {svs}
ERA: {era}
WHIP: {whip}
Current Opponent: {current_opponent}""".format(name=self.name, ip = self.ip, hits=self.hits, er = self.er, bb = self.bb, ks = self.ks, ws = self.ws, svs = self.sv, era = self.era, whip=self.whip, current_opponent = self.opponent)

        return s

class RankedPlayer(object):

    def __init__(self, player, rank_type, rank, ranked_value):
        self.player = player
        self.rank_type = rank_type
        self.rank = rank
        self.ranked_value = ranked_value

class RankedPlayerList(object):
    def __init__(self, rank_type, ranked_players = []):
        self.ranked_players = ranked_players
        self.rank_type = rank_type
        self.rebuild()

    @classmethod
    # TODO: Combine this with build_by_players_and_score method
    def build_by_player_attr(cls, players, rank_type, rank_attr, higher_is_better=True):
        sorted_players = sorted(players, key=lambda x: float(getattr(x, rank_attr)), reverse=higher_is_better)
        ranked_players = []
        current_rank = 1;
        tied_players = []
        prev_player = None

        for x in range(len(sorted_players)):
            current_player = sorted_players[x]

            if x == 0:
                prev_player = current_player
                tied_players.append(current_player)
                continue

            if getattr(prev_player, rank_attr) == getattr(current_player, rank_attr):
                tied_players.append(current_player)
            else:
                for t in tied_players:
                   ranked_players.append(RankedPlayer(t, rank_type, current_rank, getattr(t, rank_attr)))
                tied_players = [current_player]
                current_rank = x + 1

            prev_player = current_player

        if len(tied_players) > 0:
            for t in tied_players:
                ranked_players.append(RankedPlayer(t, rank_type, current_rank, getattr(t, rank_attr)))
            
        obj = cls(rank_type, ranked_players)

        return obj

    @classmethod
    def build_by_players_and_score(cls, players_and_scores, rank_type, higher_is_better):
        sorted_players = sorted(players_and_scores, key=lambda x: x[1], reverse=higher_is_better)
        ranked_players = []
        current_rank = 1;
        tied_players = []
        prev_player = None


        for x in range(len(sorted_players)):
            current_player = sorted_players[x]

            if x == 0:
                prev_player = current_player
                tied_players.append(current_player)
                continue

            if prev_player[1] == (current_player[1]):
                tied_players.append(current_player)
            else:
                for t in tied_players:
                   ranked_players.append(RankedPlayer(t[0], rank_type, current_rank, t[1]))
                tied_players = [current_player]
                current_rank = x + 1

            prev_player = current_player

        if len(tied_players) > 0:
            for t in tied_players:
                ranked_players.append(RankedPlayer(t[0], rank_type, current_rank, t[1]))

        obj = cls(rank_type, ranked_players)

        return obj

    def rebuild(self):
        self.ranked_players = sorted(self.ranked_players, key=lambda x: float(x.rank), reverse=False)

    def add_ranked_player(self, ranked_player):
        self.ranked_players.append(ranked_player)
        self.rebuild()

    def get_player_in_list(self, player):
        for rp in self.ranked_players:
            if rp.player.name == player.name:
                return rp
        return None

    def __str__(self):
        s = "***************************\n"
        s += "RANKED PLAYERS BY: " + str(self.rank_type) + "\n"
        s += "***************************\n"
        for rp in self.ranked_players:
            s += str(rp.rank) + "  |  " + str(rp.player.name) + "  |  " + str(rp.ranked_value) + "\n"
        return s

