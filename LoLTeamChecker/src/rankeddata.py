# Ranked stats data sorter/parser

from __future__ import division # must be first import

class GrabRankedData:
    """Converts and returns json/dict data requested from the Riot API
    of the type: ranked stats of summoner."""
    def __init__(self, ranked_stats):
        """Stores and manipulates ranked stats data for a single
        summoner. Takes its data returned by
        api.get_ranked_stats_by_summoner_id(...)."""
        self.all = ranked_stats['champions']
        self.relevant_stat_names = ['totalSessionsPlayed',
                                    'totalAssists',
                                    'totalDeathsPerSession',
                                    'totalSessionsWon',
                                    'totalSessionsLost',
                                    'totalGoldEarned',
                                    'totalChampionKills',
                                    'totalMinionKills',
                                    'totalAssists',
                                    'totalTurretsKilled']
        self.converted_stats_names = ['Games', 'Win Rate', 'Kills',
                                      'Deaths',
                                      'Assists', 'CS',
                                      'Towers', 'Gold',
                                      'KDA']
        self._sort_by_champid()

    def _sort_by_champid(self):
        """Sorts self.all into a dict with champid as the main key
        (dict['champname']) as opposed to lists."""
        self.all_stats_by_champid = {}
        for i in self.all:
            # note: 'id' is an int, so call it appropriately: as in,
            # stats_by_champname[22], not stats_by_champname['22'].
            self.all_stats_by_champid[i['id']] = i['stats']
##            return

    def get_averages(self, champ_stats):
        """Calculates and returns the average (per game) values for
        one champion only, in whatever dict of stats:
        all_stats_by_id[champid]/relevant_stats. Make sure they are in
        the right format."""
        # The following is weird. I remove num_games from the champ's
        # stats, loop over the remaining stats and divide by
        # num_games, then add it back to the dict because it might be
        # used.
        num_games = champ_stats.pop('totalSessionsPlayed')
        self.champ_stats = champ_stats
        self.ave_stats = {}
        for stat in champ_stats:
            self.ave_stats[stat] = round(champ_stats[stat]/num_games, 2)
        self.champ_stats['totalSessionsPlayed'] = num_games
        self.ave_stats['totalSessionsPlayed'] = num_games
        return self.ave_stats

    def get_stats_by_champid(self, champid):
        """Gets ranked stats by champid."""
        champid = int(champid)
        return self.all_stats_by_champid[champid]

    def make_relevant(self, champ_all_stats):
        """Takes only the relevant stats for *one champ* necessary for
        LoLTeamCheck, i.e. all_stats_by_id[champid]."""
        self.relevant_stats = {}
        for name in self.relevant_stat_names:
            if champ_all_stats.has_key(name):
                self.relevant_stats[name] = champ_all_stats[name]

    def convert(self):
        """Convert to final form."""
        # Sort this mess: 1. Any way to automate this? 2. Turns out
        # %win is rounded too early (i.e. in self.get_averages) 3.
        # Right now using shortened keys, for the sake of
        # LoLTeamChecker. Just a hack, needs to be changed. The
        # problem temporarily solved is that final_stats was assigned
        # this whole dict, the keys of which are checked against
        # header values, which were shorted for the GUI. Don't forget
        # to also change self.converted_stats_names
        self.converted_stats = {}
        self.converted_stats["Games"] = self.ave_stats['totalSessionsPlayed']
        self.converted_stats["Win Rate"] = round(((self.champ_stats['totalSessionsWon']/self.champ_stats['totalSessionsPlayed'])*100), 2)
        self.converted_stats["Kills"] = self.ave_stats['totalChampionKills']
        self.converted_stats["Deaths"] = self.ave_stats['totalDeathsPerSession']
        self.converted_stats["Assists"] = self.ave_stats['totalAssists']
        self.converted_stats["CS"] = self.ave_stats['totalMinionKills']
        self.converted_stats["Towers"] = self.ave_stats['totalTurretsKilled']
        self.converted_stats["Gold"] = self.ave_stats['totalGoldEarned']
        if self.ave_stats['totalDeathsPerSession'] != 0:
            self.converted_stats["KDA"] = round((self.ave_stats['totalChampionKills'] + self.ave_stats['totalAssists'])/self.ave_stats['totalDeathsPerSession'], 2)
        else:
            self.converted_stats["KDA"] = round((self.ave_stats['totalChampionKills'] + self.ave_stats['totalAssists'])/1, 2)
        return self.converted_stats
        
##        self.converted_stats["Total Games"] = self.ave_stats['totalSessionsPlayed']
##        self.converted_stats["Win Rate"] = round(((self.champ_stats['totalSessionsWon']/self.champ_stats['totalSessionsPlayed'])*100), 2)
##        self.converted_stats["Ave Kills"] = self.ave_stats['totalChampionKills']
##        self.converted_stats["Ave Deaths"] = self.ave_stats['totalDeathsPerSession']
##        self.converted_stats["Ave Assists"] = self.ave_stats['totalAssists']
##        self.converted_stats["Ave CS"] = self.ave_stats['totalMinionKills']
##        self.converted_stats["Ave Towers"] = self.ave_stats['totalTurretsKilled']
##        self.converted_stats["Ave Gold"] = self.ave_stats['totalGoldEarned']
##        self.converted_stats["KDA"] = round((self.ave_stats['totalChampionKills'] + self.ave_stats['totalAssists'])/self.ave_stats['totalDeathsPerSession'], 2)
