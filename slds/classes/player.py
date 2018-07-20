from riotwatcher import RiotWatcher
from config.constants import API_KEY, REGIONS


class Player:
    def __init__(self, player_name, summoner_name, region, main_role, team, substitute, account_type):
        self.player_name = player_name
        self.summoner_name = summoner_name
        self.region = region
        self.main_role = main_role
        self.team = team
        self.substitute = substitute
        self.account_type = account_type
        self.rw = RiotWatcher(API_KEY)

    def get_player(self):
        region = REGIONS[self.region.upper()]
        summoner = self.rw.summoner.by_name(summoner_name=self.summoner_name, region=region)
        result = {
            'summoner_name': self.summoner_name,
            'region': region,
            'main_role': self.main_role,
            'team_abbv': self.team,
            'substitute': self.substitute,
            'account_type': self.account_type,
            'account_id': summoner['accountId'],
            'id': summoner['id'],
            'key': self.player_name
        }
        return result
