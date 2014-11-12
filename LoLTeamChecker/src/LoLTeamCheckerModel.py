# -*- coding: latin-1 -*-

"""The model for LoLTeamChecker

Retrieves, and stores data retrieved by the API and manipulates them
as needed. Called by the controller."""
from __future__ import division # must be first import
##from LoLTeamCheckerController import LoLTeamCheckerController
#from riotapi_py import *
from lolteamchecker_proxyhelper_clientside import *
from rankeddata import GrabRankedData
from staticdata import GrabStaticData
from collections import Counter



class LoLTeamCheckerModel:
    def __init__(self, region="euw"):
        self.data = {}
        self.team_data = {}
        self.summoners = {}
        self.final_stats = {}
        #self.api_key = "e20154f8-3601-40ac-ae35-5af13e62cc8c" 
        self.region = region
        #self.versions = {"gsbn": "v1.4", "gsbid": "v1.4", "ggbid":
        #                 "v1.3", "grsbid": "v1.3", "sgcbid": "v1.2",
        #                 "gmhbid": "v2.2"} 
        #self.api_instance = RiotApiPy(self.api_key, self.versions,
        #                              self.region)
        self.proxy_instance = LoLTeamCheckerProxyHelper(self.region)
        self.champdata = self.proxy_instance.static_get_champion_list()
        self.staticdata = GrabStaticData(self.champdata)

    def _add_args(self, summoner_name, champ_name):
        """Unused class. Will be used if I decide to make an instance
        of model only take one summoner's data"""
        pass

    def _get_summoner_data(self):
        """Get the summoner ranked data from the RiotAPI."""
        
        print self.summoner_name
        print "stuff is happening..."
        # Is there a better way to do the encoding issue?
        #self.summoners[self.summoner_name] = self.proxy_instance.get_summoners_by_name(self.summoner_name.encode('utf-8'), self.region)
        self.summoners[self.summoner_name] = self.proxy_instance.get_summoner_by_name(self.summoner_name.encode('utf-8'))

    def _make_data_relevant(self):
        self.data[self.summoner_name].make_relevant(self.data[self.summoner_name].get_stats_by_champid(self.staticdata.get_champid(self.champ_name)))
        
    def _get_ranked_data(self):
        """Method for getting all ranked data for a summoner, which
        will be used to get requested champion's data."""
        # I don't use all the stats provided, but this is the only
        # reliable way to get individual champion stats for a
        # summoner.
        self.data[self.summoner_name] = {}
##        self.final_stats[self.summoner_name]= Counter({})
        summoner_id = str(self.summoners[self.summoner_name][(self.summoner_name.replace(" ", "")).lower()]['id'])
        self.data[self.summoner_name] = GrabRankedData(self.proxy_instance.get_ranked_stats_by_summoner_id(summoner_id))

    def _get_champ_stats(self, summoner_name, champ_name):
        """Method for getting all relevant stats for summoner/champ
        combination."""
        self.error = None
        self.summoner_name = summoner_name
        self.champ_name = champ_name
##        self.final_stats[summoner_name]= {}
        print
        print "current name {n}, current champ {c}".format(n=summoner_name, c=champ_name)
        print "current final stats are: ", self.final_stats
        print
##        if do_all is True and self.summoner_name is None:
        if self.summoner_name is "":
            self.error = "No summoner name entered."
            raise self.error
        if self.summoner_name not in self.summoners and self.summoner_name is not "":
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
            if not self.final_stats.has_key(self.summoner_name):
                print "making final_stats[{s}]".format(s=self.summoner_name)
                self.final_stats[self.summoner_name] = {}
            try:
                self.champ_id = [self.staticdata.champs_by_name[i] for i in self.staticdata.champs_by_name if i.lower() == self.champ_name.lower()] or [self.staticdata.champ_list[i]['id'] for i in self.staticdata.champ_list.keys() if i.lower() == self.champ_name.lower()]
                self.champ_id = self.champ_id.pop(0)    # There must be a better way to do this
##                    self.champ_id = [myapp.model.staticdata.champs_by_name[i] for i in myapp.model.staticdata.champs_by_name if i.lower() == self.champ_name.lower()]
##                
##                    self.champ_id = [myapp.model.staticdata.champ_list[i]['id'] for i in myapp.model.staticdata.champ_list.keys() if i.lower() == self.champ_name.lower()]
##                self.data[self.summoner_name].make_relevant(self.data[self.summoner_name].get_stats_by_champid(self.staticdata.get_champid(self.champ_name)))
                self.data[self.summoner_name].make_relevant(self.data[self.summoner_name].get_stats_by_champid(self.champ_id))
                self.data[self.summoner_name].get_averages(self.data[self.summoner_name].relevant_stats)
                self.final_stats[self.summoner_name][self.champ_name] = Counter(self.data[self.summoner_name].convert())
            except:
                print "in exception section of data loop..."
                self.error = "No data for champ"
##                self.final_stats.pop(summoner_name)
                self.final_stats[self.summoner_name][self.champ_name] = Counter({k: 0 for k in self.data[self.summoner_name].converted_stats_names})
                raise self.error
        print "it got to the end...!"
            
