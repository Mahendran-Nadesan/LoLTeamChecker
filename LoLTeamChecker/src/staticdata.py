# Static API (requested) data class file
# Takes raw json data and converts to easier/small dicts

##from riotapi_py import RiotApiPy 


class GrabStaticData:
    """Converts data requested through RiotAPI from the static site
    (https://global.api.pvp.net/api/lol/static/...) to returnable
    items. """
    def __init__(self, champ_list):
        """Gets Champ list from api.static_get_champion_list() - i.e.
        stores a local copy of the list and accesses that."""
        self.champ_list = champ_list['data']
        self._sort()

    @staticmethod
    def api_get_champname(api_returned_champdata):
        """Takes the API returned data from
        api.static_get_champion_by_id(championid) and returns the
        champion name. Note, using this requires a request to the
        API."""
        return api_returned_champdata['name']
        
    @staticmethod
    def api_get_champid(api_returned_champdata):
        """Takes the API returned data from
        api.static_get_champion_by_id(championid) and returns the
        champion id. Note, using this requires a request to the
        API."""
        return api_returned_champdata['id']
        
    def get_champname(self, champid):
        """Take the api instance and the champ id and return the
        champ name"""
        # example: name =
        # GrabStaticData.get_champname(api_instance.static_get_champion_by_id(30))
        return self.champs_by_id[champid]

    def get_champid(self, champname):
        """Return the ID of a champ by looking it up in the new
        dict."""
        # This needs to be edited to return for fname list too.
        return self.champs_by_name[champname]
        

    def _sort(self):
        """Make two list of all champs for easier access (instead of
        always calling using the API)"""
        self.champs_by_name = {}
        self.champs_by_id = {}
        self.champs_by_fname = {}
        for i in self.champ_list:
            self.champs_by_name[self.champ_list[i]['name']] = self.champ_list[i]['id']
            self.champs_by_id[self.champ_list[i]['id']] = str(self.champ_list[i]['name'])
            self.champs_by_fname[i] = self.champ_list[i]['id']
        
        
