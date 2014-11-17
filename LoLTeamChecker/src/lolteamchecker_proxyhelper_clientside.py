"""Converts LoLTeamChecker data requests to proxy server requests.

Wraps method calls eventually destined for the Riot servers. Converts
based on LoLTeamChecker calls, and is not exhaustive of Riot API
calls. Currently supports the following methods:

get_summoner_by_name(summoner_name)
get_ranked_stats_by_summoner_id(summoner_id)
static_get_champion_list()
"""

import requests
import constants


class LoLTeamCheckerProxyHelper:
    """Convert LoLTeamChecker requests to proxy server requests."""
    def __init__(self, region):
        """Initialise proxy url and Riot API region."""
        self.base_url = constants.PROXY
        self.region = region
        self.error = []

    def send_request(self, request):
        """Send request to and return data from proxy."""
        try:
            self.r = requests.get(self.base_url+'/{region}/{request}'.format
                                  (region=self.region, request=request))
            print self.r.url
            return self.r.json()
        except:
            self.error = self.r.status_code
            raise self.error

    def get_summoner_by_name(self, summoner_name):
        """Get summoner details by summoner name."""
        return self.send_request('summoner/{summoner_name}'.format
                                 (summoner_name=summoner_name))

    def get_ranked_stats_by_summoner_id(self, summoner_id):
        """Get champion ranked data by summoner id."""
        return self.send_request('ranked/{summoner_id}'.format
                                 (summoner_id=summoner_id))

    def static_get_champion_list(self):
        """Get the static list of champion details."""
        return self.send_request('champion')
