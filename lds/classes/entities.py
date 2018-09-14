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
            'name': self.player_name,
            'summoner_name': self.summoner_name,
            'region': region,
            'main_role': self.main_role,
            'team_abbv': self.team,
            'substitute': self.substitute,
            'account_type': self.account_type,
            'account_id': summoner['accountId'],
            'id': summoner['id'],
            'key': region + str(summoner['accountId'])
        }
        return result


class Game:
    def __init__(self, season, split, date, week, event, game_n, match_history, blue_team, red_team, participants):
        self.season = season
        self.split = split
        self.date = date
        self.week = week
        self.event = event
        self.game_n = game_n
        self.match_history = match_history
        self.blue_team = blue_team
        self.red_team = red_team
        self.participants = participants

    def get_game(self):
        mh = self.match_history
        realm = mh.split('/')[5]
        game_id = mh.split('/')[6].split('?')[0]
        series_id = self.blue_team + '_' + self.red_team
        try:
            game_hash = mh.split('/')[6].split('?')[1].split('=')[1].split('&')[0]
            if game_hash == 'overview':
                game_hash = None
        except IndexError:
            game_hash = None

        result = {
            'season': self.season,
            'split': self.split,
            'date': self.date,
            'series_id': series_id,
            'week': self.week,
            'event': self.event,
            'game': self.game_n,
            'game_id': game_id,
            'realm': realm,
            'hash': game_hash,
            'match_history': self.match_history,
            'blue': self.blue_team,
            'red': self.red_team,
        }
        participants = {'p{}'.format(i): p for i, p in enumerate(self.participants)}
        result.update(participants)
        return result

