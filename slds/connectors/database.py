import urllib.request
import json
import pymysql.cursors
from pymongo import MongoClient
from itertools import chain
from riotwatcher import RiotWatcher
from tqdm import tqdm
from requests.exceptions import HTTPError
from config.constants import LEAGUES_DATA_DICT, SQL_EXPORTS_CONN, SQL_LEAGUES_CONN, MONGODB_CREDENTIALS, \
    OFFICIAL_LEAGUE, API_KEY, SOLOQ, REGIONS, SUPPORTED_LEAGUES


class DataBase:
    def __init__(self, region, league):
        self.rw = RiotWatcher(API_KEY)
        self.region = region
        self.league = league
        self.mongo_conn = MongoClient(MONGODB_CREDENTIALS)
        self.mongo_db = self.mongo_conn.slds
        self.sql_exports_conn = pymysql.connect(**SQL_EXPORTS_CONN)
        self.sql_leagues_conn = pymysql.connect(**SQL_LEAGUES_CONN)

    def get_league_game_ids(self, **kwargs):
        if self.league == 'SOLOQ':
            # Current game ids in DB
            soloq_m_coll = self.mongo_db.soloq_m
            cursor = soloq_m_coll.find({'platformId': self.region.upper()}, {'_id': 0, 'gameId': 1})
            current_game_ids = [gid['gameId'] for gid in cursor]
            # Players account ids in DB
            if 'team_abbv' in kwargs:
                print('Selecting games from {}.'.format(kwargs['team_abbv']))
                abbvs = kwargs['team_abbv'].split(',')
                if len(abbvs) == 1:
                    query = 'SELECT DISTINCT account_id FROM soloq WHERE team_abbv = {}'.format('\"' + abbvs[0] + '\"')
                elif len(abbvs) > 1:
                    query = 'SELECT DISTINCT account_id FROM soloq WHERE team_abbv IN {}'.format(tuple(abbvs))
                else:
                    print('No abbreviations selected. Check help for more information.')
                    return
            elif 'team_name' in kwargs:
                print('Selecting games from {}.'.format(kwargs['team_name']))
                names = kwargs['team_name'].split(',')
                if len(names) == 1:
                    query = 'SELECT DISTINCT account_id FROM soloq WHERE team_name = {}'.format('\"' + names[0] + '\"')
                elif len(names) > 1:
                    query = 'SELECT DISTINCT account_id FROM soloq WHERE team_name IN {}'.format(tuple(names))
                else:
                    print('No names selected. Check help for more information.')
                    return
            else:
                query = 'SELECT DISTINCT account_id FROM soloq'
            cursor = self.sql_leagues_conn.cursor()
            cursor.execute(query)
            acc_ids = [gid[0] for gid in cursor]
            # New Solo Q game ids
            if 'n_games' in kwargs:
                n_games = kwargs['n_games']
            else:
                n_games = 20
            if 'begin_index' in kwargs:
                begin_index = kwargs['begin_index']
            else:
                begin_index = 0
            new_game_ids = self.get_soloq_game_ids(acc_ids=acc_ids, n_games=n_games, begin_index=begin_index)
            return current_game_ids, new_game_ids


    @staticmethod
    def get_new_ids(old, new):
        return list(set(map(int, new)) - set(map(int, old)))

    def get_new_game_ids(self):
        league = self.league
        if league == ' SOLOQ':
            soloq_m_coll = self.mongo_db.soloq_m
            cursor = soloq_m_coll.find({}, {'_id': 0, 'gameId': 1})
            old = [gid['gameId'] for gid in cursor]
        else:
            return

    def download_games(self, current_game_ids, new_game_ids):
        def tournament_match_to_dict(id1, hash1, tournament):
            with urllib.request.urlopen('https://acs.leagueoflegends.com/v1/stats/game/{tr}/{id}'
                                        '?gameHash={hash}'.format(tr=tournament, id=id1, hash=hash1)) as url:
                match = json.loads(url.read().decode())
            with urllib.request.urlopen('https://acs.leagueoflegends.com/v1/stats/game/{tr}/{id}/timeline'
                                        '?gameHash={hash}'.format(tr=tournament, id=id1, hash=hash1)) as url:
                tl = json.loads(url.read().decode())
            return match, tl
        ids_not_in_db = self.get_new_ids(current_game_ids, new_game_ids)
        if ids_not_in_db:
            for item in tqdm(ids_not_in_db, desc='Downloading games'):
                try:
                    if LEAGUES_DATA_DICT[self.league][OFFICIAL_LEAGUE]:
                        pass
                    else:
                        match = self.rw.match.by_id(match_id=item, region=self.region)
                        timeline = self.rw.match.timeline_by_match(match_id=item, region=self.region)
                        data = {'match': match, 'timeline': timeline}
                        self.__save_match_raw_data(data=data)
                except HTTPError:
                    pass
        else:
            print('All games already downloaded.')
        return None

    def get_soloq_game_ids(self, acc_ids, **kwargs):
        if 'n_games' in kwargs:
            n_games = kwargs['n_games']
        else:
            n_games = 20

        if 'begin_index' in kwargs:
            begin_index = kwargs['begin_index']
        else:
            begin_index = 0
        matches = list(chain.from_iterable(
            [self.rw.match.matchlist_by_account(account_id=acc, begin_index=begin_index,
                                                end_index=int(begin_index)+int(n_games),
                                                region=self.region,
                                                queue=420)['matches'] for acc in acc_ids]))
        result = list(set([m['gameId'] for m in matches]))
        return result

    def __save_match_raw_data(self, data, **kwargs):
        if isinstance(data, dict):
            game_id = str(data['match']['gameId'])
            platform_id = data['match']['platformId']
            data['timeline']['gameId'] = game_id
            data['timeline']['platformId'] = platform_id
            if self.league == SOLOQ:
                soloq_m_coll = self.mongo_db.soloq_m
                soloq_tl_coll = self.mongo_db.soloq_tl
                soloq_m_coll.insert_one(data['match'])
                soloq_tl_coll.insert_one(data['timeline'])
        else:
            raise TypeError('Dict expected at data param. Should be passed as shown here: {"match": match_dict, '
                            '"timeline": timeline_dict}.')

    def get_supported_leagues(self):
        query = 'SELECT DISTINCT league_abbv FROM soloq'
        cursor = self.sql_leagues_conn.cursor()
        cursor.execute(query)
        return [abbv[0] for abbv in cursor]

    def get_supported_teams(self):
        query = 'SELECT DISTINCT team_abbv FROM soloq'
        cursor = self.sql_leagues_conn.cursor()
        cursor.execute(query)
        return [abbv[0] for abbv in cursor]


def parse_args(args):
    region = REGIONS[args.region.upper()]
    league = args.league.upper()
    db = DataBase(region, league)

    if args.download:
        if league == 'SOLOQ':
            if args.n_games:
                n_games = args.n_games
            else:
                n_games = 20
            if args.team_abbv:
                team_abbv = args.team_abbv
                current_game_ids, new_game_ids = db.get_league_game_ids(n_games=n_games, team_abbv=team_abbv)
            elif args.team_name:
                team_name = args.team_name
                current_game_ids, new_game_ids = db.get_league_game_ids(n_games=n_games, team_name=team_name)
            else:
                current_game_ids, new_game_ids = db.get_league_game_ids(n_games=n_games)
            db.download_games(current_game_ids=current_game_ids, new_game_ids=new_game_ids)
            print("Games downloaded.")
        else:
            pass

    if args.export:
        if league == 'SOLOQ':

        else:
            pass

