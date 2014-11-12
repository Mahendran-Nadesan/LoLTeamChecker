'''
LoLTeamChecker ProxyHelper ClientSide

Wraps calls eventually destined for the Riot servers.
'''

import requests
import constants

class LoLTeamCheckerProxyHelper:
	'''API that converts LoLTeamChecker requests for Riot servers via a proxy server, returning data to the desktop client.
	'''
	def __init__(self, region):
		self.base_url = constants.PROXY
		self.region = region
		self.error = []

	def send_request(self, request):
		print self.base_url+'/{region}/{request}'.format(region=self.region, request=request)
		try:
			self.r = requests.get(self.base_url+'/{region}/{request}'.format(region=self.region, request=request))
			print self.r.url
			return self.r.json()
		except:
			self.error = self.r.status_code
			raise self.error

	def get_summoner_by_name(self, summoner_name):
		return self.send_request('summoner/{summoner_name}'.format(summoner_name=summoner_name))

	def get_ranked_stats_by_summoner_id(self, summoner_id):
		return self.send_request('ranked/{summoner_id}'.format(summoner_id=summoner_id))

	def static_get_champion_list(self):
		return self.send_request('champion')