##        if do_all is False and self.error:
##            raise self.error

    def _get_summary_stats(self, summoner_names, champ_names):
        """Method for averaging team stats based on summoners already
        retrieved."""

        self.summoner_names = [name for name in summoner_names]
        self.champ_names = [name for name in champ_names]
        
        # insert checker here
        self._check_entries()
            
##        self.num = len([len(self.data) for i in self.data if self.data[i] is not None])
##        self.num = len({i for i in summoner_names if i is not None}) # find best way to do this
##        self.num_games = sum([self.final_stats[i]['Total Games'] for i in self.final_stats if 'Total Games' in self.final_stats[i].keys()])

        
        self.num_data = [self.final_stats[name][champ]['Games'] for name, champ in self.data_pairs if self.final_stats[name][champ]['Games'] is not 0]
        self.num_games = sum(self.num_data)
        self.num = len(self.num_data)

        print self.num_data
        print "Number of games is :", self.num_games

        
##        newdict = dict((x, {k: 0 for k in range(3)}) for x in range(2))
##        self.team_data = dict((summoner, {stat: 0 for stat in self.data[summoner]}) for summoner in self.data)
##        for summoner in self.data:
##            self.team_data[summoner] = {}
##            for
        self.ew_data = Counter()
        self.nonew_data = Counter()
        
##        for num, name in enumerate(self.summoner_names):
##            self.nonew_data += self.final_stats[name][champ_names[num]]

        for name, champ in self.data_pairs:
            self.nonew_data += self.final_stats[name][champ]
            self.champ_id = [self.staticdata.champs_by_name[i] for i in self.staticdata.champs_by_name if i.lower() == champ.lower()] or [self.staticdata.champ_list[i]['id'] for i in self.staticdata.champ_list.keys() if i.lower() == champ.lower()]
            self.champ_id = self.champ_id.pop(0) 
            self.ew_data += Counter(self.data[name].get_stats_by_champid(self.champ_id))

        

##        for num, name in enumerate(self.summoner_names):
####            if hasattr(self.data[name], 'champ_stats'):
##            if self.final_stats[name][self.champ_names[num]]['Games'] != 0:
##                self.champ_id = [self.staticdata.champs_by_name[i] for i in self.staticdata.champs_by_name if i.lower() == self.champ_names[num].lower()] or [self.staticdata.champ_list[i]['id'] for i in self.staticdata.champ_list.keys() if i.lower() == self.champ_names[num].lower()]
##                self.champ_id = self.champ_id.pop(0) 
##                self.ew_data += Counter(self.data[name].get_stats_by_champid(self.champ_id))

        self.ave_stats = {'Ave': {key: round((self.nonew_data[key]/self.num), 2) for key in self.nonew_data}}
        self.ave_stats['EWAve'] = self._convert_bad_stats(self.ew_data)    
        print "Equally weighted averages: "
        for k, v in self.ave_stats['EWAve'].items():
            print k, ": ", v

        print
        print "Just averages: "
        for k, v in self.ave_stats['Ave'].items():
            print k, ": ", v


##        print self.final_stats['EWAve']
##        print self.final_stats['Ave']
    def _convert_bad_stats(self, ew_data):
        """Method for converting equally weighted averages into
        standard format, because it has awkward Riot JSON fields."""
        new_data = {}
        new_data['Gold'] = round((ew_data['totalGoldEarned']/self.num_games), 2)
        new_data['Games'] = round((self.num_games/self.num), 2)
        new_data['Kills'] = round((ew_data['totalChampionKills']/self.num_games), 2)
        new_data['Assists'] = round((ew_data['totalAssists']/self.num_games), 2)
        new_data['Deaths'] = round((ew_data['totalDeathsPerSession']/self.num_games), 2)
        new_data['CS'] = round((ew_data['totalMinionKills']/self.num_games), 2)
        new_data['Win Rate'] = round(((ew_data['totalSessionsWon']/self.num_games)*100), 2)
        new_data['Towers'] = round((ew_data['totalTurretsKilled']/self.num_games), 2)
        if ew_data['totalDeathsPerSession'] != 0:
            new_data['KDA'] = round(((ew_data['totalChampionKills'] + ew_data['totalAssists'])/ew_data['totalDeathsPerSession']), 2)
        else:
            new_data['KDA'] = round(((ew_data['totalChampionKills'] + ew_data['totalAssists'])/1), 2)
        return new_data

    def _check_entries(self):
        """Method for removing bad entries in final stats based on
        same requirements as _get_champ_stats() so that the
        summary/ave stats are still calculated correctly."""
        ## Things to check for: 1. Summoner name exists in final_stats 2. 
        
        self.backup_final_stats = self.final_stats
        self.data_pairs = []
        for name, champ in zip(self.summoner_names, self.champ_names):
            if name in self.final_stats:
                if champ in self.final_stats[name]:
                    if self.final_stats[name][champ]['Games'] is not 0:
                        self.data_pairs.append((name, champ))

    def _update(self):
        """Updates when the region is not the default."""
        self.proxy_instance = LoLTeamCheckerProxyHelper(self.region)
        # Don't reload static champ list, assume they're the same
        # across regions.
        
