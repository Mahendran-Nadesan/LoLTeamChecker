# -*- coding: latin-1 -*-

"""The model for LoLTeamChecker

Retrieves, and stores data retrieved by the API and manipulates them
as needed. Called by the controller.
"""
from __future__ import division  # must be first import
from collections import Counter
from lolteamchecker_proxyhelper_clientside import LoLTeamCheckerProxyHelper
from lolteamchecker_rankeddataparser import GrabRankedData
from lolteamchecker_staticdataparser import GrabStaticData


class LoLTeamCheckerModel:
    def __init__(self, region="euw"):
        """Initialise LoLTeamChecker Model.

        Stores data in different dictionaries, and manipulates them as
        necessary, returning them to the controller.
        """
        self.data = {}
        self.team_data = {}
        self.summoners = {}
        self.final_stats = {}
        self.region = region
        self.proxy_instance = LoLTeamCheckerProxyHelper(self.region)
        self.champdata = self.proxy_instance.static_get_champion_list()
        self.staticdata = GrabStaticData(self.champdata)

    def _add_args(self, summoner_name, champ_name):
        """Unused class. Will be used if I decide to make an instance
        of model only take one summoner's data.
        """
        pass

    def _get_summoner_data(self):
        """Get the summoner ranked data from the RiotAPI."""
        print self.summoner_name
        print "stuff is happening..."
        # Is there a better way to do the encoding issue?
        # Only finds ONE summoner's details.
        self.summoners[self.summoner_name] = self.proxy_instance.get_summoner_by_name(
            self.summoner_name.encode('utf-8'))

    def _make_data_relevant(self):
        """Insert docstring."""
        self.data[self.summoner_name].make_relevant(
            self.data[self.summoner_name].get_stats_by_champid(
                self.staticdata.get_champid(self.champ_name)))

    def _get_ranked_data(self):
        """Get ranked data for all summoner's champions."""
        # I don't use all the stats provided, but this is the only
        # reliable way to get individual champion stats for a
        # summoner.
        self.data[self.summoner_name] = {}
        summoner_id = str(
            self.summoners[self.summoner_name]
            [(self.summoner_name.replace(" ", "")).lower()]['id'])
        self.data[self.summoner_name] = GrabRankedData(
            self.proxy_instance.get_ranked_stats_by_summoner_id(summoner_id))

    def _get_champ_stats(self, summoner_name, champ_name):
        """Get champion's stats via various methods."""
        self.error = None
        self.summoner_name = summoner_name
        self.champ_name = champ_name
        print
        print "current name {n}, current champ {c}".format(n=summoner_name,
                                                           c=champ_name)
        print "current final stats are: ", self.final_stats
        print
        if self.summoner_name is "":
            self.error = "No summoner name entered."
            raise self.error
        if self.summoner_name not in self.summoners and (self.summoner_name is not ""):
            try:
                print "trying..._get_summoner_data()"
                self._get_summoner_data()
            except:
                self.error = "No such summoner: {s}".format(s=summoner_name)
                self.summoners.pop(self.summoner_name)
                self.final_stats.pop(summoner_name)
                raise self.error
        if self.summoner_name not in self.data:
            try:
                print "trying..._get_ranked_data()"
                self._get_ranked_data()
            except:
                self.error = "No ranked stats this season."
                self.data.pop(summoner_name)
                raise self.error
        if self.summoner_name in self.data:
            if self.summoner_name not in self.final_stats:
                print "making final_stats[{s}]".format(s=self.summoner_name)
                self.final_stats[self.summoner_name] = {}
            try:
                self.champ_id = [self.staticdata.champs_by_name[i]
                                 for i in self.staticdata.champs_by_name
                                 if i.lower() ==
                                 self.champ_name.lower()] or [
                                     self.staticdata.champ_list[i]['id']
                                     for i in
                                     self.staticdata.champ_list.keys()
                                     if i.lower() ==
                                     self.champ_name.lower()]
                self.champ_id = self.champ_id.pop(0)  # There must be a better
                # way to do this
                self.data[self.summoner_name].make_relevant(
                    self.data[self.summoner_name].get_stats_by_champid(
                        self.champ_id))
                self.data[self.summoner_name].get_averages(
                    self.data[self.summoner_name].relevant_stats)
                self.final_stats[self.summoner_name][self.champ_name] = Counter(
                    self.data[self.summoner_name].convert())
            except:
                print "in exception section of data loop..."
                self.error = "No data for champ"
                self.final_stats[self.summoner_name][self.champ_name] = Counter(
                    {k: 0 for k in self.data[self.summoner_name].converted_stats_names})
                raise self.error
        print "it got to the end...!"

    def _get_summary_stats(self, summoner_names, champ_names):
        """Calculate two types of averages for summoners displayed."""
        self.summoner_names = [name for name in summoner_names]
        self.champ_names = [name for name in champ_names]

        # insert checker here
        self._check_entries()
        self.num_data = [self.final_stats[name][champ]['Games'] for name, champ
                         in self.data_pairs if self.final_stats[name][champ]
                         ['Games'] is not 0]
        self.num_games = sum(self.num_data)
        self.num = len(self.num_data)

        print self.num_data
        print "Number of games is :", self.num_games

        self.ew_data = Counter()
        self.nonew_data = Counter()
        for name, champ in self.data_pairs:
            self.nonew_data += self.final_stats[name][champ]
            self.champ_id = [self.staticdata.champs_by_name[i] for i in
                             self.staticdata.champs_by_name
                             if i.lower() == champ.lower()
                             ] or [self.staticdata.champ_list[i]['id']
                                   for i in self.staticdata.champ_list.keys()
                                   if i.lower() == champ.lower()]
            self.champ_id = self.champ_id.pop(0)
            self.ew_data += Counter(self.data[name].
                                    get_stats_by_champid(self.champ_id))

        self.ave_stats = {'Ave': {key: round((self.nonew_data[key] / self.num),
                                             2) for key in self.nonew_data}}
        self.ave_stats['EWAve'] = self._convert_bad_stats(self.ew_data)
        print "Equally weighted averages: "
        for k, v in self.ave_stats['EWAve'].items():
            print k, ": ", v

        print
        print "Just averages: "
        for k, v in self.ave_stats['Ave'].items():
            print k, ": ", v

    def _convert_bad_stats(self, ew_data):
        """Convert equally weighted averages to my standard dict fields."""
        new_data = {}
        new_data['Gold'] = round((ew_data['totalGoldEarned'] /
                                  self.num_games), 2)
        new_data['Games'] = round((self.num_games/self.num), 2)
        new_data['Kills'] = round((ew_data['totalChampionKills'] /
                                   self.num_games), 2)
        new_data['Assists'] = round((ew_data['totalAssists'] /
                                     self.num_games), 2)
        new_data['Deaths'] = round((ew_data['totalDeathsPerSession'] /
                                    self.num_games), 2)
        new_data['CS'] = round((ew_data['totalMinionKills'] /
                                self.num_games), 2)
        new_data['Win Rate'] = round(((ew_data['totalSessionsWon'] /
                                       self.num_games)*100), 2)
        new_data['Towers'] = round((ew_data['totalTurretsKilled'] /
                                    self.num_games), 2)
        if ew_data['totalDeathsPerSession'] != 0:
            new_data['KDA'] = round(((ew_data['totalChampionKills'] +
                                      ew_data['totalAssists']) /
                                    ew_data['totalDeathsPerSession']), 2)
        else:
            new_data['KDA'] = round(((ew_data['totalChampionKills'] +
                                      ew_data['totalAssists'])/1), 2)
        return new_data

    def _check_entries(self):
        """Check if data for GUI's data pairs exist.

        If the data already exists and is parseable, it will be added to the
        data pairs parsed in _get_summary_stats.
        """
        # Things to check for: 1. Summoner name exists in final_stats 2.
        self.backup_final_stats = self.final_stats
        self.data_pairs = []
        for name, champ in zip(self.summoner_names, self.champ_names):
            if name in self.final_stats:
                if champ in self.final_stats[name]:
                    if self.final_stats[name][champ]['Games'] is not 0:
                        self.data_pairs.append((name, champ))

    def _update(self):
        """Update region."""
        self.proxy_instance = LoLTeamCheckerProxyHelper(self.region)
        # Don't reload static champ list, assume they're the same
        # across regions.
