# small debugging script

from LoLTeamChecker import *
from collections import Counter

name = 'nadsofmahen'
champ = 'rumble'
row = 0

# set user values for row 0
myapp.gui.user_values['Summoner Name'][row].set(name)
myapp.gui.user_values['Champion Name'][row].set(champ)

# imitate myapp._process_line(row):

# get id
summoner_id = myapp.model.proxy_instance.get_summoner_by_name(name)[name]['id']

# get ranked data
myapp.model.data[name] = GrabRankedData(myapp.model.proxy_instance.get_ranked_stats_by_summoner_id(summoner_id))

# prep final stats, champ id
myapp.model.final_stats[name] = {}
champ_id = [myapp.model.staticdata.champ_list[i]['id'] for i in
            myapp.model.staticdata.champ_list.keys() if i.lower() ==
            champ.lower()]
champ_id = champ_id.pop(0)
myapp.model.data[name].make_relevant(myapp.model.data[name].get_stats_by_champid(champ_id))

# check output so far
print "Relevant stats are ", myapp.model.data[name].relevant_stats

# convert to averages
averagedata = myapp.model.data[name].get_averages(myapp.model.data[name].relevant_stats)

# check output
print "Average data should be: "
print myapp.model.data[name].ave_stats

# final conversion
myapp.model.final_stats[name][champ] = Counter(myapp.model.data[name].convert())
